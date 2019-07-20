
# STL



# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT

import utilities.vqueries as vquery

# CONSTANTS



# FUNCTIONS



# CLASSES

class Watch:
    def __init__(self, bot):
        self.bot = bot
        self.watch_switch = {

        }

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def serverwatch(self, ctx, mode: str):
        """
            updates the server watch mode
        """
        mode = mode.lower()
        if mode in ['on', 'off']:
            if mode == 'on':
                await vquery.update_server_watch_mode(self.bot.pool, ctx.guild.id, True)
            else:
                await vquery.update_server_watch_mode(self.bot.pool, ctx.guild.id, False)
        else:
            await ctx.send('Incorrect format - **serverwatch <mode [on, off]>**')

    @commands.has_permissions(adminstrator=True)
    @commands.guild_only()
    @commands.command()
    async def channelwatch(self, ctx, mode: str):
        """
            updates the server channel watch mode
        """
        mode = mode.lower()
        if mode in ['on', 'off']:
            if mode == 'on':
                await vquery.update_server_watch_mode(self.bot.pool, ctx.guild.id, True)
            else:
                await vquery.update_server_watch_mode(self.bot.pool, ctx.guild.id, False)
        else:
            await ctx.send('Incorrect format - **channelwatch <mode [on, off]>**')

# MAIN

if __name__ == '__main__':
    print('==== RUNNING WATCH FILE FROM MAIN ====')
