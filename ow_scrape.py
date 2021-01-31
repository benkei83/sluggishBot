import requests
import bs4
import lxml

profile = "https://playoverwatch.com/en-us/career/nintendo-switch/kidneypool-66b444e2ea860954c2d60b291d5b2891/"

res = requests.get(profile)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features='lxml')
# soup2 = soup.find("h5", text="Best").parent.parent.parent.parent
# best = soup2.find_all("tr", attrs={"class": "DataTable-tableRow"})

stats = soup.find_all("tr", attrs={"class": "DataTable-tableRow"})
tmp = soup.find_all("select", attrs={"data-js": "career-select"})[1]
heroes = tmp.select('select > option')

hero_list = []
for hero in heroes:
    hero_list.append(hero.text)

for i, v in enumerate(hero_list):
    print(i, v)

# b = []
# count = 0
# for stat in stats:
#     cols = stat.select('td')
#     title, value = cols[0].text, cols[1].text
#     print(f'{title}: {value}')
#     count += 1
# print(count)

# quickplay > section:nth-child(2) > div > div.flex-container\@md-min.m-bottom-items > div.flex-item\@md-min.m-grow.u-align-right > div > select
