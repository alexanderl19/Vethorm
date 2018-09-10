from discord.ext import commands


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def setbotlog(self, ctx):
        self.bot.guild_data["botlogs"] = ctx.message.channel_mentions[0].id
        self.bot.dump()


def setup(bot):
    bot.add_cog(Mod(bot))