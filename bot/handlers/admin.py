"""Админ-панель — управление каналами и статистика
Команды:
  /admin — главное меню админки
  Добавить/удалить каналы через inline-кнопки
"""
import asyncio
import logging

from aiogram.exceptions import TelegramBadRequest

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.database import async_session
from bot.database.crud import (
    add_channel,
    get_active_channels,
    get_all_user_ids,
    get_user_language,
    get_user_stats,
    remove_channel,
)
from bot.emojis import E
from bot.i18n import t
from bot.keyboards.admin import (
    get_admin_keyboard,
    get_cancel_keyboard,
    get_channels_keyboard,
    get_confirm_broadcast_keyboard,
    get_confirm_delete_keyboard,
)

logger = logging.getLogger(__name__)
router = Router()


def is_admin(user_id: int) -> bool:
    """Проверяет, админ ли юзер"""
    return user_id in settings.admin_id_list


async def _get_lang(user_id: int) -> str:
    """Получает язык админа"""
    async with async_session() as session:
        return await get_user_language(session, user_id)


# === FSM для добавления канала ===

class AddChannelStates(StatesGroup):
    waiting_channel_id = State()
    waiting_title = State()
    waiting_invite_link = State()


class BroadcastStates(StatesGroup):
    waiting_message = State()
    confirming = State()


# === Команда /admin ===

@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    """Главное меню админки"""
    if not is_admin(message.from_user.id):
        lang = await _get_lang(message.from_user.id)
        await message.answer(t("admin.no_access", lang), parse_mode="HTML")
        return

    lang = await _get_lang(message.from_user.id)
    await message.answer(t("admin.title", lang),
        reply_markup=get_admin_keyboard(lang),
        parse_mode="HTML",
    )


# === Статистика ===

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery) -> None:
    """Показывает статистику"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return

    async with async_session() as session:
        stats = await get_user_stats(session)

    try:
        await callback.message.edit_text(t("admin.stats", lang, **stats),
            reply_markup=get_admin_keyboard(lang),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


# === Список каналов ===

@router.callback_query(F.data == "admin_channels")
async def admin_channels(callback: CallbackQuery) -> None:
    """Показывает список каналов"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return

    async with async_session() as session:
        channels = await get_active_channels(session)

    if not channels:
        text = t("admin.channels_empty", lang)
    else:
        lines = [t("admin.channels_title", lang)]
        for i, ch in enumerate(channels, 1):
            lines.append(
                f"{i}. <b>{ch.title}</b>\n"
                f"   ID: <code>{ch.channel_id}</code>\n"
                f"   {E['link']} {ch.invite_link}"
            )
        text = "\n".join(lines)

    await callback.message.edit_text(text,
        reply_markup=get_channels_keyboard(
            channels if channels else None, lang
        ),
        parse_mode="HTML",
    )
    await callback.answer()


# === Добавление канала (FSM) ===

@router.callback_query(F.data == "admin_add_channel")
async def start_add_channel(callback: CallbackQuery, state: FSMContext) -> None:
    """Начало добавления канала"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return
    await state.update_data(lang=lang)

    await callback.message.edit_text(t("admin.add_channel_id", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await state.set_state(AddChannelStates.waiting_channel_id)
    await callback.answer()


@router.message(AddChannelStates.waiting_channel_id)
async def process_channel_id(message: Message, state: FSMContext) -> None:
    """Получаем ID канала"""
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    lang = data.get("lang", "ru")

    try:
        channel_id = int(message.text.strip())
    except ValueError:
        await message.answer(t("admin.id_not_number", lang),
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML",
        )
        return

    await state.update_data(channel_id=channel_id)
    await message.answer(t("admin.add_channel_title", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await state.set_state(AddChannelStates.waiting_title)


@router.message(AddChannelStates.waiting_title)
async def process_title(message: Message, state: FSMContext) -> None:
    """Получаем название"""
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    lang = data.get("lang", "ru")

    title = message.text.strip()
    if len(title) > 200:
        await message.answer(t("admin.title_too_long", lang), parse_mode="HTML")
        return

    await state.update_data(title=title)
    await message.answer(t("admin.add_channel_link", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await state.set_state(AddChannelStates.waiting_invite_link)


@router.message(AddChannelStates.waiting_invite_link)
async def process_invite_link(message: Message, state: FSMContext) -> None:
    """Получаем ссылку и сохраняем канал"""
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    lang = data.get("lang", "ru")

    raw = message.text.strip()
    invite_link = _normalize_channel_link(raw)
    if not invite_link:
        await message.answer(t("admin.link_invalid", lang),
            reply_markup=get_cancel_keyboard(lang),
            parse_mode="HTML",
        )
        return

    await state.clear()

    try:
        async with async_session() as session:
            channel = await add_channel(
                session=session,
                channel_id=data["channel_id"],
                title=data["title"],
                invite_link=invite_link,
            )
        await message.answer(f"{t('admin.channel_added', lang)}\n\n"
            f"{E['megaphone']} {channel.title}\n"
            f"{E['info']} <code>{channel.channel_id}</code>\n"
            f"{E['link']} {channel.invite_link}",
            reply_markup=get_admin_keyboard(lang),
            parse_mode="HTML",
        )
    except ValueError as e:
        await message.answer(f"{E['cross']} {e}",
            reply_markup=get_admin_keyboard(lang),
            parse_mode="HTML",
        )


# === Удаление канала ===

@router.callback_query(F.data.startswith("admin_del_"))
async def confirm_delete_channel(callback: CallbackQuery) -> None:
    """Подтверждение перед удалением"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return
    channel_id = callback.data.replace("admin_del_", "")

    await callback.message.edit_text(t("admin.confirm_delete", lang, channel_id=channel_id),
        reply_markup=get_confirm_delete_keyboard(channel_id, lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_confirm_del_"))
async def delete_channel(callback: CallbackQuery) -> None:
    """Удаление канала"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return

    channel_id = int(callback.data.replace("admin_confirm_del_", ""))

    async with async_session() as session:
        removed = await remove_channel(session, channel_id)

    if removed:
        await callback.answer(t("admin.channel_deleted", lang))
    else:
        await callback.answer(t("admin.channel_not_found", lang))

    await admin_channels(callback)


# === Отмена FSM ===

@router.callback_query(F.data == "admin_cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext) -> None:
    """Отмена текущего действия"""
    await state.clear()
    lang = await _get_lang(callback.from_user.id)
    await callback.message.edit_text(t("admin.title", lang),
        reply_markup=get_admin_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


def _normalize_channel_link(raw: str) -> str | None:
    """Приводит ввод к формату https://t.me/..."""
    raw = raw.strip()

    if raw.startswith("https://t.me/"):
        return raw
    if raw.startswith("https://telegram.me/"):
        return raw.replace("https://telegram.me/", "https://t.me/")
    if raw.startswith("http://t.me/"):
        return raw.replace("http://", "https://")

    if raw.startswith("@"):
        username = raw[1:]
        if username and username.isascii():
            return f"https://t.me/{username}"
        return None

    if raw.isascii() and " " not in raw and len(raw) > 2:
        return f"https://t.me/{raw}"

    return None


# === Массовая рассылка ===

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    """Начало рассылки"""
    lang = await _get_lang(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return
    await state.update_data(lang=lang)

    await callback.message.edit_text(t("admin.broadcast_prompt", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await state.set_state(BroadcastStates.waiting_message)
    await callback.answer()


@router.message(BroadcastStates.waiting_message)
async def preview_broadcast(message: Message, state: FSMContext) -> None:
    """Получаем сообщение и показываем предпросмотр"""
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    lang = data.get("lang", "ru")

    msg_data = {"type": "text", "text": message.text or message.caption or ""}
    if message.photo:
        msg_data["type"] = "photo"
        msg_data["file_id"] = message.photo[-1].file_id
    elif message.video:
        msg_data["type"] = "video"
        msg_data["file_id"] = message.video.file_id

    await state.update_data(broadcast_msg=msg_data)

    confirm_kb = get_confirm_broadcast_keyboard(lang)

    if msg_data["type"] == "photo":
        await message.answer_photo(
            msg_data["file_id"],
            caption=msg_data["text"] or None,
        )
    elif msg_data["type"] == "video":
        await message.answer_video(
            msg_data["file_id"],
            caption=msg_data["text"] or None,
        )
    else:
        await message.answer(msg_data["text"])

    await message.answer(t("admin.broadcast_preview", lang),
        reply_markup=confirm_kb,
        parse_mode="HTML",
    )
    await state.set_state(BroadcastStates.confirming)


@router.callback_query(F.data == "admin_broadcast_confirm")
async def confirm_broadcast(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Подтверждение и запуск рассылки"""
    data = await state.get_data()
    lang = data.get("lang", "ru")
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin.no_access", lang))
        return
    msg_data = data.get("broadcast_msg")
    await state.clear()

    if not msg_data:
        await callback.answer(f"{E['cross']} {t('admin.broadcast.no_message', lang)}")
        return

    await callback.message.edit_text(t("admin.broadcast_started", lang), parse_mode="HTML")
    await callback.answer()

    async with async_session() as session:
        user_ids = await get_all_user_ids(session)

    bot_info = await callback.bot.get_me()
    skip_ids = {bot_info.id} | set(settings.admin_id_list)
    user_ids = [uid for uid in user_ids if uid not in skip_ids]

    bot = callback.bot
    success = 0
    failed = 0

    for user_id in user_ids:
        try:
            if msg_data["type"] == "photo":
                await bot.send_photo(
                    user_id,
                    msg_data["file_id"],
                    caption=msg_data["text"] or None,
                )
            elif msg_data["type"] == "video":
                await bot.send_video(
                    user_id,
                    msg_data["file_id"],
                    caption=msg_data["text"] or None,
                )
            else:
                await bot.send_message(user_id, msg_data["text"])
            success += 1
        except Exception as e:
            logger.warning(f"Рассылка: не доставлено {user_id}: {e}")
            failed += 1

        # пауза — лимит Telegram ~30 msg/sec
        if (success + failed) % 25 == 0:
            await asyncio.sleep(1)

    await callback.message.answer(t("admin.broadcast_done", lang,
          success=success, failed=failed, total=len(user_ids)),
        reply_markup=get_admin_keyboard(lang),
        parse_mode="HTML",
    )
