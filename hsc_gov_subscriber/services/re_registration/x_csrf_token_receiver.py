from bs4 import BeautifulSoup

from hsc_gov_subscriber.utils.client import Client


class XCsrfTokenReceiver:
    def __init__(self, chdate, question_id, client: Client):
        self.__chdate = chdate
        self.__question_id = question_id
        self.__client: Client = client

    async def get_x_csrf_token(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Referer': f'https://eq.hsc.gov.ua/site/step1?value={self.__question_id}&subid=1',
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

        params = {
            'chdate': self.__chdate,
            'question_id': self.__question_id,
            'id_es': '',
        }

        response = await self.__client.get("https://eq.hsc.gov.ua/site/step2", params=params, headers=headers)

        soup = BeautifulSoup(response["body"], 'lxml')
        self.__validate_html(soup)

        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

        return csrf_token

    def __validate_html(self, soup):
        if len(soup(text=lambda t: "Увійти за допомогою - ID.GOV.UA" in t.text)) != 0:
            raise Exception("need update cookies")
