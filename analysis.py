import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use("QtAgg")
# matplotlib.use
df = pd.read_csv("./big_set.csv")

print(df)
df.plot(x="time", y=" speed")
# plt.plot(df)
plt.show()
