import discord
from discord.ext import commands


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def helpme(self, ctx):
        await ctx.send("To look up courses from the UCI catalogue use the command:\n"
                       "$courseinfo [department] [course number]\n"
                       "$courseinfo I&C SCI 33 or $courseinfo MATH 2A")

class HelpFormatter:
    def __init__(self, bot):
        self.bot = bot
def setup(bot):
    bot.add_cog(Help(bot))
