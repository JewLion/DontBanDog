import discord
import random
from discord.ext import commands

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, dice : int):
        """Rolls a Dice"""
        result = random.randint(1, dice)
        await ctx.send(str(result))

    @commands.command(pass_context=True)
    async def oddsOn(self, ctx, num : int, action : str):
        """OddsOn?"""
        odd1 = random.randint(1,num)
        odd2 = random.randint(1,num)

        if odd1 == odd2:
            await ctx.send('You must ' + action)
        else:
            await ctx.send('You got lucky')
        await ctx.send('Roll 1: ' + str(odd1) + '\t\tRoll 2: ' + str(odd2))

    @commands.command(pass_context=True, description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command(pass_context=True)
    async def joke(self, ctx):
        """It's a funny joke"""
        rand = random.randint(1,5)
        if rand == 1:
            await ctx.send("What do you get from a pampered cow?")
            await ctx.send('Spoiled milk')
        elif rand == 2:
            await ctx.send("There was no punchline.")
        elif rand == 3:
            await ctx.send("What do you call a pile of kittens?")
            await ctx.send('A meowntain')
        elif rand == 4:
            await ctx.send("What do Alexander the Great and Winnie the Pooh have in common")
            await ctx.send("Their middle name")
        else:
            await ctx.send("How many cops does it take to change a light bulb?")
            await ctx.send("None, they just beat the room for being black!")

    @commands.command(pass_context=True)
    async def randomow(self, ctx):
        """Picks a random Overwatch character"""
        charlist = ["Ana", "Bastion", "DoomFist", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Orissa" "Pharah", "Reaper", "Reinhardt", "Roadhoag", "Soldier: 76", "Sombra", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta"]
        await ctx.send(random.choice(charlist))
    @commands.command(pass_context=True)
    async def randomr6A(self, ctx):
        """Picks a random Attacker for Rainbow Six Seige"""
        operators = ["Ying", "Hibana", "Jackal", "Ash", "Blackbeard", "IQ", "Thatcher", "Buck", "Fuze", "Glaz", "Capitão", "Twitch", "Thermite", "Sledge", "Montagne", "Blitz", "Recruit"#, "Dokkaebi", "Zofia"
        ]
        await ctx.send(random.choice(operators))
    @commands.command(pass_context=True)
    async def randomr6D(self, ctx):
        """Picks a random Defender for Rainbow Six Seige"""
        operators = ["Caveira", "Lesion", "Echo", "Mira", "Tachanka", "Valkyrie", "Frost", "Mute", "Kapkan", "Smoke", "Rook", "Jäger", "Doc", "Castle", "Pulse", "Bandit", "Recruit", "Ela"#, "Vigil"
        ]
        await ctx.send(random.choice(operators))
    @commands.command(pass_context=True)
    async def appearin(self, ctx):
        """Creates a ScreenSharing Website Link"""
        num = random.randint(1000000, 9999999)
        await ctx.send("https://appear.in/" + str(num))



def setup(bot):
    bot.add_cog(RNG(bot))
