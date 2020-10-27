import asyncio
import discord
import urllib
import re
import requests
import pafy
import os
import sys
import time
import queue
import subprocess
import youtube_dl
import daudio
from bs4 import BeautifulSoup
from discord.ext import commands


class Voice(commands.Cog):
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = daudio.VoiceState(self.bot)
            self.voice_states[server.id] = state
        return state

    def remove_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is not None:
            del self.voice_states[server.id]

    async def create_voice_client(self, channel):
        voice = await channel.connect()
        state = self.get_voice_state(channel.guild)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except (Exception):
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await ctx.send('Already in a voice channel...')
        except discord.InvalidArgument:
            await ctx.send('This is not a voice channel...')
        else:
            await ctx.send('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        vc = ctx.voice_client
        if not vc:
            await ctx.message.author.voice.channel.connect()
        else:
            await ctx.send("I'm already here")

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song):
        """Plays a song."""
        name = str(ctx.message.author)
        server = ctx.message.author.guild
        message = ctx.message

        if (ctx.message.author.voice is None):
            await ctx.send("Not in voice channel")
            return
        channel = ctx.message.author.voice.channel
        vc = ctx.voice_client
        print(vc)
        if not vc:
            vc = await channel.connect()

        link = song.split(':')
        if link[0] == 'https' or link[0] == 'http':
            ytsearch = song
        else:
            ytsearch = daudio.youtube(song)
        print('found song')
        player = await daudio.YTDLSource.from_url(ytsearch)
        vs = self.get_voice_state(ctx.guild)
        # vc.play(player, after=lambda e: print('done',e))
        lume = 0.2
        if vc.source:
            lume = vc.source.volume
        entry = daudio.VoiceEntry(ctx.message, player, vc, lume)
        await ctx.send('Enqueued ' + str(entry))
        await vs.songs.put(entry)

    @commands.command(pass_context=True)
    async def lol(self, ctx):
        """Plays a Laugh Track"""
        await daudio.play_soundfile(self, ctx, 'audio/lol.mp3')

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value):
        """Sets the volume of the currently playing song."""
        channel = ctx.message.author.voice.channel
        if (ctx.message.author != ctx.message.guild.get_member_named('')):
            vc = ctx.voice_client
            if not vc or not vc.source:
                await ctx.send("Nothing is playing...")
                return
            vc.source = discord.PCMVolumeTransformer(vc.source)

            if value > 200:
                value = 200
            vc.source.volume = value / 100.0
            print(vc.source.volume)
            await ctx.send('Set the volume to {:.0%}'.format(vc.source.volume))
        else:
            await ctx.send("Set the volume to `error`")

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        channel = ctx.message.author.voice.channel
        state = ctx.voice_client
        if not state:
            return
        state = await channel.connect()
        if state.is_playing():
            state.pause()
            await ctx.send('Paused')

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        channel = ctx.message.author.voice.channel
        state = ctx.voice_client
        if not state:
            return
        if state.is_playing():
            state.resume()
            await ctx.send('Resumed', delete_after=15)

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        vc = ctx.voice_client
        if not vc:
            await ctx.send('Nothing is playing...')
        else:
            vc.stop()
            self.remove_voice_state(ctx.guild)

    @commands.command(pass_context=True, no_pm=True)
    async def leave(self, ctx):
        """Bot Leaves Voice Channel"""
        server = ctx.message.guild
        voice = ctx.message.author.voice
        if not voice:
            await ctx.send("You're not in the voice channel")
            return
        channel = voice.channel
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            self.remove_voice_state(ctx.guild)

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Skips Song
        """
        vc = ctx.voice_client
        state = self.get_voice_state(ctx.guild)
        try:
            vc.stop()
            state.skip()
        except Exception as e:
            print(e)
            await ctx.send("Nothing happened")

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        vc = ctx.voice_client
        if vc is None:
            await ctx.send('Not playing anything.')
        else:
            state = self.get_voice_state(ctx.guild)
            await ctx.send('Now playing {}'.format(state.current))


def setup(bot):
    bot.add_cog(Voice(bot))
