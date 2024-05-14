import logging
from datetime import datetime

import colorlog
from bs4 import BeautifulSoup

from subscriber.client import Client
from subscriber.configs import QUESTION_ID, OFFICE_ID, EMAIL, START_DATE, END_DATE
from subscriber.services.chdate_parser import ChdateParser
from subscriber.services.finisher import Finisher
from subscriber.services.freetime_receiver import FreeTimeReceiver
from subscriber.services.reservecherga_redirect_receiver import ReservechergaRedirectReceiver
from subscriber.services.x_csrf_token_receiver import XCsrfTokenReceiver

logger = logging.getLogger('custom_logger')
logger.setLevel(logging.DEBUG)
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s %(levelname)s: %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class HscGovSubscriber:
    async def subscribe(self, text):
        client: Client = Client("cookies.json")

        chdate = ChdateParser().parse_chdate(text)
        logger.info(f"Parsed chdate: {chdate}")
        self.check_date(chdate)

        x_csrf_token = await XCsrfTokenReceiver(chdate, QUESTION_ID, client).get_x_csrf_token()
        logger.info(f"x_csrf token: {x_csrf_token}")

        first_freetime_id, first_freetime_chtime = await FreeTimeReceiver(chdate, QUESTION_ID, OFFICE_ID, x_csrf_token,
                                                                          client).get_first_freetime()
        logger.info(f"freetime first: {first_freetime_id} {first_freetime_chtime}")

        reservecherga_redirect_receiver = ReservechergaRedirectReceiver(chdate, QUESTION_ID, x_csrf_token,
                                                                        first_freetime_id, EMAIL, client)
        reservecherga_redirect_url = await reservecherga_redirect_receiver.get_reservecherga_redirect()
        logger.info(f"step3 reservecherga redirect url: {reservecherga_redirect_url}")

        csrf_token, value = await reservecherga_redirect_receiver.get_data_from_reservecherga_redirect(
            reservecherga_redirect_url)
        logger.info(f"step3 csrf_token: {csrf_token}")
        logger.info(f"step3 value: {value}")

        response = await Finisher(reservecherga_redirect_url, csrf_token, value, client).finish()
        response_body = response['body']
        logger.info(f"finish: {response_body}")
        self.validate(response_body)

    def check_date(self, date):
        if self.is_date_between(date, START_DATE, END_DATE):
            logger.info(f"{date} is between {START_DATE} and {END_DATE}")
        else:
            raise Exception(f"{date} is not between {START_DATE} and {END_DATE}")

    def is_date_between(self, date_to_check, start_date, end_date):
        date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        return start_date <= date_to_check <= end_date

    def validate(self, response_body):
        soup = BeautifulSoup(response_body, 'lxml')
        error_div = soup.find("div", {"id": "w0-error-0"}).text.strip()

        if "більше 4 разів" in error_div:
            raise Exception(error_div)
        else:
            for _ in 20:
                logger.info(f"success")
