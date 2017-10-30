import asyncio
import discord
import urllib
import re
import requests
import pafy
import os
import sys
import time
from bs4 import BeautifulSoup
from discord.ext import commands

#Repurposed from Rapptz Example

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')
    
class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player
        vol = 0.2

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Voice:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass
 
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song."""
        name = str(ctx.message.author)
        server = ctx.message.author.server
        message = ctx.message
        
        def youtube(query:str, num:int = 0):
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
            return page
        
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        link = song.split(':')
        if link[0] == 'https':
            ytsearch = song
        elif link[0] == 'http':
            ytsearch = song
        else:
            ytsearch = youtube(song)
                 
        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(ytsearch, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            #IF BREAK RESTART
            restart_program()
        else:
            player.volume = 0.2
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)		

    @commands.command(pass_context=True)
    async def prow(self, ctx, word:str):
        """Returns the pronounciation of a word from Wiktionary"""
        ipaText = ""
      	##if not state.is_playing():
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        if state.voice is None:
                success = await ctx.invoke(self.summon)
                if not success:
                    return
        tries = 1
        
        wiki = 'https://en.wiktionary.org' 
        webpage = wiki + '/wiki/' + word
        while (tries < 3):
            r = requests.get(webpage).text
            soup = BeautifulSoup(r)
            try:
                ipa = soup.find_all("span", {"class": "IPA"})[0]
                ipaText = ipa.text
                tries = 3
            except IndexError:
                    page = soup.find_all("div", {"class": "disambig-see-also"})[0]
                    webpage = page.find_all('a')[0].get('href')
                    webpage = wiki + webpage
                    tries = tries + 1
        tries = 1
        ##Play Sound File
        while (tries < 3):
            r = requests.get(webpage).text
            soup = BeautifulSoup(r)
            
            try:
                snd = soup.find_all('td', {'class': 'audiometa'})[0]
                sndsite = snd.find_all('a')[0].get('href')
                
                r = requests.get(wiki+sndsite).text
                soup = BeautifulSoup(r)
                blip = soup.find_all("div", {"class": "fullMedia"})[0].find_all('a')[0].get('href')
                urllib.request.urlretrieve('https:' + blip, "sound.ogg")
                player = state.voice.create_ffmpeg_player('sound.ogg')
                player.start()
                tries = 3
            except IndexError:
                page = soup.find_all("div", {"class": "mw-parser-output"})[0]
                webpage = page.find_all('a')[0].get('href')
                webpage = wiki + webpage
                tries = tries + 1
         
    @commands.command(pass_context=True)
    async def pro(self, ctx, *, words:str):
        """Returns the pronounciation of a word from Dictionary.com"""
      	##setup
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        if state.voice is None:
                success = await ctx.invoke(self.summon)
                if not success:
                    return
        ##done setup
        
        arr = words.split(' ')
        
        dict = 'http://www.dictionary.com/browse/'
        for x in range(0, len(arr)):
            #print (arr[x])
            webpage = dict + arr[x]
        
            r = requests.get(webpage).text
            soup = BeautifulSoup(r)
            try:
                sound = soup.find_all("div", {"class": "audio-wrapper cts-disabled"})[0]
                sndsite = sound.find_all('source')[0].get('src')
                urllib.request.urlretrieve(sndsite, "word.ogg")
                player = state.voice.create_ffmpeg_player('word.ogg')
                player.start()
                time.sleep(.25)
            except IndexError:
                await self.bot.say(arr[x] + ' is not a word')
   
    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        if (ctx.message.author):
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                if value > 200:
                    value = 200
                player.volume = value / 100
            
                await self.bot.say('Set the volume to {:.0%}'.format(player.volume))
        else:
            await self.bot.say("Set the volume to `error`")

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
            self.bot.say('Paused')

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            self.bot.say('Resumed', delete_after = 15)

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)
        summoned_channel = ctx.message.author.voice_channel

        if state.is_playing():
            player = state.player
            player.stop()
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            if summoned_channel is None:
                return False
            else:
                if state.voice is None:
                    success = await ctx.invoke(self.summon)
                if not success:
                    return
        except:
            pass
        
    @commands.command(pass_context=True, no_pm=True)
    async def leave(self, ctx):
        """Bot Leaves Voice Channel"""
        server = ctx.message.server
        state = self.get_voice_state(server)
        if state.is_playing():
            player = state.player
            player.stop()
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass   

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Skips Song
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return
        else:
            state.skip()

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/1]'.format(state.current, skip_count))
def setup(bot):
    bot.add_cog(Voice(bot))
