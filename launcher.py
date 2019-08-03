# LIBRARY IMPORTS

import asyncio
import json

# THIRD PARTY IMPORTS

import discord
from discord.ext import commands

try:
    import uvloop
except ImportError:
    print("uvloop was unable to import\n"
          "regular asyncio will run instead of uvloop")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# PROJECTS IMPORTS

import utilities.secret as secret
import utilities.vqueries as vquery
import utilities.catalogue as catalogue

# CONSTANTS

extensions = [
    "cogs.courses",
    'cogs.onhandling',
    'cogs.tags',
    'cogs.utility',
    'cogs.watch'
]

prefix = ['$']
bot = commands.Bot(command_prefix=prefix, owner_id=secret.OWNER)

@bot.event
async def on_ready() -> None:
    print(f'Logged in as: {bot.user}')
    print('__________________________________________')
    game = discord.Game(name='$help for help')
    await bot.change_presence(activity=game)
    for guild in bot.guilds:
        if guild.id not in bot.Vservers:
            await vquery.insert_server(bot, guild.id)
    print('==== Guilds Loaded ====')



@bot.event
async def on_message(message):
    # try:
    #     await vquery.insert_server(bot.pool, message.guild.id)
    # except Exception as e:
    #     print(e)
    if message.author.bot:
        return
    await bot.process_commands(message)

async def load():
    from pprint import pprint
    
    # asyncpg connection pool THIS MUST BE LOADED FIRST
    bot.Vpool = await vquery.init_database_connection()
    # UCICatalogueCachedScraper object for scraping
    bot.Vcourses = catalogue.UCICatalogueCachedScraper(7*86400)
    # dictionary course aliases
    bot.Valiases = await vquery.request_catalogue_aliases(bot)
    # dictionary of servers
    bot.Vservers = await vquery.request_servers(bot)
    # diction of users by guild id
    bot.Vusers = await vquery.request_users(bot)
    # dictionary of tags by server
    bot.Vtags = await vquery.request_tags(bot)


if __name__ == "__main__":
    from pathlib import Path
    print(Path.cwd())
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("Failed to load extension {exten}\n"
                  "ERROR - {error_name}: {error}\n".format(exten=extension, error_name=type(e).__name__, error=e))
    asyncio.get_event_loop().run_until_complete(load())
    bot.run(secret.BOT_TOKEN)

