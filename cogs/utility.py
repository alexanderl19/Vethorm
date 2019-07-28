# STL



# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT



# CONSTANTS



# FUNCTIONS

def setup(bot):
    bot.add_cog(Utility(bot))

# CLASSES

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, snowflake):
        """
            Find a user by their snowflake id
        """
        try:
            member = await self.bot.fetch_user(int(snowflake))
            embed = discord.Embed(title=f'Snowflake: {snowflake}', color=2097148)
            embed.add_field(name='Discord Id', value=f'{member.name}#{member.discriminator}', inline=False)
            embed.add_field(name=f'Creation Date', value=f'{member.created_at}', inline=False)
            embed.add_field(name='Avatar URL', value=f'{member.avatar_url}')
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'{snowflake} couldn\'t be found')

# MAIN

if __name__ == '__main__':
    pass