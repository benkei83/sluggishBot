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
import zipfile


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Environmental settings
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Discord settings
# client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True)

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


def main_apply(row):
    if (row['Nick'] == 'slug') & (row['Hero'] == 'Soldier: 76'):
        return True
    elif (row['Nick'] == 'kidneypool') & (row['Hero'] == 'Reinhardt'):
        return True
    elif (row['Nick'] == 'LarsErikO') & (row['Hero'] == 'LÃºcio'):
        return True
    elif (row['Nick'] == 'myoung') & (row['Hero'] == 'Baptiste'):
        return True
    elif (row['Nick'] == 'Stiananan') & (row['Hero'] == 'Orisa'):
        return True
    elif (row['Nick'] == 'lundefugl') & (row['Hero'] == 'Bastion'):
        return True
    else:
        return False


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
    with zipfile.ZipFile('data/stats.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write('data/stats.csv')
        zip.write('data/sr.csv')
    await ctx.send(file=discord.File('data/stats.zip'))


@bot.command(
    name='quote',
    help='Skriver ut en random quote'
)
async def print_quote(ctx):
    quote = get_quote()
    await ctx.send(quote)


@bot.command(
    name='sr',
    help='skriver ut sr i synkende rekkefølge'
)
async def get_sr(ctx):
    ranks = []
    for tag in profiler:
        url = profiler[tag]
        nick = tag.split("#")[0]
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, features='lxml')
            rank = soup.find(
                'div', attrs={"class": "competitive-rank-level"}).text
            ranks.append((rank, nick))
        except Exception as e:
            print(str(e))
            continue

    msg = ''
    for r in sorted(ranks, reverse=False):
        msg = msg + f'\n{r[1]}: {r[0]}'
    await ctx.send(msg)


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
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
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
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
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

    df = pd.read_csv('data/stats.csv', encoding='utf-8')
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


@bot.command(
    name='line',
    help='line help'
)
async def linechart(ctx, *arg):
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    tmp = df[(df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")]
    kategorier = tmp['Stat'].unique().tolist()
    df['Time'] = pd.to_datetime(df['Time']).dt.date
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
    test = df[(df['Stat'] == kategori)
              & (df['Hero'] == "ALL HEROES") & (df["Mode"] == "Quickplay")]
    pivot = test.pivot(index='Time', columns='Nick', values='Value')
    pivot.plot.line()
    plt.xticks(df['Time'].unique(), rotation=10)
    plt.title(kategori)
    plt.locator_params(nbins=7)
    plt.savefig('line.png')
    await ctx.send(file=discord.File('line.png'))


# @bot.command(
#     name='double',
#     help='double axis help'
# )
# async def double(ctx, *arg):
#     df = pd.read_csv('data/stats.csv', encoding='unicode_escape')
#     df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
#     df['Time'] = pd.to_datetime(df['Time'])
#     df = df.set_index('Time')
#     df = df.assign(main=df.apply(main_apply, axis=1))
#     tmp = df[(df['Hero'] == "ALL HEROES") & (
#         df["Mode"] == "Quickplay")]
#     kategorier = tmp['Stat'].unique().tolist()

#     if len(arg) > 1:
#         venstre, høyre = str(arg[0]), str(arg[1])
#     elif len(arg) == 1:
#         venstre, høyre = str(arg[0]), random.choice(kategorier)
#     else:
#         venstre, høyre = random.choice(kategorier), random.choice(kategorier)
#     # df = df.last("2H")
#     tmp = df[((df['Stat'] == høyre) | (df['Stat'] == venstre)) & (
#         df['main'] == True)].last("2H").pivot(index='Nick', columns='Stat', values='Value')
#     tmp.columns = [høyre, venstre]
#     _ = tmp.plot(kind='bar', secondary_y=venstre, rot=0)
#     plt.title(f'{venstre} vs {høyre}')
#     plt.savefig('double.png')
#     await ctx.send(file=discord.File('double.png'))


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


@bot.command(
    name='myline',
    help='linjediagram over tid for en stat'
)
async def my_line(ctx, *arg):
    profile = profiler[str(ctx.author)]
    nick = str(ctx.author).split("#")[0]
    res = requests.get(profile)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    main_hero = soup.find('div', attrs={'class': 'ProgressBar-title'}).text
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    # tmp = df[(df['Hero'] == main_hero) & (df["Mode"] == "Quickplay")]
    tmp = df[(df['Hero'] == main_hero)]
    kategorier = tmp['Stat'].unique().tolist()
    if len(arg) > 0:
        kategori = str(arg[0])
        if kategori == 'list':
            msg = '```'
            for k in kategorier:
                msg = msg + k + "\n"
            msg += '```'
            await ctx.send(msg)
            return
    if len(arg) > 1:
        main_hero = str(arg[1])
    if len(arg) == 0:
        kategori = random.choice(kategorier)
    hero_df = df[(df['Nick'] == nick) & (df['Stat'] == kategori) & (
        df['Mode'] == 'Quickplay') & (df['Hero'] == main_hero)]
    hero_df.plot(x='Time')
    plt.xticks(df['Time'].unique(), rotation='vertical')
    plt.title(f'{kategori} for {nick} med {main_hero}')
    plt.savefig('myline.png')
    await ctx.send(file=discord.File('myline.png'))


@bot.command(
    name='winrate',
    help='Line chart med team winrate. Sammenlagt for alle med main hero'
)
async def winrate_chart(ctx, *arg):
    mode = 'Quickplay'
    if arg and str(arg[0]).lower() == 'competitive':
        mode = 'Competitive'
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df = df.assign(main=df.apply(main_apply, axis=1))
    df['Time'] = pd.to_datetime(df['Time']).dt.date

    tmp = df[(df['Stat'] == 'Win Percentage') & (df['main'] == True) & (df['Mode'] == mode)
             ].pivot(index='Time', columns='Nick', values='Value')
    tmp = tmp.assign(mean=round(tmp.mean(axis=1), 3))
    tmp = tmp.reset_index()
    tmp['Time'] = pd.to_datetime(tmp['Time'], errors='coerce')
    tmp['Weekday'] = tmp.Time.dt.day_name()
    # print(tmp)
    to_plot = tmp[['Time', 'mean']]
    to_plot.plot(x='Time', legend=None)
    plt.xticks(to_plot['Time'].unique())
    plt.title('Gjennomsnitts winrate for laget totalt med main hero på ' + mode)
    plt.savefig('winrate.png')
    await ctx.send(file=discord.File('winrate.png'))


@bot.command(
    name='herocompare',
    help='Sammenlign to heroes for en stat. !herocompare <stat> <hero1> <hero2> <mode>'
)
async def compare_heroes(ctx, *arg):  # <stat> <hero1> <hero2> <mode>
    mode = 'Quickplay'
    if len(arg) > 3 and str(arg[3]).lower() == 'competitive':
        mode = 'Competitive'

    # hero1, hero2, stat = str(arg[0]), str(arg[1]), str(arg[2])
    nick = str(ctx.author).split("#")[0]
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    heroes = df[(df['Nick'] == nick) & (
        df['Mode'] == mode)].Hero.unique().tolist()
    hero1 = heroes.pop(random.randint(1, len(heroes)-1))
    hero2 = heroes.pop(random.randint(1, len(heroes)-1))
    stats = df[(df['Nick'] == nick) & (df['Mode'] == mode) & (
        df['Hero'].isin([hero1, hero2]))].Stat.unique().tolist()
    stat = random.choice(stats)
    if len(arg) > 0:
        stat = str(arg[0])
    if len(arg) > 1:
        hero1 = str(arg[1])
    if len(arg) > 2:
        hero2 = str(arg[2])
    # hero1df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero1) & (df['Stat'] == stat)]
    # hero2df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero2) & (df['Stat'] == stat)]
    herodf = df[(df['Nick'] == nick) & (df['Mode'] == mode) & (df['Hero'].isin([hero1, hero2])) & (
        df['Stat'] == stat)].pivot(index='Time', columns='Hero', values='Value')
    herodf.plot()
    plt.xticks(rotation='vertical')
    plt.title(f'{stat} - {hero1} vs {hero2} i {mode}')
    plt.savefig('herocompare.png')
    await ctx.send(file=discord.File('herocompare.png'))


@bot.command(
    name='statcompare',
    help='Sammenlign to stats for en hero. !statcompare <stat1> <stat2> <hero> <mode>'
)
async def compare_stats(ctx, *arg):  # <stat1> <stat2> <hero> <mode>
    mode = 'Quickplay'
    if len(arg) > 3 and str(arg[3]).lower() == 'competitive':
        mode = 'Competitive'
    profile = profiler[str(ctx.author)]
    nick = str(ctx.author).split("#")[0]
    res = requests.get(profile)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    hero = soup.find('div', attrs={'class': 'ProgressBar-title'}).text
    # hero1, hero2, stat = str(arg[0]), str(arg[1]), str(arg[2])

    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    # heroes = df[(df['Nick'] == nick) & (
    #     df['Mode'] == mode)].Hero.unique().tolist()
    if len(arg) > 2:
        hero = str(arg[2])
    stats = df[(df['Nick'] == nick) & (df['Mode'] == mode) & (
        df['Hero'] == hero)].Stat.unique().tolist()

    stat1 = stats.pop(random.randint(1, len(stats)-1))
    stat2 = stats.pop(random.randint(1, len(stats)-1))
    if len(arg) > 0:
        stat1 = str(arg[0])
    if len(arg) > 1:
        stat2 = str(arg[1])

    # stat1df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero) & (df['Stat'] == stat1)]
    # stat2df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero) & (df['Stat'] == stat2)]
    statplot = df[(df['Nick'] == nick) & (df['Mode'] == mode) & (df['Hero'] == hero) & (
        df['Stat'].isin([stat1, stat2]))].pivot(index='Time', columns='Stat', values='Value')
    statplot.plot()
    plt.xticks(rotation='vertical')
    plt.title(f'{hero} - {stat1} vs {stat2} i {mode}')
    plt.savefig('statcompare.png')
    await ctx.send(file=discord.File('statcompare.png'))


@bot.command(
    name='modecompare',
    help='Sammenligning mellom modes. !modecompare <stat> <hero>'
)
async def compare_mode(ctx, *arg):  # <stat> <hero>
    profile = profiler[str(ctx.author)]
    nick = str(ctx.author).split("#")[0]
    res = requests.get(profile)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    hero = soup.find('div', attrs={'class': 'ProgressBar-title'}).text

    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    if len(arg) > 1:
        hero = str(arg[1])
    stats = df[(df['Nick'] == nick) & (
        df['Hero'] == hero)].Stat.unique().tolist()

    stat = random.choice(stats)
    if len(arg) > 0:
        stat = str(arg[0])
    # stat1df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero) & (df['Stat'] == stat1)]
    # stat2df = df[(df['Nick'] == nick) & (df['Mode'] == mode) &
    #              (df['Hero'] == hero) & (df['Stat'] == stat2)]
    modeplot = df[(df['Nick'] == nick) & (df['Mode'].isin(['Quickplay', 'Competitive'])) & (df['Hero'] == hero) & (
        df['Stat'] == stat)].pivot(index='Time', columns='Mode', values='Value')
    modeplot.plot()
    plt.xticks(rotation='vertical')
    plt.title(f'{hero} - {stat}')
    plt.savefig('modecompare.png')
    await ctx.send(file=discord.File('modecompare.png'))


@bot.command(
    name='herotime',
    help='Viser tid brukt med hver hero'
)
async def hero_time(ctx):
    nick = str(ctx.author).split("#")[0]
    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    herotime = df[(df['Nick'] == nick) & (df['Stat'] == 'Time Played') & (df['Time'] == df.Time.max()) & (
        df['Hero'] != 'ALL HEROES')]
    pd.options.mode.chained_assignment = None
    herotime['Value'] = herotime['Value'].div(3600)
    herotime_pivot = herotime.pivot(
        index='Hero', columns='Mode', values='Value').sort_values(by='Quickplay')
    height = len(herotime['Hero'].unique()) / 1.3
    herotime_pivot.plot(kind='barh', figsize=(8, height)).grid(axis='x')
    plt.title(f'Tid per hero')
    plt.legend(loc='lower right')
    plt.savefig('herotime.png')
    await ctx.send(file=discord.File('herotime.png'))


@bot.command(
    name='dailyrate',
    help='!dailyrate <stat1> <stat2> <hero> <mode>. stat1/stat2 per dag.'
)
async def daily_rate(ctx, *arg):  # <stat1> / < stat2 > <hero > <mode >
    profile = profiler[str(ctx.author)]
    nick = str(ctx.author).split("#")[0]
    res = requests.get(profile)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    hero = soup.find('div', attrs={'class': 'ProgressBar-title'}).text

    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    if len(arg) > 2:
        hero = str(arg[2])
    stats = df[(df['Nick'] == nick) & (
        df['Hero'] == hero)].Stat.unique().tolist()
    if len(arg) > 0:
        stat1 = str(arg[0])
    if len(arg) > 1:
        stat2 = str(arg[1])
    mode = 'Quickplay'
    if len(arg) > 3 and str(arg[3]).lower() == 'competitive':
        mode = 'Competitive'

    tmp = df[(df['Nick'] == nick) & (df['Mode'] == mode) & (df['Hero'] == hero) & (
        df['Stat'].isin([stat1, stat2]))].pivot(index='Time', columns='Stat', values='Value')
    tmp['Diff1'] = tmp[stat1].diff()
    tmp['Diff2'] = tmp[stat2].diff()
    tmp['Rate'] = tmp['Diff1']/tmp['Diff2']
    plt.clf()
    tmp['Rate'].plot.bar()
    plt.xticks(rotation=90)
    plt.title(f'Daily rate - {hero} - {stat1}/{stat2}')
    plt.savefig('dailyrate.png')
    await ctx.send(file=discord.File('dailyrate.png'))


@bot.command(
    name='statlist',
    help='!statlist <hero>. Lister tilgjengelige stats med en hero. Mest spilte hero er default.'
)
async def statlist(ctx, *arg):  # <hero>
    profile = profiler[str(ctx.author)]
    nick = str(ctx.author).split("#")[0]
    res = requests.get(profile)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    hero = soup.find('div', attrs={'class': 'ProgressBar-title'}).text

    df = pd.read_csv('data/stats.csv', encoding='utf-8')
    df.columns = ['Time', 'Mode', 'Nick', 'Hero', 'Stat', 'Value']
    df['Time'] = pd.to_datetime(df['Time']).dt.date

    if len(arg) > 0:
        hero = str(arg[0])

    stats = sorted(df[(df['Nick'] == nick) & (
        df['Hero'] == hero)].Stat.unique().tolist())
    msg = f'```--- {hero} ---\n'
    for k in stats:
        msg = msg + k + "\n"
    msg += '```'
    await ctx.send(msg)


# @bot.command(
#     name='teamsr',
#     help='Viser graf for SR over tid'
# )
# async def sr_plot(ctx):
#     df = pd.read_csv('data/sr.csv', encoding='utf-8', header=None)
#     df.columns = ['Time', 'Nick', 'Class', 'Rating']
#     df['Time'] = pd.to_datetime(df['Time']).dt.date
#     df.set_index('Time')
#     df_pivot = df.pivot(index='Time', columns=[
#                         'Nick', 'Class'], values='Rating')
#     df_pivot.plot(figsize=(14, 9), xticks=df['Time'].unique()).grid(axis='y')
#     plt.title(f'Skill Rating')
#     plt.legend(loc='lower left')
#     plt.savefig('teamsr.png')
#     await ctx.send(file=discord.File('teamsr.png'))

@bot.command(
    name='teamsr',
    help='Viser graf for SR over tid'
)
async def sr_plot(ctx):
    df = pd.read_csv('data/sr.csv', encoding='utf-8', header=None)
    df.columns = ['Time', 'Nick', 'Class', 'Rating']
    df['Time'] = pd.to_datetime(df['Time']).dt.date
    # df.set_index('Time')
    df['Nick_Class'] = df['Nick'] + " " + df['Class']

    date_range = pd.DataFrame(pd.date_range(
        min(df['Time']), max(df['Time']), freq='d'))
    date_range.columns = ['Time']
    date_range['Time'] = date_range['Time'].dt.date

    df_pivot = df.pivot(index='Time', columns='Nick_Class',
                        values='Rating')
    df_graph = date_range.merge(df_pivot, on='Time', how='left')
    df_graph.fillna(method='ffill')
    ax = df_graph.set_index('Time').fillna(method='ffill').plot(
        figsize=(14, 9), rot=90, xticks=df_graph['Time'])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.title(f'Skill Rating')
    plt.grid(axis='y')
    plt.savefig('teamsr.png', bbox_inches='tight')
    await ctx.send(file=discord.File('teamsr.png'))


@ bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))
