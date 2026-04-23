"""Inline-клавиатуры — меню, подписка, язык, эффекты"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.emojis import E_ID
from bot.i18n import t


def get_start_keyboard(user_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    """Главное меню бота."""
    buttons = [
        [InlineKeyboardButton(
            text=t("btn.voice_effect", lang),
            callback_data="voice_effect",
            style="primary",
            icon_custom_emoji_id=E_ID["music"],
        )],
        [
            InlineKeyboardButton(
                text=t("btn.profile", lang),
                callback_data="my_profile",
                style="success",
                icon_custom_emoji_id=E_ID["profile"],
            ),
            InlineKeyboardButton(
                text=t("btn.help", lang),
                callback_data="help",
                style="success",
                icon_custom_emoji_id=E_ID["info"],
            ),
        ],
        [InlineKeyboardButton(
            text=t("btn.language", lang),
            callback_data="change_language",
            style="success",
            icon_custom_emoji_id=E_ID["gear"],
        )],
    ]

    if user_id in settings.admin_id_list:
        buttons.append([InlineKeyboardButton(
            text=t("btn.admin_panel", lang),
            callback_data="admin_panel",
            style="danger",
            icon_custom_emoji_id=E_ID["lock"],
        )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка 'Назад' в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_subscription_keyboard(
    channels: list[dict], lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Клавиатура подписки на каналы"""
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(
            text=f"{ch['title']}",
            url=ch["invite_link"],
            style="primary",
            icon_custom_emoji_id=E_ID["megaphone"],
        )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.check_sub", lang),
        callback_data="check_subscription",
        style="success",
        icon_custom_emoji_id=E_ID["check"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Русский",
                callback_data="set_lang_ru",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_ru"],
            ),
            InlineKeyboardButton(
                text="O'zbek",
                callback_data="set_lang_uz",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_uz"],
            ),
            InlineKeyboardButton(
                text="English",
                callback_data="set_lang_en",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_gb"],
            ),
        ],
    ])


def get_effects_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура выбора голосового эффекта."""
    def fx(name: str, icon: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=t(f"effect.{name}", lang),
            callback_data=f"fx:{name}",
            style="primary",
            icon_custom_emoji_id=E_ID[icon],
        )

    return InlineKeyboardMarkup(inline_keyboard=[
        [fx("studio", "star"), fx("chipmunk", "lightning"), fx("helium", "plus")],
        [fx("bass", "music"), fx("robot", "bot"), fx("ghost", "search")],
        [fx("whisper", "eye"), fx("radio", "link"), fx("cathedral", "book")],
        [fx("megaphone", "megaphone"), fx("phaser", "bulb"), fx("vinyl", "refresh")],
        [fx("podcast", "edit"), fx("dubstep", "lightning")],
        [fx("speed_up", "lightning"), fx("slow_down", "clock")],
        [InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data="voice_cancel",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        )],
    ])


def get_another_effect_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопки после успешного применения эффекта"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.another_effect", lang),
            callback_data="another_effect",
            style="primary",
            icon_custom_emoji_id=E_ID["refresh"],
        )],
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_voice_cancel_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Одна кнопка 'Отмена' — для FSM-шагов ожидания голосового."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data="voice_cancel",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        )],
    ])
