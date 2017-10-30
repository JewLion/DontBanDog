import discord
import time
import random
import os, sys
from discord.ext import commands

class General():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, member : discord.Member):
        """Says when a member joined."""
        await self.bot.say('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command()
    async def who(self, member : discord.User):
    	"""Gives the IRL Alias of the discord member"""
    	await self.bot.say('{0.display_name} is {0.name}'.format(member))
    	
    @commands.command()
    async def unban(self, user):
    	"""Unbans a Member"""
    	##server = member.server
    	await self.bot.unban(user)
    
    @commands.command(pass_context=True)
    async def say (self, ctx, query:str):
        """Bot says what you say"""
        await self.bot.say(query)
    
    @commands.command()
    async def nick (self, ctx, name:str):
        """Change your nickname"""
        await self.bot.change_nickname(message.author, name)
        
    @commands.command()
    async def fix (self):
        """Restarts the Bot"""
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
    @commands.command()
    async def ping (self):
        start = time.time()
        await self.bot.say("Pong!")
        end = time.time()
        ping = end - start
        ping = ping * 1000
        await self.bot.say(str(int(ping)) + "ms")
        
    @commands.command(pass_context=True)
    async def botDelete(self, ctx, num:int = 10):
    	"""Looks through <num> messages and deletes all the bot messages within that limit [default 10]"""
    	message = ctx.message
    	await self.bot.delete_message(message)
    	def is_me(message):
    		return message.author == self.bot.user
    	await self.bot.purge_from(message.channel, limit=num, check=is_me)
      
    @commands.command()
    async def add(self, left : int, right : int):
        """Adds two numbers together"""
        await self.bot.say(left + right)
        
    @commands.command()
    async def sub(self, left : int, right : int):
        """Subtracts two numbers together."""
        await self.bot.say(left - right)
    
    @commands.command()
    async def repeat(self, times : int, content='repeating...'):
        """Repeats a message multiple times. [Max 12]"""
        for i in range(times % 12):
            await self.bot.say(content)

    @commands.command(pass_context=True)
    async def purge (self, ctx, limiter:int = 10):
        """Deletes all messages before it [limit 100]"""
        if (limiter > 100):
            limiter = 100
        message = ctx.message
        await self.bot.delete_message(message)
        await self.bot.purge_from(message.channel, limit=limiter)
        await self.bot.say ("purged by " + message.author)
        
def setup(bot):
    bot.add_cog(General(bot))