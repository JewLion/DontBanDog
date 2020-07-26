import discord
import time
import random
import os, sys
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, member : discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command(pass_context=True)
    async def who(self, ctx, member : discord.User):
    	"""Gives the IRL Alias of the discord member"""
    	await ctx.send('{0.display_name} is {0.name}'.format(member))

    @commands.command(pss_context=True)
    async def created(self, ctx, user):
        """When were you created"""
        await ctx.send('{0.display_name} was born on {0.created_at}'.format(user))

    @commands.command(pass_context=True)
    async def unban(self, ctx, member : discord.Member):
    	"""Unbans a Member"""
    	server = ctx.guild
    	await server.unban(member)

    @commands.command(pass_context=True)
    async def say (self, ctx, query:str):
        print (query)
        await ctx.send(query)

    @commands.command(pass_context=True)
    async def nick (self, ctx, nick:str, name:str = 'DontBanDog'):
        print (ctx.message.author)
        await self.bot.change_nickname(ctx.message.author.server.get_member_named(name), nick)

    @commands.command(pass_context=True)
    async def ping (self, ctx):
        start = time.time()
        await ctx.send("Pong!")
        end = time.time()
        ping = end - start
        ping = ping * 1000
        await ctx.send(str(int(ping)) + "ms")

    @commands.command(pass_context=True)
    async def botDelete(self, ctx, num:int = 10):
    	"""Looks through <num> messages and deletes all the bot messages within that limit"""
    	message = ctx.message
    	await message.delete
    	def is_me(message):
    		return message.author == self.bot.user
    	await ctx.purge(limit=num, check=is_me)

    @commands.command(pass_context=True)
    async def add(self, ctx, left : int, right : int):
        """Adds two numbers together"""
        await ctx.send(left + right)

    @commands.command(pass_context=True)
    async def sub(self, ctx, left : int, right : int):
        """Subtracts two numbers together."""
        await ctx.send(left - right)

    @commands.command(pass_context=True)
    async def repeat(self, ctx, times : int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times % 12):
            await ctx.send(content)
def setup(bot):
    bot.add_cog(General(bot))
