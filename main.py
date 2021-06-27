import discord
import os
from bs4 import BeautifulSoup
import requests

client = discord.Client()
my_secret = os.environ['TOKEN']
URL = 'https://www.volcanodiscovery.com/earthquakes/today.html'
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$earthquake'):
        table = soup.findChildren("table", attrs={"id": "qTable"})
        rows = table[0].findChildren('tr')
        cells = rows[2].find_all('td')
        location = cells[3].get_text()
        index = cells[1].get_text().find('.')
        depth = cells[1].get_text()[index + 2:]

        time = cells[0].get_text()
        mag = cells[1].findChildren('div')[0].get_text()

        if "(preliminary) Early Alert!I FELT IT" in location:
            location = location[:-36]
        elif "I FELT IT" in location:
            location = location[:-10]

        if mag == "?":
            mag = "_unavialable_"

        if depth == "n/a":
            depth = "_unavailable_"

        response = "Did someone call to hear about an earthquake?\n\nThe most recent earthquake occured on **%s** at**%s**. The magnitude of this earthquake was **%s** on the Richter scale and its depth was **%s**.\n\n_All information is from_ `https://www.volcanodiscovery.com/earthquakes/today.html`" % (time, location, mag, depth)

        await message.channel.send(response)
        
    elif message.content.startswith('$dailysummary'):
        summary = soup.find_all("div", attrs={"class":"textbox"})[0].get_text()
        index = summary.find("writeAge")
        paragraph = summary[0:index]
        index = paragraph.find("Biggest")
        topLines = paragraph[0:index]
        
        response = "%s \n\n_All information is from_ `https://www.volcanodiscovery.com/earthquakes/today.html`" % topLines
        await message.channel.send(response)
        
    elif message.content.startswith('$strongestquake'):
        text = soup.find('div', attrs={'class': 'textbox'}).getText()
        start = text.find('Biggest quake')
        end = text.find('Most recent quake')
        
        response = "%s \n\n_All information is from_ `https://www.volcanodiscovery.com/earthquakes/today.html`" % text[start:end]
        await message.channel.send(response)
        
    elif message.content.startswith('$help'):
        response = "Commands:\n\n`$earthquake` to see the most recent earthquake\n\n`$dailysummary` to see the daily summary of all the earthquakes across the globe\n\n`$strongestquake` to see the strongest earthquake today"

        await message.channel.send(response)

client.run(my_secret)
