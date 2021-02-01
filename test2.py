import requests
import bs4
import lxml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

profiler = {'slug#8001': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/',
            'LarsErikO#9944': 'https://playoverwatch.com/en-us/career/nintendo-switch/Lasch-4a32b34ab766b78a5190ca06a107b170/',
            'myoung#9113': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:mag%20nes-87e9eb5985483a5ad21f8a93501b302f/',
            'Stiananan#6379': 'https://playoverwatch.com/en-us/career/nintendo-switch/Stiananan-ac85a3a5a3b29caf2fe2782380ff687f/',
            'kidneypool#5944': 'https://playoverwatch.com/en-us/career/nintendo-switch/kidneypool-66b444e2ea860954c2d60b291d5b2891/',
            'lundefugl#6477': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:biRd-575879571c4e49637754c4720a32ebcd/'}

alle_stats = []
for tag in profiler:
    url = profiler[tag]
    nick = tag.split("#")[0]
    try:
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, features='lxml')
        heroes = soup.find_all(
            "select", attrs={"data-js": "career-select"})[1].select('select > option')
        quickplay_soup = soup.find('div', attrs={'id': 'quickplay'})
        stats_soup = quickplay_soup.find_all(
            "div", attrs={"data-group-id": "stats"})
        for i in range(len(stats_soup)):
            stats = stats_soup[i].find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            for stat in stats:
                cols = stat.select('td')
                title, value = cols[0].text, cols[1].text
                alle_stats.append([nick, heroes[i].text, title, value])
    except:
        continue

df = pd.DataFrame(alle_stats)
df.columns = ['Nick', 'Hero', 'Stat', 'Value']


tmp = df[(df.Stat == "All Damage Done - Most in Game")
         & (df.Hero == "ALL HEROES")]

tmp['Value'] = tmp['Value'].astype(float)

tmp[(df.Stat == "All Damage Done - Most in Game") &
    (tmp.Hero == "ALL HEROES")].groupby('Nick').agg(np.mean)


plt.close("all")

plt.figure()

tmp[(df.Stat == "All Damage Done - Most in Game") & (tmp.Hero ==
                                                     "ALL HEROES")].groupby('Nick').agg(np.mean).plot(kind="bar")
