import discord
from discord.ext import commands


class Tags:
    def __init__(self, bot):
        self.bot = bot

    # @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def tag(self, ctx, name):
        '''gets a tag - [tag]'''
        if name in self.bot.guild_data["tags"]:
            await ctx.send(self.bot.guild_data["tags"][name])

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def createtag(self, ctx, name, link):
        '''creates a tag - [tag] [content]'''
        if name in self.bot.guild_data["tags"]:
            await ctx.send("{tag} is already a tag\n"
                           "If you would like to change the tag please use \"changetag\"".format(tag=name))
        else:
            self.bot.guild_data["tags"][name] = link
            self.bot.dump()
            if not link.startswith("http://") and not link.startswith("https://"):
                await ctx.send("If {data} was supposed to be a link it needs to begin with http:// or https://\n"
                               "You can change the tag with \"changetag\"".format(data=link))
            await ctx.send("**TAG CREATED** - {tag} : {data}".format(tag=name, data=link))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def changetag(self, ctx, name, link):
        '''changes a tag - [tag] [content]'''
        if name in self.bot.guild_data["tags"]:
            self.bot.guild_data["tags"][name] = link
            self.bot.dump()
            if not link.startswith("http://") and not link.startswith("https://"):
                await ctx.send("If {data} was supposed to be a link it needs to begin with http:// or https://\n"
                               "You can change the tag with \"changetag\"".format(data=link))
            await ctx.send("**TAG CHANGED** - {tag} : {data}".format(tag=name, data=link))
        else:
            await ctx.send("{tag} is not a currently existing tag".format(tag=name))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def deletetag(self, ctx, name):
        '''deletes a tag - [tag]'''
        if name in self.bot.guild_data["tags"]:
            del self.bot.guild_data["tags"][name]
            self.bot.dump()
            await ctx.send("**TAG DELETED** - {tag}".format(tag=name))
        else:
            await ctx.send("{tag} is not a currently existing tag".format(tag=name))

    # @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def listtags(self, ctx):
        '''lists all tag'''
        nembed = discord.Embed(title="Tags")
        for tag, content in self.bot.guild_data["tags"].items():
            nembed.add_field(name=tag, value=content)
        await ctx.send(embed=nembed)


def setup(bot):
    bot.add_cog(Tags(bot))
