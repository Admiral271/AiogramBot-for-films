from aiogram import Router, types

from bot.keyboards.inline import create_movie_buttons
from bot.handlers.user.search import kp_api

router = Router()

@router.callback_query()
async def process_callback(query: types.CallbackQuery):
    data = query.data

    if data == 'next_page':
        await next_page(query)
    elif data == 'prev_page':
        await prev_page(query)

async def next_page(query: types.CallbackQuery):
    kp_api.current_page += 1
    results = await kp_api.search_movies()
    if results:
        inline_kb = create_movie_buttons(results)
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
    else:
        await query.message.answer("К сожалению, на следующей странице ничего не найдено.")

async def prev_page(query: types.CallbackQuery):
    if kp_api.current_page > 1:
        kp_api.current_page -= 1
        results = await kp_api.search_movies()
        if results:
            inline_kb = create_movie_buttons(results)
            await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
        else:
            await query.message.answer("К сожалению, на предыдущей странице ничего не найдено.")
    else:
        await query.message.answer("Вы находитесь на первой странице.")
