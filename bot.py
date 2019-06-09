# BUILT-INS

import asyncio
import json

# THIRD PARTY LIBRARIES

import discord
from discord.ext import commands

# PERSONAL IMPORTS

import datamanagement
import secret

try:
    import uvloop
except ImportError:
    print("uvloop was unable to import\n"
          "regular asyncio will run instead of uvloop")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# GLOBAL CONSTANTS

EXTENSIONS = [
    "addons.alerts",
    "utilities.error_handling",
    "addons.mod",
    "addons.onhandling",
    "addons.tags",
    "addons.ucicourses",
    "addons.watch"
]

prefix = ["$"]

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready() -> None:
    '''runs operations when the bot is ready'''
    """runs operations when the bot is ready"""
    print("Logged in as: {user}".format(user=bot.user))
    print("__________________________________________")
    game = discord.Game(name="$help for help")
    await bot.change_presence(activity=game)
    if bot.guild_data == {}:
        bot.guild_data = {
        'alerts': {},
        'alert_users': [],
        'tags': {},
        'cataloguealiases': {},
        'botlogs': None,
        'watchmode': False,
        'channelwatch': False,
        'watching': []
        }
        bot.dump()


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("Failed to load extension {exten}\n"
                  "ERROR - {error_name}: {error}".format(exten=extension, error_name=type(e).__name__, error=e))

    bot.run(secret.BOT_TOKEN)

