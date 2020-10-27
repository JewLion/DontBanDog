import asyncio
import discord
import urllib
import re
import requests
import pafy
import os
import sys
import time
import json
import queue
import subprocess
import youtube_dl
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
            'format': 'bestaudio/best',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'restrictfilenames': True,
                        'noplaylist': True,
                            'nocheckcertificate': True,
                                'ignoreerrors': False,
                                    'logtostderr': False,
                                        'quiet': True,
                                            'no_warnings': True,
                                                'default_search': 'auto',
                                                    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
                                                    }

ffmpeg_options = {
            'options': '-vn'
            }

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def youtube(query: str, num: int = 0):
    """Returns the first youtube video"""

    url = 'https://youtube.com/results?search_query=' + query.replace(" ", "+")
    print(url)

    r = requests.get(url).text

    num1 = r.find("// scraper_data_begin")
    num2 = r.find("// scraper_data_end")
    # print (num1)
    # print (num2)
    yInit = r[num1:num2-1].strip()

    num1 = yInit.find('{')
    res = yInit[num1:-1]
    resource = json.loads(res)
    ls = resource['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
    videoRenderer = ls[0]['itemSectionRenderer']['contents'][0]['videoRenderer']
    vid = (videoRenderer["videoId"])
    page = ("https://youtube.com/watch?v=" + vid)
    return page


async def disconnect(vc, ctx, cls):
    await vc.disconnect()
    cls.remove_voice_state(ctx.guild)


async def play_soundfile(cls, ctx, sf):
    vc = ctx.voice_client
    path = sf
    if vc:
        state = vc
    else:
        state = await ctx.message.author.voice.channel.connect()
    player = state.play(discord.FFmpegPCMAudio(sf))
    state.source.volume = 0.2
    await ctx.message.channel.purge(limit=1)
    waitTime = MP3(path).info.length

    time.sleep(int(waitTime))
    await disconnect(state, ctx, cls)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.views = data.get('view_count')
        self.uploader = data.get('uploader')
        self.duration = data.get('duration')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


class VoiceEntry:
    def __init__(self, message, player, vc, volume):
        self.requester = message.author
        self.channel = message.channel
        self.player = player
        self.volume = volume
        self.vc = vc

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name} with '
        try:
            views = self.player.views
            num = int(views)
            fmt = fmt + (f"{num:,d}") + " views"
        except:
            fmt += "an unknown amount of views"
        fmt += " at {0}% volume".format(self.volume*100)
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
        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.toggle_next()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        await self.bot.wait_until_ready()
        while True:
        #while self.bot.is_closed():
            self.play_next_song.clear()
            self.current = await self.songs.get()
            if False:
            #if not isinstance(self.current, YTDLSource):
                try:
                    self.current = await YTDLSource.regather_stream(self.current, loop=self.bot.loop)
                except Exception as e:
                    print (e)
                    continue

            self.current.vc.play(self.current.player, after=lambda _: self.toggle_next())
            #self.current.vc.play(self.current.player, after=lambda _: self.bot.loop.call_soon_threadsafe(self.play_next_song.set))
            await self.current.channel.send('Now playing ' + str(self.current))
            await self.play_next_song.wait()
            #self.current.cleanup()
            #self.current = None

