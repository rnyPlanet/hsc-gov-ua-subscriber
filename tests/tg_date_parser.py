import re
from datetime import datetime

text = """🎫 Знайдено талони 🏛️ ТСЦ МВС № 4841 м. Миколаїв, пров. Транспортний, 1а/1
💼 На послугу: 🚗 Практичний іспит (транспортний засіб навчального закладу)
✅ Талони наявні на наступні дати :
📆 2.5.2024 - 1 🎫 талон
📆 24.4.2024 - 1 🎫 талон 
📆 30.9.2024 - 1 🎫 талон 
"""
# matches = re.findall(r'📆 \d+\.\d+\.\d+ - \d+ 🎫 талон', text)

# dates = []
# for match in matches:
#     date_str = re.search(r'\d+\.\d+\.\d+', match).group()
#     date_obj = datetime.strptime(date_str, '%d.%m.%Y')
#     dates.append((date_str, date_obj))
#
# sorted_dates = sorted(dates, key=lambda x: x[1])
# first_date = sorted_dates[0][1].strftime('%Y-%m-%d')
# print(first_date)



pattern_service = r'💼 На послугу: 🚗 Практичний іспит \(транспортний засіб навчального закладу\)'
pattern_dates = r'📆 \d+\.\d+\.\d+ - \d+ 🎫 талон'

dates = []
service_match = re.search(pattern_service, text)
if service_match:
    service_line = service_match.group()
    matches_dates = re.findall(pattern_dates, text)
    print("Service Line:", service_line)
    for match in matches_dates:
        date_str = re.search(r'\d+\.\d+\.\d+', match).group()
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
        dates.append((date_str, date_obj))
else:
    print("Pattern not found.")


sorted_dates = sorted(dates, key=lambda x: x[1])
first_date = sorted_dates[0][1].strftime('%Y-%m-%d')
print(first_date)
