import aiohttp
from typing import Optional, List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KinoPoiskAPI:
    BASE_URL = "https://api.kinopoisk.dev/"
    SEARCH_ENDPOINT = "v1.4/movie/search"

    def __init__(self, token: str):
        self.token = token
        self.results = []
        self.current_index = 0

    async def search_movies(self, query: str) -> Optional[List[Dict]]:
        self.results = []
        url = f"{self.BASE_URL}{self.SEARCH_ENDPOINT}"
        params = {"page": 1, "limit": 50, "query": query}
        headers = {"X-API-KEY": self.token}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    json_response = await response.json()
                    self.results = json_response["docs"]
                    logger.info(f"Получено {len(self.results)} результатов по запросу '{query}'")
                else:
                    logger.warning(f"Запрос к {url} вернул код статуса {response.status}")
        return self.results[self.current_index:self.current_index+10]
    
class KinoClubAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://kinoclub.dev/api/movies/"

    async def get_movie(self, kp_id):
        url = f"{self.base_url}{kp_id}"
        headers = {"Authorization": self.token}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
