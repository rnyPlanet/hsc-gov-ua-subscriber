import json

from subscriber.client import Client


class FreeTimeReceiver:
    def __init__(self, chdate, question_id, office_id, x_csrf_token, client: Client):
        self.__chdate = chdate
        self.__question_id = question_id
        self.__office_id = office_id
        self.__x_csrf_token = x_csrf_token
        self.__client: Client = client

    async def get_first_freetime(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

        data = {
            'office_id': self.__office_id,
            'date_of_admission': self.__chdate,
            'question_id': self.__question_id,
            'es_date': '',
            'es_time': '',
        }

        response = await self.__client.post("https://eq.hsc.gov.ua/site/freetimes", data=data, headers=headers)

        freetime_json = json.loads(response["body"])

        freetime_first = freetime_json['rows'][0]
        freetime_first_id = freetime_first['id']
        freetime_first_chtime = freetime_first['chtime']

        return freetime_first_id, freetime_first_chtime
