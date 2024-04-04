import aiohttp

class KinoPoiskAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.kinopoisk.dev/"
        self.current_page = 1
        self.last_query = None

    async def search_movies(self, query=None, page=None):
        if query is not None:
            self.last_query = query
        if page is not None:
            self.current_page = page
        url = f"{self.base_url}v1.4/movie/search"
        params = {"page": self.current_page, "limit": 10, "query": self.last_query}
        headers = {"X-API-KEY": self.token}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response["docs"]
                return None


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
