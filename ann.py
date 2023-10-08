from matplotlib import figure
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats
import numpy as np

from datetime import datetime, timedelta

def day_to_date(day_number, year):
    date_format = '%Y-%m-%d'
    # create a datetime object for January 1st of the given year
    start_date = datetime(year, 1, 1)
    # add the number of days to the start date
    result_date = start_date + timedelta(days=day_number-1)
    # format the date string using the specified format
    return result_date.strftime(date_format)
RECONNECT_THRESHOLD = 75000
MERGE_THRESHOLD = 0.01
FIELD_DENSITY_WEIGHT = -1 
PLASMA_TEMP_WEIGHT = 1 
SPEED_WEIGHT = 1 
PROTON_DENSITY_WEIGHT = 0.1

matplotlib.use("QtAgg")
plt.style.use("ggplot")
# matplotlib.use

# fig, ax = plt.subplots()
df1 = pd.read_csv("./data/big_set.csv")
df2 = pd.read_csv("./data/plasma.csv")

# df2.drop("timed")
del df2["time"]
del df2["day"]
del df2["hour"]
del df2["minute"]
del df2["year"]
del df1["field_density"]
df = pd.concat([df1, df2], axis=1)

df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]

df_premod = df.copy() 

field_densities = df["field_density"].to_numpy()
plasma_temps = df["plasma_temp"].to_numpy()
speeds = df["speed"].to_numpy()
proton_densities = df["proton_density"].to_numpy()

# Square some fields to exaggerate jumps
# plasma_temps **= 2 
# speeds **= 2
# proton_densities **= 2


# Apply weights to each field
field_densities *= FIELD_DENSITY_WEIGHT 
plasma_temps *= PLASMA_TEMP_WEIGHT
speeds *= SPEED_WEIGHT
proton_densities *= PROTON_DENSITY_WEIGHT

nets = field_densities + plasma_temps + speeds + proton_densities

net_df = pd.DataFrame({"time" : df["time"], "year" : df["year"], "day" : df["day"], "hour" : df["hour"], "value" : nets})

# Aply the thresholding filter
net_df = net_df[net_df["value"] > RECONNECT_THRESHOLD].dropna()



net_df["time_diff"] = net_df["time"].diff()
net_df["group"] = (net_df["time_diff"] > MERGE_THRESHOLD).cumsum()
print(net_df)

result_df = net_df.groupby('group').agg({
    'time': 'first',  # Take the first timestamp in each group
    'value': 'mean',  # Calculate the mean of numeric_column1
    "day" : "first",
    "hour" : "first",
    "year" : "first"
    # 'numeric_column2': 'mean',  # Calculate the mean of numeric_column2
    # Add more columns as needed
}).reset_index(drop=True)


reconnect_dates = []

for idx in result_df.index:
    year = int(result_df["year"][idx])
    day = int(result_df["day"][idx])
    hour = int(result_df["hour"][idx])

    date = day_to_date(day, year)
    reconnect_dates.append(date)

print("Magnetic Reconnection Is Expected to have happened in the following dates:")
for d in reconnect_dates:
    print("\t", d)


t = df["time"]
f1 = plt.figure()
plt.bar(net_df["time"], net_df["value"], 0.01)
plt.savefig("plots/suspected reconnects.png")
# plt.plot(net_df["time"], net_df["value"])
plt.title("Suspected Magnetic Reconnection Points")
f2 = plt.figure()
plt.title("Magnetic Field Densities over time")
plt.plot(t, df_premod["field_density"])
plt.savefig("plots/field density.png")


plt.figure()
plt.title("Plasma Temperatures over time")
plt.plot(t, df_premod["plasma_temp"])
plt.savefig("plots/plasma temps.png")


plt.figure()
plt.title("Proton Densities over time")
plt.plot(t, df_premod["proton_density"])
plt.savefig("plots/proton densities.png"
            )
plt.figure()
plt.title("Ion Speeds over time")
plt.plot(t, df_premod["speed"])
plt.savefig("plots/ion speeds.png")
