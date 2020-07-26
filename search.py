import discord
import urllib
import re
import os
import random
import requests
import html
import json
from bs4 import BeautifulSoup
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def scrabble (self, ctx, word:str):
        webpage = "http://www.dictionary.com/browse/" + word
        r = requests.get(webpage).text
        soup = BeautifulSoup(r)
        try:
            points = soup.find_all('div', {'class':'game-scrabble'})[0].text
        except IndexError:
            points = 0
        await ctx.send(points)

    @commands.command(pass_context=True)
    async def youtube(self, ctx, *, query:str):
        """Returns the first youtube video"""
        isNotAVideo = True
        url = 'https://youtube.com/results?search_query=' + query.replace(" ", "+")
        r = requests.get(url).text
        soup = BeautifulSoup(r)
        yt = soup.find_all("div", {"class": "yt-lockup-content"})
        num = 0
        while isNotAVideo:
            try:
                if (not 'list' in yt[num].a.get('href')
                and 'watch' in yt[num].a.get('href')
                and len(yt[num].get('class')) < 2
                and not 'googleads.g.doubleclick.net' in yt[num].a.get('href')):
                    isNotAVideo = False
                else:
                    num = num + 1
            except AttributeError:
                num = num + 1

        link = yt[num].a.get('href')
        page = 'https://youtube.com' + link
        await ctx.send(page)

    @commands.command(pass_context=True)
    async def bImage(self, ctx, query:str, num:int = 1):
        """Returns the first image from the bing search"""

        webpage = "http://www.bing.com/images/search?q=" + query.replace(" ", "+") + "&view=detailv2&adlt=off&selectedIndex=0"
        html_content = urllib.request.urlopen(webpage)
        str_html = html_content.read().decode("utf-8")
        match = re.findall(r'src="http://?([^\'" >]+)', str_html)
        if match:
            try:
                await ctx.send("http://" + match[num-1])
            except:
                await ctx.send("```No " + str(num) + "th Result```")
        else:
            await ctx.send("```No Image Found```")

    @commands.command(pass_context=True)
    async def gImage(self, ctx, query:str, num:int = 1):
        """Returns the first image from the google search"""
        #imageKey = "AIzaSyAiIu9VFK4ww8iQUD7XAR6QvRcYW83B3Ks" 
        imageKey = ""
        f = open("secrets.txt", "r")
        imageKey = f.readlines()[1].strip()
        f.close()
        webpage = "https://www.googleapis.com/customsearch/v1?cx=013629950505680552901%3Axac8ijijt08&searchType=image&key=" + imageKey + "&q=" + query.replace(" ", "+")
        r  = requests.get(webpage).text
        js = json.loads(r)
        try:
            pic = (js['items'][1-num]['link'])
            listd = pic.split('.')
            end = (listd[len(listd)-1])
            if (end[:3] == 'jpg'):
                end = 'jpg'
            elif (end[:3] == 'png'):
                end = 'png'
            elif (end[:4] == 'jpeg'):
                end = 'jpg'
            else:
                raise Exception("not jpg or png")
            urllib.request.urlretrieve(pic, "img/gimage." + end)
            await ctx.send(file=discord.File('img/gimage.' + end))
            os.remove('img/gimage.'+end)
            return
        except IndexError:
            await ctx.send("```No " + str(num) + "th Result```")
        except:
            try:
                await ctx.send(pic)
            except:
                await ctx.send("```No Image Found```")


    @commands.command(pass_context=True)
    async def ub(self, ctx, query:str = random):
        """Returns the first Urban Dictionary result"""
        if query == random:
            webpage = "https://www.urbandictionary.com/random.php"
        else:
            webpage = "http://www.urbandictionary.com/define.php?term=" + query.replace(" ", "+")
        r = requests.get(webpage).text
        soup = BeautifulSoup(r, 'lxml')
        title = soup.find_all("div", {"class": "def-header"})[0]
        await ctx.send(title.find_all("a")[0].text)
        meaning = soup.find_all("div", {"class": "meaning"})[0].text
        await ctx.send("Meaning: " + html.unescape(meaning))
        example = soup.find_all("div", {"class": "example"})[0].text
        await ctx.send("Example: " + html.unescape(example))

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, num:int = -1):
        """Returns a random xkcd comic"""
        if (num < 0):
            webpage = "https://c.xkcd.com/random/comic/"
        else:
            try:
                webpage = "https://xkcd.com/" + str(num)

                r = requests.get(webpage).text
                soup = BeautifulSoup(r, 'lxml')
                title = soup.find_all("div", {"id": "ctitle"})[0]
                comic = soup.find_all("div", {"id": "comic"})[0]
                img = comic.find_all("img")[0]
                await ctx.send(title.text)
                await ctx.send("https:" + img.get('src'))
                return

            except IndexError:
                webpage = "https://xkcd.com/"

        r = requests.get(webpage).text
        soup = BeautifulSoup(r)
        title = soup.find_all("div", {"id": "ctitle"})[0]
        comic = soup.find_all("div", {"id": "comic"})[0]
        img = comic.find_all("img")[0]
        await ctx.send(title.text)
        await ctx.send("https:" + img.get('src'))

    @commands.command(pass_context=True)
    async def chobbes(self, ctx):
        calvin = 'https://www.gocomics.com/random/calvinandhobbes'
        r = requests.get(calvin).text
        soup = BeautifulSoup(r, 'lxml')
        pic = soup.find_all('img', {'class':'img-fluid'})[1].get('src')
        urllib.request.urlretrieve(pic, 'img/calvin.jpg')
        await ctx.send(file=discord.File('img/calvin.jpg'))
        os.remove("img/calvin.jpg")

    @commands.command(pass_context=True)
    async def define (self, ctx, query:str, num:int = 1):
        """Returns a definition"""
        url = "https://dictionary.com/browse/" + query
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        defin = soup.find_all("div", {"class": "def-content"})[num - 1]
        await ctx.send(defin.text)


def setup(bot):
    bot.add_cog(Search(bot))
