from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.settings import settings

def unsub() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Подписаться на канал", url=settings.chat_url
    )
    kb.button(
        text="Начать просмотр", callback_data="get_started"
    )
    kb.adjust(1)
    return kb.as_markup()
