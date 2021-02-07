import pandas as pd
import matplotlib.pyplot as plt
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

df = pd.read_csv('../data/stats.csv', encoding='unicode_escape')
# df = pd.DataFrame(alle_stats)
df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
# df['Time'] = pd.to_datetime(df['Time']).dt.date

# slug = df[(df['Nick'] == 'LarsErikO') & (df['Stat'] == 'All Damage Done')
#           & (df['Mode'] == 'Quickplay')]
# slug.plot(x='Time')
# plt.xticks(df['Time'].unique())
# # plt.show()
# winrate = df[(df['Stat'] == 'Win Percentage') &
#              (df['main'] == True)].Value.mean()
# print(winrate)


def main_apply(row):
    if (row['Nick'] == 'slug') & (row['Hero'] == 'Soldier: 76'):
        return True
    elif (row['Nick'] == 'kidneypool') & (row['Hero'] == 'Reinhardt'):
        return True
    elif (row['Nick'] == 'LarsErikO') & (row['Hero'] == 'LÃºcio'):
        return True
    elif (row['Nick'] == 'myoung') & (row['Hero'] == 'Baptiste'):
        return True
    elif (row['Nick'] == 'Stiananan') & (row['Hero'] == 'Orisa'):
        return True
    elif (row['Nick'] == 'lundefugl') & (row['Hero'] == 'Bastion'):
        return True
    else:
        return False


df = df.assign(main=df.apply(main_apply, axis=1))
df['Time'] = pd.to_datetime(df['Time']).dt.date

tmp = df[(df['Stat'] == 'Win Percentage') & (df['main'] == True)
         ].pivot(index='Time', columns='Nick', values='Value')
tmp = tmp.assign(mean=round(tmp.mean(axis=1), 3))
tmp = tmp.reset_index()
tmp['Time'] = pd.to_datetime(tmp['Time'], errors='coerce')
tmp['Weekday'] = tmp.Time.dt.day_name()
# print(tmp)
to_plot = tmp[['Time', 'mean']]
to_plot.plot(x='Time')
plt.xticks(to_plot['Time'].unique())
plt.show()
