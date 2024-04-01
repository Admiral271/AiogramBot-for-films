from aiogram  import Bot, Dispatcher
from bot.settings import settings
import logging
from bot.handlers import user

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.tg_token)
    dp = Dispatcher()
    
    dp.include_routers(*user.routes)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)