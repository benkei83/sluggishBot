import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/stats.csv', encoding='unicode_escape')
# df = pd.DataFrame(alle_stats)
df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']

df['Time'] = pd.to_datetime(df['Time']).dt.date
test = df[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min")
          & (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")]
pivot = test.pivot(index='Time', columns='Nick', values='Value')
pivot.plot.line()
plt.xticks(df['Time'].unique())
plt.show()
