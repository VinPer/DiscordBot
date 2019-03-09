# -*- coding: utf-8 -*-

import discord
import asyncio

from discord.ext import commands

"""
This extension implements a random assortment of miscellaneous commands,
mostly for testing and without significant use, although it may also implement
more meaningful but uncategorizable commands in the future.
"""


class Misc:
    def __init__(self, client):
        self.client = client

    """
    Repeats an incoming message exactly as it is sent. Will not resend files.
    """
    @commands.command(name='repeat',
                      description='Repeats the given phrase.',
                      aliases=['r'],
                      pass_context=True)
    async def repeat(self, context):
        client = self.client
        try:
            content = context.message.content.split(" ", maxsplit=1)[1]
            await client.say(content)
        except Exception:
            await client.say("You must give me something to repeat.")
        # delete the message the user sent, in case it's within a server
        try:
            await client.delete_message(context.message)
        except Exception:
            pass

    """
    Collects the avatar of a mentioned user or the author of the message.
    Implements itself through an embed.
    """
    @commands.command(name="summon",
                      description="A quick command to summon your own or \
                          someone's avatar.",
                      pass_context=True)
    async def summon(self, context):
        client = self.client
        # selects the first mention; selects the author if there is none
        try:
            mention = context.message.mentions[0]
        except Exception:
            mention = context.message.author

        embed = discord.Embed(
            description="Here's " + mention.name + "'s avatar.",
            colour=discord.Colour.teal())
        embed.set_image(url=mention.avatar_url)
        embed.set_author(name=client.user.name,
                         icon_url=client.user.avatar_url)
        await client.say(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
