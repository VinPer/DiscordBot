# -*- coding: utf-8 -*-

import discord

from discord.ext import commands

"""
This extension is focused on playing with voice: joining/leaving channels,
playing sound, etc. It has a dependency on the youtube_dl Python library
and requires the ffmpeg framework installed.

youtube_dl:
pip install -U youtube_dl
ffmpeg:
https://ffmpeg.zeranoe.com/builds/

Additionally, discord.py must be installed with voice enabled:
pip install -U discord[voice]
"""


class Voice:
    def __init__(self, client):
        self.client = client
        self.players = {}

    """
    Basic play command - joins a channel and starts playing an
    audio from a youtube link.
    """

    @commands.command(name="play",
                      description="Plays a Youtube audio.",
                      pass_context=True)
    async def play(self, context):
        try:
            channel = context.message.author.voice.voice_channel
            server = context.message.server
            if channel is None:
                await self.client.say("You must be in a voice channel to" +
                                      " play audio.")
                return

            url = context.message.content.split(" ", maxsplit=1)[1]
            voice = self.client.voice_client_in(server)
            if self.client.is_voice_connected(server):
                if voice.channel != channel:
                    await voice.move_to(channel)
            else:
                voice = await self.client.join_voice_channel(channel)

            if server.id in self.players:
                self.players[server.id].stop()

            player = await voice.create_ytdl_player(url)
            self.players[server.id] = player
            player.start()
        except Exception as e:
            raise Exception('{}: {}'.format(type(e).__name__, e))
            # print(exc)

    """
    Stops playing audio in the server the command was sent.
    """

    @commands.command(name="stop",
                      description="Stops playing audio.",
                      pass_context=True)
    async def stop(self, context):
        try:
            server = context.message.server
            voice = self.client.voice_client_in(server)
            self.players[server.id].stop()
            self.players.pop(server.id)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(exc)

    """
    Sets the volume for the audio currently playing in the
    server the message was sent. Receives a value between 0
    and 200 (to express 0% to 200%) and applies the change.
    """

    @commands.command(name="volume",
                      description="Adjusts audio volume.",
                      pass_context=True)
    async def volume(self, context, volume: float=100):
        try:
            server = context.message.server
            volume /= 100
            if volume > 2:
                volume = 2
            elif volume < 0:
                volume = 0
            if server.id in self.players:
                self.players[server.id].volume = volume
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(exc)


def setup(client):
    client.add_cog(Voice(client))
