"""Хэндлер голосовых эффектов — FSM-флоу.

Состояния:
  1. waiting_voice  — ждём голосовое/аудио
  2. waiting_effect — ждём выбор эффекта (inline-кнопки)
  3. processing     — обрабатываем файл

Cleanup — явный, синхронно по завершении хендлера.
"""
from __future__ import annotations

import asyncio
import logging
import os
import shutil
import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.database import async_session
from bot.database.crud import get_user_language, increment_user_effect_count
from bot.i18n import t
from bot.keyboards.inline import (
    get_another_effect_keyboard, get_back_keyboard,
    get_effects_keyboard, get_start_keyboard, get_voice_cancel_keyboard,
)
from bot.services.voice_effects import VoiceEffectError, apply_effect, classify_error
from bot.utils.fsm_cleanup import cleanup_state

logger = logging.getLogger(__name__)
router = Router()

TMP_ROOT = "/tmp/voice_bot"
MAX_INPUT_SIZE = 20 * 1024 * 1024


class VoiceStates(StatesGroup):
    waiting_voice = State()
    waiting_effect = State()
    processing = State()


_user_locks: dict[int, asyncio.Lock] = {}


def _get_user_lock(user_id: int) -> asyncio.Lock:
    lock = _user_locks.get(user_id)
    if lock is None:
        lock = asyncio.Lock()
        _user_locks[user_id] = lock
    return lock


def cleanup_user_locks() -> int:
    """Чистит освобождённые блокировки — вызывается из фоновой задачи.

    Удаляем только незаблокированные локи, чтобы не сломать активную обработку.
    Возвращает число удалённых записей.
    """
    removed = 0
    for user_id in list(_user_locks.keys()):
        lock = _user_locks.get(user_id)
        if lock is not None and not lock.locked():
            _user_locks.pop(user_id, None)
            removed += 1
    return removed


async def _get_lang(user_id: int) -> str:
    async with async_session() as session:
        return await get_user_language(session, user_id)


@router.message(F.voice | F.audio)
async def handle_voice(message: Message, state: FSMContext) -> None:
    """Принимает голосовое сообщение или аудиофайл."""
    current = await state.get_state()
    lang = await _get_lang(message.from_user.id)

    if current == VoiceStates.processing.state:
        await message.answer(t("voice.busy", lang), parse_mode="HTML")
        return

    voice = message.voice
    audio = message.audio

    if voice is not None:
        file_id = voice.file_id
        file_size = voice.file_size or 0
        file_ext = ".ogg"
    elif audio is not None:
        file_id = audio.file_id
        file_size = audio.file_size or 0
        file_name = audio.file_name or ""
        if file_name and "." in file_name:
            file_ext = "." + file_name.rsplit(".", 1)[1].lower()
        else:
            mime = (audio.mime_type or "").lower()
            ext_map = {"audio/mpeg": ".mp3", "audio/ogg": ".ogg",
                       "audio/wav": ".wav", "audio/mp4": ".m4a",
                       "audio/aac": ".aac", "audio/flac": ".flac"}
            file_ext = ext_map.get(mime, ".mp3")
    else:
        await message.answer(t("voice.error_not_audio", lang), parse_mode="HTML")
        return

    if file_size and file_size > MAX_INPUT_SIZE:
        await message.answer(t("error.too_large", lang), parse_mode="HTML")
        return

    if current == VoiceStates.waiting_effect.state:
        await cleanup_state(state)

    os.makedirs(TMP_ROOT, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix="voice_", dir=TMP_ROOT)
    input_path = str(Path(tmp_dir) / f"input{file_ext}")

    try:
        file_obj = await message.bot.get_file(file_id)
        api_file_path: str = file_obj.file_path
        await message.bot.download_file(api_file_path, destination=input_path)
    except Exception as exc:
        logger.exception("download: %s", exc)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        await message.answer(t("voice.error_download", lang), parse_mode="HTML")
        return

    await state.set_state(VoiceStates.waiting_effect)
    await state.update_data(tmp_dir=tmp_dir, input_path=input_path)

    await message.answer(t("voice.choose_effect", lang),
        reply_markup=get_effects_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(VoiceStates.waiting_effect, F.data.startswith("fx:"))
async def handle_effect_choice(callback: CallbackQuery, state: FSMContext) -> None:
    """Юзер выбрал эффект — применяем."""
    lang = await _get_lang(callback.from_user.id)
    effect_name = callback.data.split(":", 1)[1]

    lock = _get_user_lock(callback.from_user.id)
    if lock.locked():
        try:
            await callback.answer(t("voice.busy", lang), show_alert=True)
        except Exception:
            pass
        return

    async with lock:
        current = await state.get_state()
        if current != VoiceStates.waiting_effect.state:
            await callback.answer()
            return

        data = await state.get_data()
        tmp_dir = data.get("tmp_dir")
        input_path = data.get("input_path")

        if not tmp_dir or not input_path or not os.path.exists(input_path):
            await cleanup_state(state)
            try:
                await callback.message.edit_text(t("voice.error_download", lang),
                    reply_markup=get_back_keyboard(lang), parse_mode="HTML")
            except Exception:
                pass
            await callback.answer()
            return

        await state.set_state(VoiceStates.processing)
        effect_label = t(f"effect.{effect_name}", lang)
        await callback.answer()
        try:
            await callback.message.edit_text(t("voice.processing", lang, effect=effect_label), parse_mode="HTML")
        except Exception:
            pass

        output_path = str(Path(tmp_dir) / f"output_{effect_name}.ogg")
        success = False

        try:
            await apply_effect(
                input_path=Path(input_path),
                output_path=Path(output_path),
                effect_name=effect_name,
            )

            try:
                await callback.message.answer_voice(
                    voice=FSInputFile(output_path),
                    caption=t("voice.done", lang, effect=effect_label),
                    parse_mode="HTML",
                    reply_markup=get_another_effect_keyboard(lang),
                )
                success = True
            except Exception as exc:
                logger.exception("send_voice: %s", exc)
                await callback.message.answer(t("error.generic", lang), parse_mode="HTML")

            async with async_session() as session:
                await increment_user_effect_count(session, callback.from_user.id)

        except VoiceEffectError as exc:
            category = classify_error(exc)
            logger.warning("apply_effect: %s (%s)", exc, category)
            msg_key = {
                "file_too_large": "error.too_large",
                "unsupported_format": "voice.error_not_audio",
                "ffmpeg_error": "voice.error_ffmpeg",
                "network": "error.timeout",
            }.get(category, "voice.error_ffmpeg")
            try:
                await callback.message.answer(t(msg_key, lang), reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML")
            except Exception:
                pass
        except Exception as exc:
            logger.exception("voice: неизвестная ошибка: %s", exc)
            try:
                await callback.message.answer(t("error.generic", lang), reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML")
            except Exception:
                pass
        finally:
            try:
                if output_path and os.path.exists(output_path):
                    os.unlink(output_path)
            except Exception:
                pass
            if success and os.path.exists(input_path):
                await state.set_state(VoiceStates.waiting_effect)
                await state.update_data(tmp_dir=tmp_dir, input_path=input_path)
            else:
                await cleanup_state(state)


@router.callback_query(F.data == "another_effect")
async def another_effect(callback: CallbackQuery, state: FSMContext) -> None:
    """Юзер хочет применить другой эффект к тому же голосовому."""
    lang = await _get_lang(callback.from_user.id)
    data = await state.get_data()
    tmp_dir = data.get("tmp_dir")
    input_path = data.get("input_path")

    if input_path and os.path.exists(input_path):
        await state.set_state(VoiceStates.waiting_effect)
        await state.update_data(tmp_dir=tmp_dir, input_path=input_path)
        await callback.message.answer(t("voice.choose_effect", lang),
            reply_markup=get_effects_keyboard(lang), parse_mode="HTML")
        await callback.answer()
        return

    await cleanup_state(state)
    await state.set_state(VoiceStates.waiting_voice)
    await callback.message.answer(t("voice.send_audio", lang),
        reply_markup=get_voice_cancel_keyboard(lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "voice_cancel")
async def voice_cancel_callback(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    current = await state.get_state()
    if current == VoiceStates.processing.state:
        await callback.answer(t("voice.busy", lang), show_alert=True)
        return
    await cleanup_state(state)
    try:
        await callback.message.edit_text(t("voice.cancelled", lang),
            reply_markup=get_start_keyboard(user_id=callback.from_user.id, lang=lang),
            parse_mode="HTML")
    except Exception:
        await callback.message.answer(t("voice.cancelled", lang),
            reply_markup=get_start_keyboard(user_id=callback.from_user.id, lang=lang),
            parse_mode="HTML")
    await callback.answer()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    lang = await _get_lang(message.from_user.id)
    current = await state.get_state()
    if current == VoiceStates.processing.state:
        await message.answer(t("voice.busy", lang), parse_mode="HTML")
        return
    await cleanup_state(state)
    await message.answer(t("voice.cancelled", lang),
        reply_markup=get_start_keyboard(user_id=message.from_user.id, lang=lang),
        parse_mode="HTML")
