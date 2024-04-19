import os
import json
import asyncio

import urllib.parse
import aiohttp


class APIManager:
    def __init__(self):
        self.login = os.getenv("API_LOGIN")
        self.token = os.getenv("API_TOKEN")

        self.base_address = os.getenv("API_ADDRESS")


        print("Logged in as:", self.login)

    def get_default_context(self, task: str) -> dict:
        context = {
            "login": self.login,
            "token": self.token,
            "task": task
        }
        return context

    def create_url(self, path: str, **kwargs) -> str:
        return "https://" + self.base_address + '/' + path + '?' + urllib.parse.urlencode(kwargs)

    async def get_games(self) -> list:
        async with aiohttp.ClientSession() as session:
            context = self.get_default_context("predata")
            context["sport"] = "esport"
            context["day"] = "20240420" # today

            url = self.create_url("api/get.php/", **context)

            async with session.get(url) as resp:
                result = await resp.json()

                if resp.status == 200:
                    games = result["games_pre"]
                    for game in games:
                        game["date"] = result["date_games"]
                    return games
                return []

    async def get_game_info(self, session: aiohttp.ClientSession, game: dict):
        game_id = game["game_id"]

        context = self.get_default_context(task="allodds")
        context["game_id"] = game_id
        url = self.create_url(path="api/get.php/", **context)

        async with session.get(url) as resp:
            if resp.status == 200:
                res = await resp.json()
                res["status"] = resp.status
                return game | res
            else:
                res = {"status": resp.status}
                return game | res

    async def get_games_info(self, data: list):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for el in data:
                task = asyncio.create_task(self.get_game_info(session, game=el))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            return result

    def get_data(self, use_net: bool = False, debug: bool = False):
        if use_net:
            games = asyncio.run(self.get_games())
        #     with open("temp/get_games.json", 'r') as file:
        #         json.dump(games, file, indent=4)
        #
            games_info = asyncio.run(self.get_games_info(games))
        #     with open("temp/get_games_info.json", 'w') as file:
        #         json.dump(games_info, file, indent=4)

        if not use_net:
            print(os.getcwd())

            with open("temp/get_games.json", 'r') as file:
                games = json.load(file)
            with open("temp/get_games_info.json", 'r') as file:
                games_info = json.load(file)

        if debug:
            print(len(games_info), games_info)

        return games_info
