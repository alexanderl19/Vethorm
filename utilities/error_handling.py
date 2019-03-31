
import discord

import addons.helpers as helpers
import secret


class ErrorHandling:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def print_error_to_console(error, function: str) -> None:
        print("%s: [%s]\n\t%s" % (type(error).__name__, function, str(error)))

    async def dm_error(self, error, function: str) -> None:
        user = self.bot.get_user(secret.PROFILE_ID)
        dm = await helpers.get_dm_channel(user)
        embed = discord.Embed(title=type(error).__name__ + ": " + function, description=str(error))
        await dm.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
