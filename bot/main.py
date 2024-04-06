import logging
import asyncio
from aiogram  import Bot, Dispatcher

from bot.settings import settings
from bot.handlers import user

logging.basicConfig(level=logging.INFO)
logging.getLogger('aiogram.event').setLevel(logging.CRITICAL)

async def main():
    bot = Bot(token=settings.tg_token)
    dp = Dispatcher()
    
    dp.include_routers(*user.routes)
    
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass 