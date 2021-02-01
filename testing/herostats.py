import requests
import bs4
import lxml

profiler = {'slug#8001': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/',
            'LarsErikO#9944': 'https://playoverwatch.com/en-us/career/nintendo-switch/Lasch-4a32b34ab766b78a5190ca06a107b170/',
            'myoung#9113': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:mag%20nes-87e9eb5985483a5ad21f8a93501b302f/',
            'Stiananan#6379': 'https://playoverwatch.com/en-us/career/nintendo-switch/Stiananan-ac85a3a5a3b29caf2fe2782380ff687f/',
            'kidneypool#5944': 'https://playoverwatch.com/en-us/career/nintendo-switch/kidneypool-66b444e2ea860954c2d60b291d5b2891/',
            'lundefugl#6477': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:biRd-575879571c4e49637754c4720a32ebcd/'}

url = profiler['slug#8001']

res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features='lxml')
main = soup.find('div', attrs={'class': 'ProgressBar-title'}).text
heroes = [hero.text for hero in soup.find_all(
    "select", attrs={"data-js": "career-select"})[1].select('select > option')]
# print(heroes)
main_index = heroes.index(main)
# print(main_index)
quickplay_soup = soup.find('div', attrs={'id': 'quickplay'})
stats_soup = quickplay_soup.find_all(
    "div", attrs={"data-group-id": "stats"})
print(len(stats_soup))
msg = ''
main_soup = stats_soup[main_index].find(
    "h5", text="Hero Specific").parent.parent.parent.parent
main_stats = main_soup.find_all(
    "tr", attrs={"class": "DataTable-tableRow"})
for i in main_stats:
    cols = i.select('td')
    title, value = cols[0].text, cols[1].text
    msg = msg + (f'\n{title}: **{value}**')
print(msg)
