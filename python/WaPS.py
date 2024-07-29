import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

mlb_batting = pd.read_csv('data/mlb_batting.csv').query("PA > 300")

fig, ax = plt.subplots()

ax.set_xlabel("WaPS")
ax.set_ylabel("BB")
ax.set_title("OPS vs WaPS")
ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax.scatter(mlb_batting.WaPS, mlb_batting.BB)

plt.show()