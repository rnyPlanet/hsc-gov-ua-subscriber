from subscriber.client import Client


class Finisher:
    def __init__(self, referer, csrf_token, value, client: Client):
        self.__referer = referer
        self.__csrf_token = csrf_token
        self.__value = value
        self.__client: Client = client

    async def finish(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://eq.hsc.gov.ua',
            'Referer': self.__referer,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        data = {
            '_csrf': self.__csrf_token,
            'value': self.__value,
        }

        return await self.__client.post("https://eq.hsc.gov.ua/site/finish", headers=headers, data=data)
