import discord
import random
from discord.ext import commands

class RNG():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice : int):
        """Rolls a Dice"""
        result = random.randint(1, dice)
        await self.bot.say(str(result))

    @commands.command()
    async def oddsOn(self, num : int, action : str):
        """What are the odds"""
        odd1 = random.randint(1,num)
        odd2 = random.randint(1,num)

        if odd1 == odd2:
            await self.bot.say('You must ' + action)
        else:
            await self.bot.say('You got lucky')
        await self.bot.say('Roll 1: ' + str(odd1) + '\t\tRoll 2: ' + str(odd2))
        
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))
         
    @commands.command()
    async def joke(self):
        """It's a funny joke"""
        rand = random.randint(1,5)
        if rand == 1:
            await self.bot.say("I have a doctor’s appointment today but I really don’t want to go…")
            await self.bot.say('Just call in sick then.')
        elif rand == 2:
            await self.bot.say("The 2016 US Presidential Election")
        elif rand == 3:
            await self.bot.say("A man walks into a bar...")
            await self.bot.say('"Ouch" he said')
        elif rand == 4:
            await self.bot.say("What's the best part about Switzerland'")
            await self.bot.say("I don't know, but the flag is a big plus")
        else:
            await self.bot.say("I wasn’t originally going to get a brain transplant")
            await self.bot.say("but then I changed my mind.")
    
    @commands.command()
    async def randomow(self):
        """Picks a random Overwatch character"""
        charlist = ["Ana", "Bastion", "DoomFist", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Orissa" "Pharah", "Reaper", "Reinhardt", "Roadhoag", "Soldier: 76", "Sombra", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta"]
        await self.bot.say(random.choice(charlist))
        
    @commands.command()
    async def appearin(self):
        """Creates a ScreenSharing Website Link"""
        num = random.randint(1000000, 9999999)
        await self.bot.say("https://appear.in/" + str(num))
              
def setup(bot):
    bot.add_cog(RNG(bot))