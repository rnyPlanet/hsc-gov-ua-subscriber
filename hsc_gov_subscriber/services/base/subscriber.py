import re
from abc import abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from hsc_gov_subscriber.services.base.finisher import Finisher
from hsc_gov_subscriber.services.base.freetime_receiver import FreeTimeReceiver
from hsc_gov_subscriber.services.base.reservecherga_redirect_receiver import ReservechergaRedirectReceiver
from hsc_gov_subscriber.services.base.x_csrf_token_receiver import XCsrfTokenReceiver
from hsc_gov_subscriber.utils.client import Client
from hsc_gov_subscriber.utils.config import Config, cookies_file
from hsc_gov_subscriber.utils.log import logger


class HscGovSubscriberAbs:
    async def subscribe(self, text: str):
        logger.info(f"\n{text}\n")

        chdates = self._parse_chdates(text)
        logger.info(f"В наявності {chdates} дат.")

        for chdate in chdates:
            try:
                subscribe_successfully = await self._subscribe(chdate)
                if subscribe_successfully:
                    logger.info(f"Успішно записались на дату {chdate}")
                    break
            except Exception as e:
                logger.error(e)
                raise e

    async def _subscribe(self, chdate):
        self._check_date(chdate)
        logger.info(f"Працюємо з датою {chdate}")

        client: Client = Client(cookies_file)

        x_csrf_token = await self._get_x_csrf_token(chdate, client)

        first_freetime_id, first_freetime_chtime = await self._get_first_freetime(chdate, x_csrf_token, client)

        redirect_url, csrf_token, value = \
            await self._get_data_from_reservecherga(chdate, client, first_freetime_id, x_csrf_token)

        subscribe_successfully = await self._finish(redirect_url, csrf_token, value, client)
        return subscribe_successfully

    async def _get_x_csrf_token(self, chdate, client):
        return await XCsrfTokenReceiver.get_x_csrf_token(chdate, self.get_question_id(), self.get_sub_id(), client)

    async def _get_first_freetime(self, chdate, x_csrf_token, client):
        question_id = self.get_question_id()
        office_id_value = Config.OFFICE_ID.value
        return await FreeTimeReceiver.get_first_freetime(chdate, question_id, office_id_value, x_csrf_token, client)

    async def _get_data_from_reservecherga(self, chdate, client, first_freetime_id, x_csrf_token):
        question_id = Config.QUESTION_ID.value
        data = self.get_reservecherga_data(question_id, first_freetime_id)
        redirect_url, csrf_token, value = \
            await ReservechergaRedirectReceiver.get_data_from_reservecherga(chdate, question_id,
                                                                            x_csrf_token, data, client)
        return redirect_url, csrf_token, value

    async def _finish(self, redirect_url, csrf_token, value, client):
        response = await Finisher.finish(redirect_url, csrf_token, value, client)
        return self._is_subscribe_successfully(response['body'])

    @abstractmethod
    def get_question_id(self):
        pass

    @abstractmethod
    def get_sub_id(self):
        pass

    @abstractmethod
    def get_reservecherga_data(self, question_id, first_freetime_id):
        pass

    @classmethod
    def _parse_chdates(cls, text):
        matches = re.findall(r'📆 \d+\.\d+\.\d+ - \d+ 🎫 талон', text)
        dates = []
        for match in matches:
            date_str = re.search(r'\d+\.\d+\.\d+', match).group()
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            dates.append((date_str, date_obj))
        sorted_dates = sorted(dates, key=lambda x: x[1])

        return [date_obj.strftime('%Y-%m-%d') for _, date_obj in sorted_dates]

    @classmethod
    def _check_date(cls, date):
        if not cls._is_date_between(date, Config.START_DATE.value, Config.END_DATE.value):
            raise Exception(f"{date} не знаходиться між {Config.START_DATE.value} та {Config.END_DATE.value}")

    @classmethod
    def _is_date_between(cls, date_to_check, start_date, end_date):
        date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        return start_date <= date_to_check <= end_date

    @classmethod
    def _is_subscribe_successfully(cls, response_body):
        soup = BeautifulSoup(response_body, 'lxml')
        error_div = soup.find("div", {"id": "w0-error-0"})

        if not error_div:
            return True
        if error_div:
            raise Exception(error_div.text.strip())
