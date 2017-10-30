import discord
import urllib
import re
import random
import requests
import wikipedia
from bs4 import BeautifulSoup
from discord.ext import commands

class Search():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()    
    async def wiki(self, *, query : str):
        """Returns a wikipedia summary"""
        ans = wikipedia.summary(query)
        await self.bot.say(ans)
  
    @commands.command()
    async def scrabble (self, word:str):
        """Returns the scrabble points of the word"""
        webpage = "http://www.dictionary.com/browse/" + word
        r = requests.get(webpage).text
        soup = BeautifulSoup(r)
        try:
            points = soup.find_all('div', {'class':'game-scrabble'})[0].text
        except IndexError:
            points = 0
        await self.bot.say(points)
    
    @commands.command()
    async def youtube(self, *, query:str):
        """Returns the first youtube video"""        
        isNotAVideo = True
        url = 'https://youtube.com/results?search_query=' + query.replace(" ", "+")
        r = requests.get(url).text
        soup = BeautifulSoup(r)
        yt = soup.find_all("div", {"class": "yt-lockup-content"})
        num = 0
        while isNotAVideo:
            try:
                if (not 'list' in yt[num].a.get('href') and 'watch' in yt[num].a.get('href') and len(yt[num].get('class')) < 2):
                    isNotAVideo = False
                else:
                    num = num + 1
            except AttributeError:
                num = num + 1
                
        link = yt[num].a.get('href')
        page = 'https://youtube.com' + link
        await self.bot.say(page)
       
    @commands.command(pass_context=True)
    async def bImage(self, ctx, query:str, num:int = 1):
        """Returns the first image from the bing search"""
        webpage = "http://www.bing.com/images/search?q=" + query.replace(" ", "+") + "&view=detailv2&adlt=off&selectedIndex=0"
        html_content = urllib.request.urlopen(webpage)
        str_html = html_content.read().decode("utf-8")
        match = re.findall(r'src="http://?([^\'" >]+)', str_html)
        if match:
            try:
                await self.bot.say("http://" + match[num-1])
            except:
                await self.bot.say("```No " + str(num) + "th Result```")
        else:
            await self.bot.say("```No Image Found```")
    
    @commands.command(pass_context=True)
    async def gImage(self, ctx, query:str, num:int = 1):
        """Returns the first image from the google search"""
        #google api token
        gToken = ""
        webpage = "https://www.googleapis.com/customsearch/v1?cx=013629950505680552901%3Axac8ijijt08&searchType=image&key=" + gToken + "&q=" + query.replace(" ", "+")
        html_content = urllib.request.urlopen(webpage)
        str_html = html_content.read().decode("utf-8")
        match = re.findall(r'link": "?([^\'" >]+)', str_html)
        
        if match:
            try:
                await self.bot.say(match[num - 1])
            except IndexError:
                await self.bot.say("```No " + str(num) + "th Result```")
        else:
            await self.bot.say("```No Image Found```") 
   
    @commands.command()
    async def ree(self, num:int = 1):
        """Returns [num] amount of rees with a random amount of Es"""
        gToken = ""
        times = num
        if (times > 10):
            times = 10
        ree = "r"
        rand = 1
        while (times > 0):
            ree = "r"
            rand = random.randint(3,30)
            while (rand > 0):
                ree = ree + "e"
                rand = rand -1
            webpage = "https://www.googleapis.com/customsearch/v1?cx=013629950505680552901%3Axac8ijijt08&searchType=image&key=" + gToken + "&q=" + ree
            ##await self.bot.say(webpage)
            html_content = urllib.request.urlopen(webpage)
            str_html = html_content.read().decode("utf-8")
            match = re.findall(r'link": "?([^\'" >]+)', str_html)
        
            if match:
                try:
                    await self.bot.say(ree)
                    await self.bot.say(match[0])
                except IndexError:
                    await self.bot.say("```No " + str(num) + "th Result```")
            else:
                await self.bot.say("```No Image Found```")
            times = times -1
        await self.bot.say("REE")

    @commands.command()
    async def ub(self, query:str = random):
        """Returns the first Urban Dictionary result"""
        if query == random:
            webpage = "https://www.urbandictionary.com/random.php"
        else:
            webpage = "http://www.urbandictionary.com/define.php?term=" + query.replace(" ", "+")
        r = requests.get(webpage).text
        soup = BeautifulSoup(r)
        title = soup.find_all("div", {"class": "def-header"})[0]
        await self.bot.say(title.find_all("a")[0].text)
        meaning = soup.find_all("div", {"class": "meaning"})[0].text
        await self.bot.say("Meaning: " + meaning.replace("&apos;", "'"))
        example = soup.find_all("div", {"class": "example"})[0].text
        await self.bot.say("Example: " + example)
            
    @commands.command()
    async def spiderman(self, rando:str = 'random'):
        "Returns a spiderman meme"
        num = random.randint(0, 221)
        if (rando == 'random'):
            webpage = 'http://spidermanmeme.weebly.com'
            r = requests.get(webpage).text
            soup = BeautifulSoup(r)
            meme = soup.find_all("div", {"class": "paragraph"})[0]
            await self.bot.say(meme.find_all("li")[num].text)
        else:
            await self.bot.say('spiderman ' + rando)
     
    @commands.command()
    async def xkcd(self, num:int = -1):
        """Returns a random xkcd comic"""
        if (num < 0):
            webpage = "https://c.xkcd.com/random/comic/"
        else:
            try:
                webpage = "https://xkcd.com/" + str(num)
          
                r = requests.get(webpage).text
                soup = BeautifulSoup(r)
                title = soup.find_all("div", {"id": "ctitle"})[0]
                comic = soup.find_all("div", {"id": "comic"})[0]
                img = comic.find_all("img")[0]
                await self.bot.say(title.text)
                await self.bot.say("https:" + img.get('src'))
                return
                
            except IndexError:
                webpage = "https://xkcd.com/"
                
        r = requests.get(webpage).text
        soup = BeautifulSoup(r)
        title = soup.find_all("div", {"id": "ctitle"})[0]
        comic = soup.find_all("div", {"id": "comic"})[0]
        img = comic.find_all("img")[0]
        await self.bot.say(title.text)
        await self.bot.say("https:" + img.get('src'))       

    @commands.command()
    async def csgo (self, name:str):
        """Returns your csgo stats [input your steamid]"""
        await self.bot.say('http://csgo-stats.com/' + name + '/graphic.png')

    @commands.command()
    async def csgoval (self, name:str):
        """Returns your csgo inventory worth [input your steamid]"""
        try:
            url = "http://csgobackpack.net/?nick=" + name + "&currency=USD"
            r = requests.get(url).text
            soup = BeautifulSoup(r)
            well = soup.find_all("div", {"class": "well"})[2]
            pic = well.find_all("img")[0].get("src")
            name = soup.find_all("div", {"class": "media-body"})[0]
            value = well.find("p").text
            await self.bot.say(pic)
            await self.bot.say(value)
        except:
           await self.bot.say("```User's Inventory is Private or does not exist```")
           
    @commands.command()
    async def gif (self, query:str):
        """Returns a gif"""
        url = "https://tenor.co/search/" + query + "-gifs"
        r = requests.get(url).text
        soup = BeautifulSoup(r)
        div = soup.find_all("div", {"class": "column"})[0]
        gif = div.find_all("a")[0].get('href')
        await self.bot.say('https://tenor.co' + gif)
        
def setup(bot):
    bot.add_cog(Search(bot))
