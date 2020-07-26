import discord
import random
import asyncio
import os
import sys
import datetime
from discord.ext import commands

# this specifies what extensions to load when the bot starts up
startup_extensions = ["rng", "search", "general", "voice"]

description = '''A bot made by Julian.'''
bot = commands.Bot(command_prefix=('?'), description=description)

token = ""
with open ('secrets.txt') as f:
    lines = f.readlines()
    token = lines[0].strip()

@bot.event
@asyncio.coroutine
async def on_member_join(member):
    server = member.guild
    fmt = '```Welcome {0.name} to {1.name}!```'
    await server.channels[0].send(fmt.format(member, server))

@bot.event
@asyncio.coroutine
async def on_member_remove(member):
	server = member.guild
	fmt = '```{0.name} has been kicked by {1.name}```'
	await server.channels[0].send(fmt.format(member, server))

@bot.event
@asyncio.coroutine
async def on_member_ban(member):
	server = member.guild
	fmt = '```{0.name} has been banned by {1.name}```'
	await server.channels[0].send(fmt.format(member, server))

@bot.event
@asyncio.coroutine
async def on_message(message):
    if message.content.startswith(''):
        rand = random.randint(1,5)
        if (rand == 1):
            msg = "With Her Mind"
        elif (rand == 2):
            msg = "In the Jungle"
        elif (rand == 3):
            msg = "Apples n Oranges"
        elif (rand == 4):
            msg = "bubbles"
        elif (rand == 5):
            msg = "where am i"
        elif (rand == 6):
            msg = "With the Prime Minister"
        await bot.change_presence(activity=discord.Game(name=msg))

    if message.content.startswith('feelsbadman.jpg'):
        await message.channel.send('https://openclipart.org/image/2400px/svg_to_png/222252/feels.png')
    if message.content.startswith('feelsgoodman.jpg'):
        await message.channel.send('http://i2.kym-cdn.com/entries/icons/original/000/000/142/feelsgood.jpg')
    if message.content.startswith('feelsamazingman.jpg'):
        await message.channel.send('https://static-cdn.jtvnw.net/jtv_user_pictures/feelsamazingman-profile_image-4f58813faad77764-300x300.png')
    if message.content.startswith('Are you sure about that?'):
        await message.channel.send('http://i.imgur.com/auM1Xmb.gif')

    await bot.process_commands(message)

@bot.event
async def on_ready():
    fmt = "%a, %b %d, %Y %H:%M:%S"
    now = datetime.datetime.now()
    print (now.strftime(fmt))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@commands.command(pass_context=True)
async def load(self, ctx, extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@commands.command(pass_context=True)
async def unload(self, ctx, extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@commands.command(pass_context=True)
async def refresh(self, ctx, extension_name : str):
    """Unloads then loads command"""
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} refreshed.".format(extension_name))

@commands.command(pass_context=True)
async def tags(self, ctx, command : str, query = 'query'):
    if command == 'list':
        """Lists all the commands"""
        msg = '```Tags:'
        for tag in list(sorted(bot.commands.keys())):
            msg += '\n\t' + tag
        msg += '```'
        await ctx.send(msg)

    else:
        """Returns commands that fit the query"""
        msg = '```Tags found matching \'' + query + '\':'
        for tag in list(sorted(bot.commands.keys())):
            if tag.find(query) > -1:
                msg += '\n\t' + tag
        await ctx.send(msg + '```')

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(token)
