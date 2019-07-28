# STL



# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT

import utilities.vqueries as vquery

# CONSTANTS



# FUNCTIONS

def setup(bot):
    bot.add_cog(Tags(bot))

# CLASSES

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()   
    async def tag(self, ctx, name):
        if ctx.guild.id in self.bot.Vservers and name in self.bot.Vtags[ctx.guild.id]:
            await ctx.send(self.bot.Vtags[ctx.guild.id][name])

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def ctag(self, ctx, name, info):
        if ctx.guild.id in self.bot.Vservers and name in self.bot.Vtags[ctx.guild.id]:
            await ctx.send(f'{name} is already a tag, delete the tag to change it')
        else:
            await vquery.insert_tag(self.bot, name, ctx.guild.id, info)
            if not info.startswith('http://') and not info.startswith('https://'):
                await ctx.send(f'If `{info}` is a link, `http://` or `https://` must be included for it to be a hyperlink')
            embed = discord.Embed(title='**TAG CREATED**')
            embed.add_field(name=name, value=info)
            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def dtag(self, ctx, name):
        if ctx.guild.id in self.bot.Vservers and name in self.bot.Vtags[ctx.guild.id]:
            await vquery.remove_tag(self.bot, name, ctx.guild.id)
            await ctx.send(f'Tag ({name}) deleted')
        else:
            await ctx.send(f'Tag ({name}) doesn\'t exist')

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def ltags(self, ctx):
        if ctx.guild.id in self.bot.Vservers:
            embed = discord.Embed(title='Tags')
            for name, info in self.bot.Vtags[ctx.guild.id].items():
                embed.add_field(name=name, value=info)
            await ctx.send(embed=embed)

# MAIN

if __name__ == '__main__':
    pass