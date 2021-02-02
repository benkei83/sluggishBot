import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json
import bs4
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import random


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Environmental settings
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Discord settings
# client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Overwatch settings
profiler = {'slug#8001': 'https://playoverwatch.com/en-us/career/nintendo-switch/SK%3ASlug-2b9f80fe2f23386a731431e300bf9bb0/',
            'LarsErikO#9944': 'https://playoverwatch.com/en-us/career/nintendo-switch/Lasch-4a32b34ab766b78a5190ca06a107b170/',
            'myoung#9113': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:mag%20nes-87e9eb5985483a5ad21f8a93501b302f/',
            'Stiananan#6379': 'https://playoverwatch.com/en-us/career/nintendo-switch/Stiananan-ac85a3a5a3b29caf2fe2782380ff687f/',
            'kidneypool#5944': 'https://playoverwatch.com/en-us/career/nintendo-switch/kidneypool-66b444e2ea860954c2d60b291d5b2891/',
            'lundefugl#6477': 'https://playoverwatch.com/en-us/career/nintendo-switch/sk:biRd-575879571c4e49637754c4720a32ebcd/'}

# Wordcloud settings
stopwords = set()
stopwords.update(["e", "på", "å", "med", "det", "og", "om",
                  "til", "va", "en", "vi", "d", "så", "den"])


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


async def scrape_stats(ctx, stat, author, msg):
    if str(author) in profiler:
        profile = profiler[str(author)]
        res = requests.get(profile)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, features='lxml')
        soup2 = soup.find("h5", text=stat).parent.parent.parent.parent
        best = soup2.find_all("tr", attrs={"class": "DataTable-tableRow"})
        # msg = (
        #     f'__**Best stats for {str(author).split("#")[0]}**__')
        for i in best:
            cols = i.select('td')
            title, value = cols[0].text, cols[1].text
            msg = msg + (f'\n{title}: **{value}**')
        await ctx.send(msg)
    else:
        await ctx.send("Du har ikke registrert profil-URL.")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


# Bot commands

@bot.command(
    name="cloud",
    help="Lager ordsky"
)
async def ordsky(ctx):
    text = ''
    async for msg in ctx.history():
        text = text + msg.content + " "
    wordcloud = WordCloud(width=800, height=400,
                          stopwords=stopwords).generate(text)
    wordcloud.to_file("cloud.png")
    await ctx.send(file=discord.File('cloud.png'))


@bot.command(
    name='csv',
    help='Sender siste versjon av csv-fil, alle data.'
)
async def send_csv(ctx):
    await ctx.send(file=discord.File('data/stats.csv'))


@bot.command(
    name='quote',
    help='Skriver ut en random quote'
)
async def print_quote(ctx):
    quote = get_quote()
    await ctx.send(quote)


@bot.command(
    name='best',
    help='Viser beste stats for spiller. !best <nick#ID> (optional)'
)
async def best_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Best'
    msg = (f'__**Best stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='average',
    help='Viser gjennomsnitt-stats for spiller. !average <nick#ID> (optional)'
)
async def average_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Average'
    msg = (f'__**Average stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='combat',
    help='Viser combat-stats for spiller. !combat <nick#ID> (optional)'
)
async def combat_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Combat'
    msg = (f'__**Combat stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='game',
    help='Viser game-stats for spiller. !game <nick#ID> (optional)'
)
async def game_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Game'
    msg = (f'__**Game stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='assists',
    help='Viser assist-stats for spiller. !assists <nick#ID> (optional)'
)
async def assists_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Assists'
    msg = (f'__**Assist stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='medals',
    help='Viser medalje-stats for spiller. !medals <nick#ID> (optional)'
)
async def medals_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Match Awards'
    msg = (f'__**Medal stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='misc',
    help='Viser misc-stats for spiller. !misc <nick#ID> (optional)'
)
async def misc_stat(ctx, *arg):
    if len(arg) > 0:
        author = str(arg[0])
    else:
        author = ctx.author
    stat = 'Miscellaneous'
    msg = (f'__**Miscellaneous stats for {str(author).split("#")[0]}**__')
    await scrape_stats(ctx, stat, author, msg)


@bot.command(
    name='dmgrank',
    help='Rangerig med mest damage per 10 min i snitt'
)
async def dmg_rank(ctx):
    tmp = []
    for nick, url in profiler.items():
        try:
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, features='lxml')
            dmg = soup.select(
                'tr[data-stat-id="0x0860000000000386"] > td')[1].text
            tmp.append((int(dmg), nick))
        except:
            pass
    result = sorted(tmp, reverse=True)
    msg = '**__Ranking - All Damage Done - Avg per 10 Min__**'
    spot = 1
    for row in result:
        msg = msg + (f'\n{spot} - {row[1].split("#")[0]}: **{row[0]}**')
        spot += 1
    await ctx.send(msg)


@bot.command(
    name='firerank',
    help='Rangering med gjennomsnittlig tid on fire'
)
async def on_fire(ctx):
    df = pd.read_csv('data/stats.csv', encoding='unicode_escape')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    fire = df.assign(ranking=df.loc[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay"), 'Value'].rank(ascending=False))[
        (df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay")].loc[:, ['ranking', 'Nick', 'Value']].sort_values(by=['ranking'])
    msg = '**__Ranking - Time Spent on Fire - Avg per 10 Min__**\n'
    for index, row in fire.iterrows():
        msg = msg + \
            f"{int(row['ranking'])} - {row['Nick']}: **{int(row['Value'])}s**\n"
    await ctx.send(msg)


@bot.command(
    name='chart_test',
    help='test av matplotlib'
)
async def chart(ctx):
    df = pd.read_csv('data/stats.csv', encoding='unicode_escape')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    fire = df.assign(ranking=df.loc[(df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay"), 'Value'].rank(ascending=False))[
        (df['Stat'] == "Time Spent on Fire - Avg per 10 Min") & (df['Hero'] == "ALL HEROES") & (df['Mode'] == "Quickplay")].loc[:, ['ranking', 'Nick', 'Value']].sort_values(by=['ranking'])
    ax = fire.plot.bar(x='Nick', y='Value')
    ax.set_title("Time Spent on Fire - Avg per 10 Min")
    ax.set_ylabel('Seconds')
    ax.set_xlabel('')
    ax.get_legend().remove()
    ax.tick_params(axis='x', labelrotation=0)
    plt.savefig('test.png')
    await ctx.send(file=discord.File('test.png'))


@bot.command(
    name='bar',
    help='Lager rangering med barchart over en stat. !bar "<stat-navn>"'
)
async def barchart(ctx, *arg):

    df = pd.read_csv('data/stats.csv', encoding='unicode_escape')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    tmp = df[(df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")]
    kategorier = tmp['Stat'].unique().tolist()
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')
    if len(arg) > 0:
        kategori = str(arg[0])
        if kategori == 'list':
            msg = '```'
            for k in kategorier:
                msg = msg + k + "\n"
            msg += '```'
            await ctx.send(msg)
            return
    else:
        kategori = random.choice(kategorier)
        print(kategori)

    table = df[(df['Stat'] == kategori) &
               (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")].last('1H')
    table = table.sort_values(by=['Value'], ascending=False)
    ax = table.plot.bar(x='Nick', y='Value')
    ax.set_title(kategori)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.get_legend().remove()
    ax.tick_params(axis='x', labelrotation=0)
    plt.savefig('test.png')
    await ctx.send(file=discord.File('test.png'))


@ bot.command(
    name='healrank',
    help='Rangerig med mest healing per 10 min i snitt'
)
async def healing_rank(ctx):
    tmp = []
    for nick, url in profiler.items():
        try:
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, features='lxml')
            heal = soup.select(
                'tr[data-stat-id="0x08600000000004B2"] > td')[1].text
            tmp.append((int(heal), nick))
        except:
            pass
    result = sorted(tmp, reverse=True)
    msg = '**__Ranking - Healing Done - Avg per 10 Min__**'
    spot = 1
    for row in result:
        msg = msg + (f'\n{spot} - {row[1].split("#")[0]}: {row[0]}')
        spot += 1
    await ctx.send(msg)


@ bot.command(
    name='deathrank',
    help='Rangerig med mest deaths per 10 min i snitt'
)
async def death_rank(ctx):
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
    await ctx.send(msg)


@bot.command(
    name='main',
    help='Hero specific stats for main'
)
async def main_stats(ctx):
    if str(ctx.author) in profiler:
        profile = profiler[str(ctx.author)]
        nick = str(ctx.author).split("#")[0]
        res = requests.get(profile)
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
        msg = f'__**Hero specific stats with {main} for {nick}**__'
        main_soup = stats_soup[main_index].find(
            "h5", text="Hero Specific").parent.parent.parent.parent
        main_stats = main_soup.find_all(
            "tr", attrs={"class": "DataTable-tableRow"})
        for i in main_stats:
            cols = i.select('td')
            title, value = cols[0].text, cols[1].text
            msg = msg + (f'\n{title}: **{value}**')
        await ctx.send(msg)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))
