import requests
import bs4

profiler = {'slug#8001': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/',
            'LarsErikO#9944': 'https://playoverwatch.com/en-us/career/nintendo-switch/Lasch-4a32b34ab766b78a5190ca06a107b170/',
            'myoung#9113': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:mag%20nes-87e9eb5985483a5ad21f8a93501b302f/',
            'Stiananan#6379': 'https://playoverwatch.com/en-us/career/nintendo-switch/Stiananan-ac85a3a5a3b29caf2fe2782380ff687f/',
            'kidneypool#5944': 'https://playoverwatch.com/en-us/career/nintendo-switch/kidneypool-66b444e2ea860954c2d60b291d5b2891/',
            'lundefugl#6477': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:biRd-575879571c4e49637754c4720a32ebcd/'}

tmp = []
for nick, url in profiler.items():
    try:
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, features='lxml')
        death = soup.select(
            'tr[data-stat-id="0x08600000000004C3"] > td')[1].text
        tmp.append((float(death), nick))
    except:
        pass
result = sorted(tmp, reverse=True)
msg = '**__Ranking - Deaths - Avg per 10 Min__**'
spot = 1
for row in result:
    msg = msg + (f'\n{spot} - {row[1].split("#")[0]}: {row[0]}')
    spot += 1
print(msg)
