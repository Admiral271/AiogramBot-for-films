from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower() == 'поиск по названию🔎')
async def search_by_name(message: Message):
    await message.answer(
        "Вызван сервис поиска по названию!"
    )