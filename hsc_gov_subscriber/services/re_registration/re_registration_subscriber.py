import logging
from datetime import datetime

import colorlog
from bs4 import BeautifulSoup

from hsc_gov_subscriber.services.practice.chdate_parser import ChdateParser
from hsc_gov_subscriber.services.practice.finisher import Finisher
from hsc_gov_subscriber.services.practice.freetime_receiver import FreeTimeReceiver
from hsc_gov_subscriber.services.practice.reservecherga_redirect_receiver import ReservechergaRedirectReceiver
from hsc_gov_subscriber.services.practice.x_csrf_token_receiver import XCsrfTokenReceiver
from hsc_gov_subscriber.services.subscriber import HscGovSubscriberAbs
from hsc_gov_subscriber.utils.client import Client
from hsc_gov_subscriber.utils.config import Config

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


class ReRegistrationSubscriber(HscGovSubscriberAbs):
    async def subscribe(self, text):
        client: Client = Client("cookies.json")

        chdate = ChdateParser().parse_chdate(text)
        logger.info(f"Parsed chdate: {chdate}")
        self.check_date(chdate)

        x_csrf_token = await XCsrfTokenReceiver(chdate, Config.QUESTION_ID.value, client).get_x_csrf_token()
        logger.info(f"x_csrf token: {x_csrf_token}")

        first_freetime_id, first_freetime_chtime = await FreeTimeReceiver(chdate, Config.QUESTION_ID.value, Config.OFFICE_ID.value,
                                                                          x_csrf_token,
                                                                          client).get_first_freetime()
        logger.info(f"freetime first: {first_freetime_id} {first_freetime_chtime}")

        reservecherga_redirect_receiver = ReservechergaRedirectReceiver(chdate, Config.QUESTION_ID.value, x_csrf_token,
                                                                        first_freetime_id, Config.EMAIL.value, client)
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
        if self.is_date_between(date, Config.START_DATE.value, Config.END_DATE.value):
            logger.info(f"{date} is between {Config.START_DATE.value} and {Config.END_DATE.value}")
        else:
            raise Exception(f"{date} is not between {Config.START_DATE.value} and {Config.END_DATE.value}")

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
