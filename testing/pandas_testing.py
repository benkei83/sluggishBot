import pandas as pd
import matplotlib.pyplot as plt
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

df = pd.read_csv('../data/stats.csv', encoding='unicode_escape')
# df = pd.DataFrame(alle_stats)
df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']


def main_apply(row):
    if (row['Nick'] == 'slug') & (row['Hero'] == 'Soldier: 76'):
        return True
    elif (row['Nick'] == 'kidneypool') & (row['Hero'] == 'Reinhardt'):
        return True
    elif (row['Nick'] == 'LarsErikO') & (row['Hero'] == 'Lúcio'):
        return True
    elif (row['Nick'] == 'myoung') & (row['Hero'] == 'Baptiste'):
        return True
    elif (row['Nick'] == 'Stiananan') & (row['Hero'] == 'Orisa'):
        return True
    else:
        return False


# fire = df.assign(ranking=df.loc[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES"), 'Value'].rank(ascending=False))[(df['Stat']
#                                                                                                                                                        == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES")].loc[:, ['ranking', 'Nick', 'Value']].sort_values(by=['ranking']).to_string(index=False, justify='left')
recent_date = df.groupby(['Nick', 'Hero'])['Time'].max()
# last = df[df['Time'] == recent_date]
# fire = last.assign(ranking=last.loc[(last['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (last['Hero'] == "ALL HEROES") & (last['Mode'] == "Quickplay"), 'Value'].rank(ascending=False))[(last['Stat']
#                                                                                                                                                                                                == "Time Spent on Fire - Avg per 10 Min") & (last['Hero'] == "ALL HEROES") & (last['Mode'] == "Quickplay")].loc[:, ['ranking', 'Nick', 'Value']].sort_values(by=['ranking'])


# for index, row in fire.iterrows():
#     print(int(row['ranking']), row['Nick'], int(row['Value']))

# ax = fire.plot.bar(x='Nick', y='Value')
# ax.set_title("ON FIRE!")
# ax.set_ylabel('Seconds')
# ax.tick_params(axis='x', labelrotation=0)
# plt.savefig('test.png')

# df = df.assign(main=df.apply(main_apply, axis=1))

# print(df[(df['Stat'].str.contains('Avg')) & (df['main'] == True)].pivot(
#     index='Stat', columns='Nick', values='Value'))

# print(fire)

# categories = df.Stat.unique()
# for category in categories:
#     print(type(category))

# print(recent_date)


# df['Time'] = pd.to_datetime(df['Time']).dt.date
# test = df[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min")
#           & (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")]
# pivot = test.pivot(index='Time', columns='Nick', values='Value')
# pivot.plot.line()
# plt.xticks(df['Time'].unique())
# plt.show()
# # print(pivot)


def main_apply(row):
    if (row['Nick'] == 'slug') & (row['Hero'] == 'Soldier: 76'):
        return True
    elif (row['Nick'] == 'kidneypool') & (row['Hero'] == 'Reinhardt'):
        return True
    elif (row['Nick'] == 'LarsErikO') & (row['Hero'] == 'Lúcio'):
        return True
    elif (row['Nick'] == 'myoung') & (row['Hero'] == 'Baptiste'):
        return True
    elif (row['Nick'] == 'Stiananan') & (row['Hero'] == 'Orisa'):
        return True
    else:
        return False


# df = df.assign(main=df.apply(main_apply, axis=1))

# pct = df[(df['Stat'] == 'Win Percentage') & (df['main'] == True)].Value.mean()
# print(pct)
df = df.assign(main=df.apply(main_apply, axis=1))
df['Time'] = pd.to_datetime(df['Time'])
df = df.set_index('Time')
tmp = df[((df['Stat'] == 'Time Played') | (df['Stat'] == 'Medals')) & (
    df['main'] == True)].last("2H")

tmp.plot(x='Nick', y='Value', kind='bar', secondary_y='Medals', rot=0)
plt.show()


# tmp = df[df['Hero'] == 'ALL HEROES']
# kategorier = tmp['Stat'].unique().tolist()
# table = df[(df['Stat'] == "Medals") &
#            (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")].last('2H')
# table2 = df[(df['Stat'] == "Time Played") & (
#     df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")].last('2H')
# table = table.sort_values(by=['Value'], ascending=False)
# # plt.figure()
# table.Value.plot.bar(x='Nick', y='Value')
# table2.Value.plot.bar(x='Nick', y='Value', secondary_y=True, style='g')
# plt.show()

# test = df.last((df['Stat'] == "Time Spent on Fire - Avg per 10 Min")
#                & (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay"))
# pivot = test.pivot(index='Nick', columns='Value')
# pivot.plot.bar()
# # plt.xticks(df['Time'].unique())
# plt.show()
# # print(pivot)
