import matplotlib.pyplot as plt
import pandas as pd

from notifications_stat.times import times

df = pd.DataFrame({"Time": times})

df["Time"] = pd.to_datetime(df["Time"])

df["DayOfWeek"] = df["Time"].dt.day_name()
df["Hour"] = df["Time"].dt.hour

grouped = df.groupby(["DayOfWeek", "Hour"]).size().reset_index(name="Count")

average_count_by_day_hour = grouped.groupby(["DayOfWeek", "Hour"])["Count"].mean().reset_index(name="AverageCount")

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for day in days_of_week:
    plt.figure(figsize=(8, 5))
    data = average_count_by_day_hour[average_count_by_day_hour["DayOfWeek"] == day]
    plt.plot(data["Hour"], data["AverageCount"], label=day)
    plt.xlabel("Hour")
    plt.ylabel("Average Count")
    plt.title(f"Average Counts by Hour - {day}")
    plt.legend()
    plt.grid(True)
    plt.xticks(range(24))
    plt.show()