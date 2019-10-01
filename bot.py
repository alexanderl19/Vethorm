# STL

import asyncio
import traceback
import sys

# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT

import utilities.vqueries as vquery
import utilities.secret as secret
from utilities.catalogue import UCICatalogueCachedScraper

# CONSTANTS

description = 'Vethorm: Protector of the shrine.\nBot made for the UCI Discord server.'

cogs = [
    'cogs.courses',
    'cogs.onhandling',
    'cogs.tags',
    'cogs.utility',
    'cogs.watch'
]

# FUNCTIONS

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id} ', '$']
    return base

# CLASSES

class Vethorm(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, owner_id=secret.OWNER)

        loop = asyncio.get_event_loop()
        vrun = loop.run_until_complete

        # asyncpg connection pool THIS MUST BE LOADED FIRST
        self.Vpool = vrun(vquery.init_database_connection())
        # UCICatalogueCachedScraper object for scraping
        self.Vcourses = UCICatalogueCachedScraper(7*86400)
        # dictionary course aliases
        self.Valiases = vrun(vquery.request_catalogue_aliases(self))
        # dictionary of servers
        self.Vguilds = vrun(vquery.request_guilds(self))
        # diction of users by guild id
        self.Vusers = vrun(vquery.request_users(self))
        # dictionary of channels by guild id
        self.Vchans = vrun(vquery.request_channels(self))
        # dictionary of tags by server
        self.Vtags = vrun(vquery.request_tags(self))

        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                print(f'Cog failed to load ({cog}).', file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        print(f'{self.user} online (ID: {self.user.id})')
        print(f'==================================================')
        game = discord.Game(name='Watching the shrine')
        await self.change_presence(activity=game)
        # load guild and insert new ones
        for guild in self.guilds:
            if guild.id not in self.Vguilds:
                await vquery.insert_guild(self, guild.id)
        print('==== Guilds Loaded ====')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_guild_join(self, guild):
        if guild.id not in self.Vguilds:
            await vquery.insert_guild(self, guild.id)
    
    def run(self):
        super().run(secret.BOT_TOKEN, reconnect=True)
        

# MAIN



