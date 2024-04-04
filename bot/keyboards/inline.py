from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

def create_movie_buttons(results) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for movie in results:
        button_text = f"{movie['name']} ({movie['year']})"
        callback_data = f"movie:{movie['id']}"
        kb.row(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    kb.row(
        InlineKeyboardButton(text="« Назад", callback_data="prev_page"),
        InlineKeyboardButton(text="Далее »", callback_data="next_page")
    )
    return kb.as_markup()