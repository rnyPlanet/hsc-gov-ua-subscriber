import json

import aiohttp


class Client:
    __cookies_dict = {}

    def __init__(self, path):
        self.__load_cookies(path)

    def __load_cookies(self, path):
        with open(path, 'r') as file:
            cookie_data = json.load(file)

        for key, value in cookie_data.items():
            self.__cookies_dict[key] = value

    async def get(self, link, headers, params=None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            response = await session.get(link, cookies=self.__cookies_dict, params=params, headers=headers)
            return await self.__buid_response(response)

    async def post(self, link, headers, data, params=None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            response = await session.post(link, cookies=self.__cookies_dict, params=params, headers=headers, data=data)
            return await self.__buid_response(response)

    async def __buid_response(self, response):
        status = response.status
        headers = response.headers
        body = await response.text()
        return {
            'status': status,
            'headers': dict(headers),
            'body': body
        }
