import json

from bs4 import BeautifulSoup

from hsc_gov_subscriber.utils.client import Client


class ReservechergaRedirectReceiver:
    def __init__(self, chdate, question_id, x_csrf_token, first_freetime_id, email, client: Client):
        self.__chdate = chdate
        self.__question_id = question_id
        self.__x_csrf_token = x_csrf_token
        self.__first_freetime_id = first_freetime_id
        self.__email = email
        self.__client: Client = client

    async def get_reservecherga_redirect(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybjBnn2JwFbBJj5R3',
            'Origin': 'https://eq.hsc.gov.ua',
            'Referer': f'https://eq.hsc.gov.ua/site/step2?chdate={self.__chdate}&question_id={self.__question_id}&id_es=',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'X-CSRF-Token': self.__x_csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        data = (
            f'------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; '
            f'name="question_id"\r\n\r\n{self.__question_id}\r\n------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; '
            f'name="id_chtime"\r\n\r\n{self.__first_freetime_id}\r\n------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; '
            f'name="vin"\r\n\r\n{self.__vin}\r\n------WebKitFormBoundaryP7oR9mbTO4pVYPmB\r\nContent-Disposition: form-data; '
            f'name="email"\r\n\r\n{self.__email}\r\n------WebKitFormBoundarybjBnn2JwFbBJj5R3--\r\n')

        response = await self.__client.post("https://eq.hsc.gov.ua/site/reservecherga", data=data, headers=headers)

        return response["headers"]['X-Redirect']

    async def get_data_from_reservecherga_redirect(self, redirect_url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Referer': f'https://eq.hsc.gov.ua/site/step2?chdate={self.__chdate}&question_id={self.__question_id}&id_es=',
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

        response = await self.__client.get(redirect_url, headers=headers)

        soup = BeautifulSoup(response["body"], 'lxml')
        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

        data_params = soup.select_one('a', {"class": "btn-hsc-green"})['data-params']
        value = json.loads(data_params)['value']

        return csrf_token, value
