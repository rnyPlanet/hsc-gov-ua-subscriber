import re
from datetime import datetime


class ChdateParser:
    def parse_chdate(self, text):
        matches = re.findall(r'📆 \d+\.\d+\.\d+ - \d+ 🎫 талон', text)
        dates = []
        for match in matches:
            date_str = re.search(r'\d+\.\d+\.\d+', match).group()
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            dates.append((date_str, date_obj))

        sorted_dates = sorted(dates, key=lambda x: x[1])
        first_date = sorted_dates[0][1].strftime('%Y-%m-%d')

        return first_date
