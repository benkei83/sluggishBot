import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json
import bs4
from wordcloud import WordCloud

# Environmental settings
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Discord settings
client = discord.Client()
bot = commands.Bot(command_prefix='$')

# Overwatch settings
profiler = {'slug#8001': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/',
            'LarsErikO#9944': 'https://playoverwatch.com/en-us/career/nintendo-switch/Lasch-4a32b34ab766b78a5190ca06a107b170/', 'myoung#9113': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:mag%20nes-87e9eb5985483a5ad21f8a93501b302f/', 'Stiananan#6379': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK:Stianan-ac85a3a5a3b29caf2fe2782380ff687f/'}

# Wordcloud settings
stopwords = set()
stopwords.update(["e", "på", "å", "med", "det", "og", "om",
                  "til", "va", "en", "vi", "d", "så", "den"])


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        nick = str(message.author).split('#')[0]
        await message.channel.send(f"Hei, {nick}!")

    if message.content.startswith("$quote"):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith("$test"):
        async for msg in message.channel.history(limit=10000):
            await message.channel.send(msg.author.name)

    if message.content.startswith("$dmg"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            dmg = soup.select(
                'tr[data-stat-id="0x08600000000004B8"] > td')[1].text
            msg = f"{str(message.author).split('#')[0]} - Hero damage done: {dmg}"
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$cloud"):
        text = ''
        async for msg in message.channel.history():
            text = text + msg.content + " "
        wordcloud = WordCloud(width=800, height=400,
                              stopwords=stopwords).generate(text)
        wordcloud.to_file("cloud.png")

        await message.channel.send(file=discord.File('cloud.png'))

    if message.content.startswith("$best"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find("h5", text="Best").parent.parent.parent.parent
            best = soup2.find_all("tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Best stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$average"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find(
                "h5", text="Average").parent.parent.parent.parent
            best = soup2.find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Average stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$game"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find(
                "h5", text="Game").parent.parent.parent.parent
            best = soup2.find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Game stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$assists"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find(
                "h5", text="Assists").parent.parent.parent.parent
            best = soup2.find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Assist stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$medals"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find(
                "h5", text="Match Awards").parent.parent.parent.parent
            best = soup2.find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Medal stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")

    if message.content.startswith("$combat"):
        if str(message.author) in profiler:
            profile = profiler[str(message.author)]
            res = requests.get(profile)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features='lxml')
            soup2 = soup.find(
                "h5", text="Combat").parent.parent.parent.parent
            best = soup2.find_all(
                "tr", attrs={"class": "DataTable-tableRow"})
            msg = (
                f'__**Combat stats for {str(message.author).split("#")[0]}**__')
            for i in best:
                cols = i.select('td')
                title, value = cols[0].text, cols[1].text
                msg = msg + (f'\n{title}: **{value}**')
            await message.channel.send(msg)
        else:
            await message.channel.send("Du har ikke registrert profil-URL.")


client.run(os.getenv('TOKEN'))
# client.run('ODA0NDc4NjcxNTkwOTE2MTE5.YBM7JQ.OK-NrLnCKV5kZw0_3WsE1lgO3FI')
