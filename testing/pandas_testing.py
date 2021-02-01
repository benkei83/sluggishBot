import pandas as pd

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

fire = df.assign(ranking=df.loc[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay"), 'Value'].rank(ascending=False))[(df['Stat']
                                                                                                                                                                                     == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay")].loc[:, ['ranking', 'Nick', 'Value']].sort_values(by=['ranking'])


for index, row in fire.iterrows():
    print(int(row['ranking']), row['Nick'], int(row['Value']))

# df = df.assign(main=df.apply(main_apply, axis=1))

# print(df[(df['Stat'].str.contains('Avg')) & (df['main'] == True)].pivot(
#     index='Stat', columns='Nick', values='Value'))
