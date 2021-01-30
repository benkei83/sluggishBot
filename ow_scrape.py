import requests
import bs4
import lxml

profile = "https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/"

res = requests.get(profile)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features='lxml')
soup2 = soup.find("h5", text="Best").parent.parent.parent.parent
best = soup2.find_all("tr", attrs={"class": "DataTable-tableRow"})

b = []

for i in best:
    cols = i.select('td')
    title, value = cols[0].text, cols[1].text
    print(f'{title}: {value}')
