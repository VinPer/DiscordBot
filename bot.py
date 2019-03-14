# -*- coding: utf-8 -*-

import discord
import asyncio
import json

from discord.ext.commands import Bot

"""
Settings for prefix, token and extensions are found in
the config.json file for easy manipulation.
"""

try:
    with open("config.json") as data_file:
        data = json.loads(data_file.read())
    data_file.close()
except FileNotFoundError:
    print("Configuration not found.")
    exit

TOKEN = data["token"]
BOT_PREFIX = data["prefix"]
STARTUP_EXT = data["extensions"]
LOOP = asyncio.get_event_loop()

client = Bot(command_prefix=BOT_PREFIX,
             description="A generic bot to test functionality with the" +
                         "discord.py API")


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='in space'))
    print('Successfully logged in as ' + client.user.name)

"""
This simple version changes the bot's default prefix on the config file.
Todo - implement server-based prefix selection.
"""


@client.command(name="prefix",
                description="Changes the bot's prefix.")
async def prefix(prefix: str=""):
    if prefix != "":
        with open("config.json") as data_file:
            data = json.loads(data_file.read())
        data_file.close()
        data["prefix"] = prefix
        with open("config.json", "w") as data_file:
            json.dump(data, data_file)

        client.command_prefix = prefix
    else:
        await client.say("No prefix was provided.")

"""
Reloads extensions through the STARTUP_EXT array. Extensions are .py
files with commands to be attached to the bot. This method of
implementation allows for the user to keep the bot up and reload
its commands as they are altered by simply using the reload command.
"""


@client.command(name="reload",
                hidden=True,
                pass_context=True)
async def reload(context):
    app_info = await client.application_info()
    owner = app_info.owner

    if context.message.author.id == owner.id:
        for exten in STARTUP_EXT:
            try:
                client.unload_extension(exten)
                client.load_extension(exten)
                print('Successfully reloaded extension ' + exten)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to operate extension {}\n{}'.format(exten, exc))
    else:
        print("User " + context.message.author.name + " attempted to reload" +
              "extensions")

"""
Loads extensions through the STARTUP_EXT array. Extensions are .py
files with commands to be attached to the bot.
"""

if __name__ == "__main__":
    for extension in STARTUP_EXT:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

"""
Runs the bot. It can be shut down through a KeyboardInterrupt in the
console it is running.
"""

try:
    LOOP.run_until_complete(client.start(TOKEN))
except KeyboardInterrupt:
    LOOP.run_until_complete(client.logout())
    print("Logging out through keyboard interruption.")
    # cancel all tasks lingering
finally:
    print("Bot stopped.")
    LOOP.close()
