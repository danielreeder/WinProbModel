import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mlb_batting = pd.read_csv('data/mlb_batting.csv')
print(mlb_batting)

plt.scatter(mlb_batting.BB, mlb_batting.OPS)

plt.show()