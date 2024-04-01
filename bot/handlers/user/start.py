from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.reply import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привет! {message.from_user.first_name}",
        reply_markup=main_menu()
    )
    
