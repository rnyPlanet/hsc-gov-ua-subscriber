from datetime import datetime


def is_date_between(date_to_check, start_date, end_date):
    date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    return start_date <= date_to_check <= end_date


dates_to_check = ["2024-04-24", "2024-05-01", "2024-05-10", "2024-04-22"]
start_date = "2024-04-22"
end_date = "2024-05-04"

for date in dates_to_check:
    if is_date_between(date, start_date, end_date):
        print(f"{date} is between {start_date} and {end_date}")
    else:
        print(f"{date} is not between {start_date} and {end_date}")


def is_date_between(date_to_check, start_date, end_date):
    date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    return start_date <= date_to_check <= end_date


date_to_check = "2024-05-03"
start_date = "2024-04-30"
end_date = "2024-05-04"

if is_date_between(date_to_check, start_date, end_date):
    print(f"{date_to_check} is between {start_date} and {end_date}")
else:
    print(f"{date_to_check} is not between {start_date} and {end_date}")
