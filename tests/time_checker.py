from datetime import datetime


def is_time_before(time_to_check, reference_time):
    time_to_check = datetime.strptime(time_to_check, "%H:%M")
    reference_time = datetime.strptime(reference_time, "%H:%M")

    return time_to_check < reference_time


time_to_check = "11:24"
reference_time = "12:34"

if is_time_before(time_to_check, reference_time):
    print(f"{time_to_check} is before {reference_time}")
else:
    print(f"{time_to_check} is not before {reference_time}")
