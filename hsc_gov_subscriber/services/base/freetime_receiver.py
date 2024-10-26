import json
import random

from hsc_gov_subscriber.services.base.exceptions.no_time_available_exception import NoTimeAvailableException
from hsc_gov_subscriber.utils.client import Client
from hsc_gov_subscriber.utils.log import logger


class FreeTimeReceiver:
    @staticmethod
    async def get_first_freetime(chdate, question_id, office_id, x_csrf_token, client: Client):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,uk;q=0.9,en-US;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

        data = {
            'office_id': office_id,
            'date_of_admission': chdate,
            'question_id': question_id,
            'es_date': '',
            'es_time': '',
        }

        response = await client.post("https://eq.hsc.gov.ua/site/freetimes", data=data, headers=headers)
        logger.debug(response)

        freetime_json = json.loads(response["body"])
        logger.debug(f"freetime_json {freetime_json}")

        rows = freetime_json['rows']
        if len(rows) == 0:
            msg = "Нема вільного часу на дату '{}' для офісу '{}'".format(chdate, office_id)
            logger.error(msg)
            raise NoTimeAvailableException(msg)
        else:
            freetime_first = random.choice(rows)

        freetime_first_id = freetime_first['id']
        freetime_first_chtime = freetime_first['chtime']
        logger.debug(f"Вільний час: id - {freetime_first_id}, час - {freetime_first_chtime}")
        logger.info(f"Вільний час: {freetime_first_chtime}")

        return freetime_first_id, freetime_first_chtime
