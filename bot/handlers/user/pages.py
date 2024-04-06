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
    if kp_api.current_index + 10 < len(kp_api.results):
        kp_api.current_index += 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index+10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)

async def prev_page(query: types.CallbackQuery):
    if kp_api.current_index >= 10:
        kp_api.current_index -= 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index+10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)