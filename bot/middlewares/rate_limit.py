"""Rate limiting — ограничение частоты запросов на обработку голосовых
Лимит: 5 запросов в минуту на юзера
Хранение в памяти — без Redis/БД, сбрасывается при перезапуске
"""
import time
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.i18n import detect_language, t

logger = logging.getLogger(__name__)

# лимит — сколько операций в минуту
MAX_REQUESTS = 5
WINDOW_SECONDS = 60

# {user_id: [timestamp1, timestamp2, ...]}
_user_requests: dict[int, list[float]] = {}


def cleanup_stale_entries() -> int:
    """Удаляет протухшие записи из _user_requests.
    Вызывается фоновой задачей раз в несколько минут.
    Возвращает количество удалённых записей.
    """
    now = time.time()
    stale_users = [
        uid for uid, timestamps in _user_requests.items()
        if not any(now - ts < WINDOW_SECONDS for ts in timestamps)
    ]
    for uid in stale_users:
        del _user_requests[uid]
    if stale_users:
        logger.debug("Rate limit: удалено %d устаревших записей", len(stale_users))
    return len(stale_users)


def is_heavy_request(message: Message) -> bool:
    """Проверяет, является ли сообщение тяжёлой операцией (голосовое/аудио)."""
    return message.voice is not None or message.audio is not None


class RateLimitMiddleware(BaseMiddleware):
    """Ограничивает частоту обработки — только для голосовых/аудио сообщений"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # ограничиваем только голосовые/аудио (тяжёлые операции)
        if not isinstance(event, Message):
            return await handler(event, data)

        if not is_heavy_request(event):
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.time()

        # чистим старые записи
        if user_id in _user_requests:
            _user_requests[user_id] = [
                ts for ts in _user_requests[user_id]
                if now - ts < WINDOW_SECONDS
            ]
        else:
            _user_requests[user_id] = []

        # проверяем лимит
        if len(_user_requests[user_id]) >= MAX_REQUESTS:
            oldest = _user_requests[user_id][0]
            wait_sec = int(WINDOW_SECONDS - (now - oldest)) + 1
            lang = detect_language(event.from_user.language_code)
            await event.answer(
                t("error.rate_limit", lang, seconds=wait_sec),
            )
            logger.info(f"Rate limit для {user_id}: подождать {wait_sec} сек")
            return None

        # записываем запрос и пропускаем
        _user_requests[user_id].append(now)
        return await handler(event, data)
