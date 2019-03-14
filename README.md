# DiscordBot
A generic discord bot for experimenting implemented with discord.py.

The bot is ran through **bot.py** and utilizes the discord.py library. Extensions for additional commands are found within the extensions folder.

## bot.py functionality
The main bot.py file serves to set up the bot and connect it to the extensions to add more commands. A couple of commands are included right within the bot.py file as they are slightly more important:

**prefix**: changes the bot's prefix globally.  
**reload**: forces the bot to reload the extensions; can be used to modify extensions without having to restart the bot.

## Misc module
The misc extension implements miscellaneous commands, mostly for feature testing.

**repeat**: repeats what the user has said.  
**summon**: sends the user or a mention's avatar as a file.

## RNG module
The RNG module plays around with randomly generated numbers.

**eight_ball**: answers a yes or no question randomly using a set of predetermined answers.  
**roll**: simulates a dice roll in a NdN or NdN+N format.  
**choose**: chooses between a set of text choices that the user provides.
