import json

from bs4 import BeautifulSoup

from hsc_gov_subscriber.utils.client import Client
from hsc_gov_subscriber.utils.log import logger


class ReservechergaRedirectReceiver:
    @staticmethod
    async def get_data_from_reservecherga(chdate, question_id, x_csrf_token, data, client: Client):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Referer': f'https://eq.hsc.gov.ua/site/step2?chdate={chdate}&question_id={question_id}&id_es=',
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

        redirect_url = await ReservechergaRedirectReceiver._get_reservecherga_redirect(chdate, question_id,
                                                                                       x_csrf_token, data, client)

        response = await client.get(redirect_url, headers=headers)
        logger.debug(response)

        soup = BeautifulSoup(response["body"], 'lxml')
        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

        data_params = soup.select_one('a', {"class": "btn-hsc-green"})['data-params']
        value = json.loads(data_params)['value']

        logger.debug(f"step3 redirect_url: {redirect_url}")
        logger.debug(f"step3 csrf_token: {csrf_token}")
        logger.debug(f"step3 value: {value}")

        return redirect_url, csrf_token, value

    @staticmethod
    async def _get_reservecherga_redirect(chdate, question_id, x_csrf_token, data, client: Client):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybjBnn2JwFbBJj5R3',
            'Origin': 'https://eq.hsc.gov.ua',
            'Referer': f'https://eq.hsc.gov.ua/site/step2?chdate={chdate}&question_id={question_id}&id_es=',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'X-CSRF-Token': x_csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        response = await client.post("https://eq.hsc.gov.ua/site/reservecherga", data=data, headers=headers)
        logger.debug(response)

        x_redirect = response["headers"]['X-Redirect']
        logger.debug(f"x_redirect: {x_redirect}")

        return x_redirect
