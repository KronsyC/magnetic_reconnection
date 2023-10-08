
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use("QtAgg")
# matplotlib.use
df = pd.read_csv("./plasma.csv")

print(df)
df.plot(x="time", y="plasma_temp")
# # plt.plot(df)
plt.show()
