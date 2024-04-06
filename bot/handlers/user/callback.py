from aiogram import Router, types
import logging

import os
import subprocess
import aiofiles
import asyncio

from bot.keyboards.inline import create_movie_buttons
from bot.handlers.user.search import kp_api
from bot.api import KinoClubAPI
from bot.settings import settings

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query()
async def process_callback(query: types.CallbackQuery):
    data = query.data

    if data == 'pages:next_page':
        await next_page(query)
    elif data == 'pages:prev_page':
        await prev_page(query)
    elif data.startswith("movie:"):
        await process_movie_callback(query)

async def next_page(query: types.CallbackQuery):
    logger.info("Обработчик next_page вызван")
    if kp_api.current_index + 10 < len(kp_api.results):
        kp_api.current_index += 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index+10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
        logger.info("Обработчик next_page обработал callback следующей страницы")

async def prev_page(query: types.CallbackQuery):
    logger.info("Обработчик prev_page вызван")
    if kp_api.current_index >= 10:
        kp_api.current_index -= 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index+10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
        logger.info("Обработчик prev_page обработал callback предыдущей страницы")
        
async def process_movie_callback(query: types.CallbackQuery):
    logger.info("Обработчик process_movie_callback вызван")
    movie_id = query.data.split(":")[1]
    
    kinoclub_api = KinoClubAPI(settings.kinoclub_token)

    movie_data = await kinoclub_api.get_movie(movie_id)

    if movie_data is not None and "data" in movie_data:
        data = movie_data["data"]
        if all(key in data for key in ("name", "type", "full_description", "poster")):
            name = data["name"]
            movie_type = data["type"]
            full_description = data["full_description"]
            poster_url = data["poster"]
            
            if movie_type == "film":
                movie_type = "Фильм"
                movie_url = data["url"]
                # Отправить сообщение пользователю о начале процесса загрузки
                message = await query.message.answer("Начинаю загрузку видео...")
                
                if not os.path.exists("tempfiles"):
                    os.makedirs("tempfiles")

                # Загрузить и преобразовать файл
                process = subprocess.run(["yt-dlp", "--newline", "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36", "-o", f"tempfiles/{movie_id}.mp4", movie_url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                # Отправить файл пользователю
                message = await query.message.answer("Файл загружен, отправляю")
                async with aiofiles.open(f"tempfiles/{movie_id}.mp4", 'rb') as f:
                    await query.message.answer_video(f)

                # Удалить временный файл
                os.remove("tempfiles/{movie_id}.mp4")
                
            elif movie_type == "serial":
                movie_type = "Сериал"
                seasons = data["seasons"]
                seasons_dict = {}
                for season in seasons:
                    season_title = season["title"]
                    series_dict = {}
                    for series in season["series"]:
                        series_title = series["seria"]
                        series_url = series["url"]
                        series_dict[series_title] = series_url
                    seasons_dict[season_title] = series_dict

            message_text = f"<b>{movie_type}</b>: {name}\\n\\n<b>Описание</b>:\\n{full_description}"

            logger.info(f"Обработчик process_movie_callback отправил сообщение с информацией о '{name}' (id:{movie_id})")
            await query.message.answer_photo(photo=poster_url, caption=message_text, parse_mode="html")
        else:
            logger.error("В данных о фильме отсутствуют некоторые необходимые ключи")
            await query.message.answer("Извините, некоторые необходимые данные о фильме отсутствуют.")
    else:
        logger.error("Данные о фильме отсутствуют или не содержат ключ 'data'")
        await query.message.answer("Извините, информация о фильме не найдена.")

