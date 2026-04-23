"""Клавиатуры админ-панели"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.emojis import E_ID
from bot.i18n import t


def get_admin_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Главное меню админки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.admin_stats", lang),
            callback_data="admin_stats",
            style="primary",
            icon_custom_emoji_id=E_ID["chart"],
        )],
        [InlineKeyboardButton(
            text=t("btn.admin_channels", lang),
            callback_data="admin_channels",
            style="primary",
            icon_custom_emoji_id=E_ID["megaphone"],
        )],
        [InlineKeyboardButton(
            text=t("btn.admin_broadcast", lang),
            callback_data="admin_broadcast",
            style="danger",
            icon_custom_emoji_id=E_ID["plane"],
        )],
        [InlineKeyboardButton(
            text=t("btn.admin_home", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["home"],
        )],
    ])


def get_channels_keyboard(
    channels: list | None, lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Список каналов с кнопками удаления"""
    buttons = []
    if channels:
        for ch in channels:
            buttons.append([InlineKeyboardButton(
                text=f"{ch.title}",
                callback_data=f"admin_del_{ch.channel_id}",
                style="danger",
                icon_custom_emoji_id=E_ID["trash"],
            )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.admin_add", lang),
        callback_data="admin_add_channel",
        style="success",
        icon_custom_emoji_id=E_ID["plus"],
    )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.admin_back", lang),
        callback_data="admin_panel",
        style="success",
        icon_custom_emoji_id=E_ID["back"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cancel_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка отмены"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.admin_cancel", lang),
            callback_data="admin_cancel",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        )],
    ])


def get_confirm_delete_keyboard(channel_id: str | int, lang: str = "ru") -> InlineKeyboardMarkup:
    """Подтверждение удаления канала"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=t("btn.admin_confirm_del", lang),
                callback_data=f"admin_confirm_del_{channel_id}",
                style="danger",
                icon_custom_emoji_id=E_ID["trash"],
            ),
            InlineKeyboardButton(
                text=t("btn.admin_cancel_del", lang),
                callback_data="admin_channels",
                style="success",
                icon_custom_emoji_id=E_ID["check"],
            ),
        ],
    ])


def get_confirm_broadcast_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Подтверждение запуска рассылки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=t("admin.broadcast_confirm", lang),
                callback_data="admin_broadcast_confirm",
                style="success",
                icon_custom_emoji_id=E_ID["check"],
            ),
            InlineKeyboardButton(
                text=t("admin.broadcast_cancel", lang),
                callback_data="admin_cancel",
                style="danger",
                icon_custom_emoji_id=E_ID["cross"],
            ),
        ],
    ])
