# -*- coding: utf-8 -*-

import discord
import random
import math

from discord.ext import commands

"""
This extension implements basic commands based upon the use of randomly
generated numbers or choices, just to add some interactivity to the bot.
"""


class RNG:
    def __init__(self, client):
        self.client = client

    """
    8ball is a very simple eight ball command, answering a yes or no
    question with a randomly selected choice, having the possibility
    of 2 uncertain answers, 4 affirmative answers and 4 negative answers.
    """

    @commands.command(name="8ball",
                      description="Answers all your yes or no questions.",
                      pass_context=True)
    async def eight_ball(self, context, message: str=None):
        if message is not None:
            author = context.message.author
            possible_responses = [
                "bears ate my response",
                "ask again later",
                "yes.",
                "definitely.",
                "it is certain.",
                "absolutely.",
                "no.",
                "absolutely not.",
                "don't bet on it.",
                "negative."
            ]

            await self.client.say(author.mention + ", " +
                                  random.choice(possible_responses))

        else:
            await self.client.say(author.mention + ", you must supply a ",
                                  "question for me to answer.")

    """
    roll simulates the roll of a dice, although being able to take any
    amount of sides. It allows for you to roll multiple dice and add
    a value to the final result.
    """

    @commands.command(name="roll",
                      description="Rolls a dice of your choice. Use -d to " +
                                  "see all rolls.",
                      aliases=['dice', 'r'])
    async def roll(self, message: str=None, mode: str=None):
        try:
            rolls = int(message.split("d")[0])
            limit = int(message.split("+")[0].split("d")[1])
            # check for presence of + argument
            if len(message.split("+")) > 1:
                add = int(message.split("+")[1])
            else:
                add = 0

            rolls_array = []
            result = 0
            for r in range(rolls):
                random_roll = random.randint(1, limit)
                rolls_array.append(str(random_roll))
                result += random_roll

            # if -d mode is active, display all rolls.
            # may not work with large numbers
            if mode == "-d":
                message = ", ".join(rolls_array) + "\nYou have rolled: " \
                    + str(result+add)
            else:
                message = "You have rolled: " + str(result + add)

            await self.client.say(message)
        except Exception as e:
            await self.client.say("There was an error. Make sure you're " +
                                  "utilizing the NdN or NdN+N formats.")

    """
    choose has the bot choose randomly from a set of text options the user
    provides, separated by commas.
    """

    @commands.command(name="choose",
                      description="Chooses between a set of options. " +
                                  "Separate them by a comma.",
                      aliases=["choice"],
                      pass_context=True)
    async def choose(self, context):
        try:
            content = context.message.content.split(" ", maxsplit=1)[1]
            options = content.split(",")
            await self.client.say("I have chosen: " + random.choice(options))
        except Exception:
            await self.client.say("You gave me no options to choose from.")


def setup(client):
    client.add_cog(RNG(client))
