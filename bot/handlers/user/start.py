from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.reply import main_menu
from bot.keyboards.inline import unsub
from bot.handlers.user.check_subscribe import is_user_subscribed
from bot.settings import settings

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    channel_id = settings.chat_id
    if await is_user_subscribed(bot, user_id, channel_id):
        text = f"<b>Добро пожаловать, {message.from_user.first_name}!</b>\n\n" + \
        "📺 Вы находитесь в лучшем боте для просмотра фильмов и сериалов прямо в Telegram!\n\n"+ \
        "Смотрите сериалы на телефоне, планшете и компьютере." + \
        "Подписывайтесь на уведомления о новых сериях. Сортируйте сериалы по названию, жанрам и интересам." + \
        "Скачивайте сериалы себе на устройство и смотрите без интернета.\n\n" + \
        "<i>Используя бота, вы подтверждаете, что будете соблюдать возрастные ограничения сериалов.</i>"
        
        markup = main_menu()
        
    else:
        text = f"<b>Добро пожаловать, {message.from_user.first_name}!</b>\n\n" + \
        "Чтобы приступить к просмотру сериалов в боте, необходимо подписаться на наш канал " + \
        "— для этого воспользуйтесь кнопками ниже!👇\n\n" + \
        "После подписки на канал вернитесь обратно и нажмите кнопку «Приступить к просмотру». \n\n" + \
        "<i>Бот работает для вас и без ограничений! Наслаждайтесь!</i>"
        
        markup = unsub()
        
    await message.answer(
        text,
        parse_mode="html",
        reply_markup=markup
    )
    
