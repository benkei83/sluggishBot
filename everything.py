import requests
import bs4
import lxml
import pandas as pd
from datetime import datetime
import os
import csv

os.makedirs('data', exist_ok=True)

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
    time = datetime.now()
    try:
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, features='lxml')
        # heroes = soup.find_all(
        #     "select", attrs={"data-js": "career-select"})[1].select('select > option')
        quickplay_soup = soup.find('div', attrs={'id': 'quickplay'})
        competitive_soup = soup.find('div', attrs={'id': 'competitive'})
        modes = [quickplay_soup, competitive_soup]
        mode_names = ['Quickplay', 'Competitive']
        for mode in range(len(modes)):
            mode_index = 1 + (mode * 2)
            heroes = soup.find_all("select", attrs={
                                   "data-js": "career-select"})[mode_index].select('select > option')
            stats_soup = modes[mode].find_all(
                "div", attrs={"data-group-id": "stats"})
            for i in range(len(heroes)):
                stats = stats_soup[i].find_all(
                    "tr", attrs={"class": "DataTable-tableRow"})
                for stat in stats:
                    cols = stat.select('td')
                    title, value = cols[0].text, cols[1].text
                    if ":" in value:
                        tmp = value.split(":")
                        value = int(tmp[0])*60 + int(tmp[1])
                    elif "%" in value:
                        value = int(value.replace('%', '')) / 100
                    print(time, mode_names[mode], nick,
                          heroes[i].text, title, value)
                    # alle_stats.append(
                    #     [time, nick, heroes[i].text, title, value])
                    with open('data/stats.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            [time, mode_names[mode], nick, heroes[i].text, title, value])
    except Exception as e:
        print(str(e))
        continue
