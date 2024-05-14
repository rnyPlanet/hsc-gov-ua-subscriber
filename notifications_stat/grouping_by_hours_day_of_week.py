import matplotlib.pyplot as plt
import pandas as pd

from notifications_stat.times import times

df = pd.DataFrame({"Time": times})

df["Time"] = pd.to_datetime(df["Time"])

df["DayOfWeek"] = df["Time"].dt.dayofweek
df["Hour"] = df["Time"].dt.hour

grouped = df.groupby(["DayOfWeek", "Hour"]).size().reset_index(name="Count")

plt.figure(figsize=(10, 6))

for index, row in grouped.iterrows():
    plt.text(row["Hour"], row["DayOfWeek"], row["Count"], ha="center", va="center", color="black", fontsize=10)

plt.xlim(-0.5, 23.5)
plt.ylim(-0.5, 6.5)
plt.xlabel("Hour")
plt.ylabel("Day of Week")
plt.title("Grouped Data by Time and Day of Week")
plt.xticks(range(24))
plt.yticks(range(7), ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()
