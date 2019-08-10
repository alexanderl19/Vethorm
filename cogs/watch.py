
# STL

from pathlib import Path

# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT

import utilities.vqueries as vquery

# CONSTANTS



# FUNCTIONS



# CLASSES

class Watch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def serverwatch(self, ctx, mode: str):
        """
            updates the server watch mode
        """
        mode = mode.lower()
        if mode in ['on', 'off']:
            if mode == 'on' and not self.bot.Vservers[ctx.guild.id]['watch_mode']:
                await vquery.update_guild_watch_mode(self.bot, ctx.guild.id, True)
                await ctx.send('Guild watch mode set to `True`')
            elif mode == 'off' and self.bot.Vservers[ctx.guild.id]['watch_mode']:
                await vquery.update_guild_watch_mode(self.bot, ctx.guild.id, False)
                await ctx.send('Guild watch mode set to `False`')
            else:
                await ctx.send(f'Guild watch mode already set to `{mode}`')
        else:
            await ctx.send('Incorrect format - **serverwatch <mode [on, off]>**')

    # @commands.has_permissions(adminstrator=True)
    # @commands.guild_only()
    # @commands.command()
    # async def channelwatch(self, ctx, mode: str):
    #     """
    #         updates the server channel watch mode
    #     """
    #     mode = mode.lower()
    #     if mode in ['on', 'off']:
    #         if mode == 'on':
    #             await vquery.update_server_watch_mode(self.bot, ctx.guild.id, True)
    #         else:
    #             await vquery.update_server_watch_mode(self.bot, ctx.guild.id, False)
    #     else:
    #         await ctx.send('Incorrect format - **channelwatch <mode [on, off]>**')

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def checkwatch(self, ctx):
        """
            checks the watch mode for the server
        """
        if ctx.guild.id in self.bot.Vservers:
            await ctx.send("Watch enabled" if self.bot.Vservers[ctx.guild.id]['watch_mode'] else "Watch disabled")
        else:
            await ctx.send('Something brok :b:')

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def watchfile(self, ctx):
        """
            NOT FINISHED, WRITE TO FILE FORMAT NEEDED
            WRITE TO BIN
            SEND FILE 
            DELETE FILE FROM BIN
        """
        try:
            messages = await vquery.request_user_logs(self.bot, ctx.message.mentions[0].id, ctx.guild.id)
        except IndexError:
            await ctx.send('No user mentioned. Watchfile not pulled.')
        except Exception as e:
            await ctx.send(f'Bot Brok {e}')
        else:
            with open(f'bin/{ctx.message.mentions[0].id}_logs.txt', 'w') as f:
                for m in messages:
                    output = (  f"{m['msg_type']:<15} - {m['message_id']:<20} - {m['msg_date']}\n"
                                f"{m['msg']}\n\n"
                             )
                    f.write(output)
            try:
                with open(f'bin/{ctx.message.mentions[0].id}_logs.txt', 'rb') as f:
                    await ctx.send(file=discord.File(f), delete_after=60.0)
                Path(f'bin/{ctx.message.mentions[0].id}_logs.txt').unlink()
            except FileNotFoundError:
                await ctx.send(f'Something went wrong requesting file for {ctx.message.mentions[0]}')
            

def setup(bot):
    bot.add_cog(Watch(bot))

# MAIN

if __name__ == '__main__':
    print('==== RUNNING WATCH FILE FROM MAIN ====')
