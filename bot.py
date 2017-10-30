import discord
import random
import asyncio
import os
import sys
from discord.ext import commands

# this specifies what extensions to load when the bot starts up
startup_extensions = ["rng", "search", "general", "voice"]

description = '''A helpful bot made by Julian.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
@asyncio.coroutine
async def on_member_join(member):        
    server = member.server
    fmt = '```Welcome {0.name} to {1.name}!```'
    await bot.send_message(server, fmt.format(member, server))

@bot.event
@asyncio.coroutine	
async def on_member_remove(member):
	server = member.server
	fmt = '```{0.name} has been removed by {1.name}```'
	await bot.send_message(server, fmt.format(member, server))

@bot.event
@asyncio.coroutine
async def on_member_ban(member):
	server = member.server
	fmt = '```{0.name} has been banned from {1.name}```'
	await bot.send_message(server, fmt.format(member, server))
	
@bot.event
@asyncio.coroutine
async def on_message(message):
    # Changes what the bot is playing everytime there is a message in Discord
    if message.content.startswith(''):
        rand = random.randint(1,5)
        if (rand == 1):
            msg = "With Pogs"
        elif (rand == 2):
            msg = "the Bongo"
        elif (rand == 3):
            msg = "Apples n Oranges"
        elif (rand == 4):
            msg = "Alphabet Soup"
        elif (rand == 5):
            msg = "With the Cat"
        await bot.change_presence(game=discord.Game(name=msg))

    #Displays a picture if a keyword is pressed    
    if message.content.startswith('feelsbadman.jpg'):
        await bot.send_message(message.channel, 'https://openclipart.org/image/2400px/svg_to_png/222252/feels.png')
    if message.content.startswith('feelsgoodman.jpg'):
        await bot.send_message(message.channel, 'http://i2.kym-cdn.com/entries/icons/original/000/000/142/feelsgood.jpg')
    if message.content.startswith('feelsamazingman.jpg'):
        await bot.send_message(message.channel, 'https://static-cdn.jtvnw.net/jtv_user_pictures/feelsamazingman-profile_image-4f58813faad77764-300x300.png')     
    if message.content.startswith('Are you sure about that?'):
        await bot.send_message(message.channel, 'http://i.imgur.com/auM1Xmb.gif')

    #Start working
    await bot.process_commands(message)

@bot.event
async def on_ready():
    #System Checks
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))
		
@bot.command()
async def tags(command : str, query = 'query'):
    if command == 'list':
        """Lists all the commands"""
        msg = '```Tags:'
        for tag in list(sorted(bot.commands.keys())):
            msg += '\n\t' + tag
        msg += '```'
        await bot.say(msg)

    else:
        """Returns commands that fit the query"""
        msg = '```Tags found matching \'' + query + '\':'
        for tag in list(sorted(bot.commands.keys())):
            if tag.find(query) > -1:
                msg += '\n\t' + tag
        await bot.say(msg + '```')

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

@bot.command()
async def restart():
    """Restarts the Bot"""
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            await bot.say("Successfully Loaded " + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

	
f = open("token.txt", "r")
bot.run(f.read())

#Restart Bot on Close
python = sys.executable
os.execl(python, python, * sys.argv)