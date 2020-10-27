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
    async def scrabble(self, ctx, word):
        url = "https://dictionary.com/browse/" + word
        r = requests.get(url).text
        if ("no results" in r.lower()):
            await ctx.send("word bad bad")
            return
        values = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1,
                  1, 4, 4, 8, 4, 10]
        points = 0
        for letter in word:
            num = ord(letter.lower())-97
            if (num < 0 or num > 25):
                await ctx.send("word bad bad")
                return
            points += values[num]
        await ctx.send(points)

    @commands.command(pass_context=True)
    async def youtube(self, ctx, *, query):
        """Returns the first youtube video"""

        utub = 'https://youtube.com/results?search_query='
        url = utub + query.replace(" ", "+")
        r = requests.get(url).text
        num1 = r.find('{"videoRenderer')
        num2 = r.find('{"videoRenderer', num1+1)
        # print (num1)
        # print (num2)
        videoRenderer = (json.loads(r[num1:num2-1])["videoRenderer"])
        vid = (videoRenderer["videoId"])
        page = ("https://youtube.com/watch?v=" + vid)
        await ctx.send(page)

    @commands.command(pass_context=True)
    async def bImage(self, ctx, query, num=1):
        """Returns the first image from the bing search"""

        webpage = "http://www.bing.com/images/search?q=" + query.replace(" ", "+") + "&view=detailv2&adlt=off&selectedIndex=0"

        html_content = urllib.request.urlopen(webpage)
        str_html = html_content.read().decode("utf-8")
        match = re.findall(r'src="http://?([^\'" >]+)', str_html)
        if match:
            try:
                await ctx.send("http://" + match[num-1])
            except (Exception):
                await ctx.send("```No " + str(num) + "th Result```")
        else:
            await ctx.send("```No Image Found```")

    @commands.command(pass_context=True)
    async def gImage(self, ctx, query, num=1):
        """Returns the first image from the google search"""
        imageKey = ""
        f = open("secrets.txt", "r")
        imageKey = f.readlines()[1].strip()
        f.close()
        webpage = "https://www.googleapis.com/customsearch/v1?cx=013629950505680552901%3Axac8ijijt08&searchType=image&key=" + imageKey + "&q=" + query.replace(" ", "+")
        r = requests.get(webpage).text
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
        except Exception:
            try:
                await ctx.send(pic)
            except Exception:
                await ctx.send("```No Image Found```")

    @commands.command(pass_context=True)
    async def ub(self, ctx, query=random):
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
