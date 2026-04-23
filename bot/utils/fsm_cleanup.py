"""Утилита очистки FSM и связанной tmp-директории.

Вынесена отдельно от handlers/voice.py, чтобы другие хендлеры (start.py)
могли импортировать её на уровне модуля без циклического импорта.
"""
from __future__ import annotations

import logging
import shutil

from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)


async def cleanup_state(state: FSMContext) -> None:
    """Удаляет tmp_dir из state и очищает FSM. Безопасно вызывать повторно."""
    try:
        data = await state.get_data()
    except Exception:
        data = {}
    tmp_dir = data.get("tmp_dir") if isinstance(data, dict) else None
    if tmp_dir:
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as exc:
            logger.warning("cleanup: не удалось удалить %s: %s", tmp_dir, exc)
    try:
        await state.clear()
    except Exception:
        pass
