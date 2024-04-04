from aiogram import Router, F, types

from bot.api import KinoPoiskAPI
from bot.keyboards.inline import create_movie_buttons
from bot.settings import settings

router = Router()
kp_api = KinoPoiskAPI(settings.kp_token)

@router.message(F.text.lower() == 'поиск по названию🔎')
async def search_by_name(message: types.Message):
    await message.answer("Введите название фильма или сериала, который вы хотите найти:")

@router.message()
async def get_search_results(message: types.Message):
    query = message.text
    kp_api.last_query = query 
    results = await kp_api.search_movies(query)
    if results:  
        inline_kb = create_movie_buttons(results)
        await message.answer("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
    else:
        await message.answer("К сожалению, по вашему запросу ничего не найдено.")
