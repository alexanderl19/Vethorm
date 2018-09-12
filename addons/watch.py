import datamanagement
import discord
from pathlib import Path
from discord.ext import commands
from discord.utils import find


class Watch:
    def __init__(self, bot):
        self.bot = bot
        self.watchswitch = {
            0: "off",
            1: "individual",
            2: "all"
        }

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def watchmode(self, ctx, mode: str):
        '''toggles watch mode'''
        if mode == "individual":
            self.bot.guild_data["watchmode"] = 1
            await ctx.send("Watch mode has been set to individual")
            self.bot.dump()
        elif mode == "off":
            self.bot.guild_data["watchmode"] = 0
            await ctx.send("Watch mode has been set to off")
            self.bot.dump()
        elif mode == "all":
            self.bot.guild_data["watchmode"] = 2
            await ctx.send("Watch mode has been set to all")
            self.bot.dump()
        else:
            await ctx.send("That is not a valid use of the command\n"
                           "Valid options: {options}".format(options=self.watchswitch.values()))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def channelwatch(self, ctx, mode: str):
        '''changes channel watch mode'''
        if mode == "on":
            self.bot.guild_data["channelwatch"] = True
            await ctx.send("Channel watch has been set to on")
            self.bot.dump()
        elif mode == "off":
            self.bot.guild_data["channelwatch"] = False
            await ctx.send("Channel watch has been set to off")
            self.bot.dump()
        else:
            await ctx.send("That is not a valid use of the command\n"
                           "Valid options: ['on', 'off']")

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def checkwatchmodes(self, ctx):
        '''gets watch modes'''
        mode = self.watchswitch[self.bot.guild_data["watchmode"]]
        await ctx.send("Watchmode: {wmode}\n"
                       "ChannelWatch: {cwatch}\n".format(wmode=mode,
                                                  cwatch=self.bot.guild_data["channelwatch"]))

    def watchlist(self, ctx):
        title = "**Users on Watch**"
        description = ""
        for id in self.bot.guild_data["watching"]:
            user = find(lambda person: person.id == id, ctx.guild.members)
            description += user.mention + "\n\n"
        if description == "":
            description = "No users on watch"
        return discord.Embed(title=title, description=description)

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def getwatchlist(self, ctx):
        '''gets list of watched users'''
        if self.bot.guild_data["watchmode"] is 2:
            await ctx.send(f"Watch mode is currently set to {self.watchswitch[2]}\n"
                           f"All users are currently under watch")
        elif self.bot.guild_data["watchmode"] is 1:
            await ctx.send(embed=self.watchlist(ctx))
        elif self.bot.guild_data["watchmode"] is 0:
            await ctx.send(content="Watch mode is currently set to off", embed=self.watchlist(ctx))

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def watch(self, ctx):
        '''starts watching a user'''
        for member in ctx.message.mentions:
            if member.id not in self.bot.guild_data["watching"]:
                self.bot.guild_data["watching"].append(member.id)
                msg = "**WATCH**: {P1} put {P2} on watch\n" \
                      "{name}#{discrim} : {snowflake}".format(P1=ctx.message.author.mention, P2=member.mention,
                                                              name=member.name,discrim=member.discriminator,
                                                              snowflake=member.id)
                if self.bot.guild_data["botlogs"] is None:
                    await ctx.send(msg)
                else:
                    try:
                        channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                       ctx.guild.channels)
                        await channel.send(msg)
                    except Exception as e:
                        await ctx.send("botlogs channel couldn't be found\n" + msg)
        if len(ctx.message.mentions) is not 0:
            self.bot.dump()
        else:
            await ctx.send("You must mention users to use this command\n"
                           "$watch mention1 mention2 mentionx")

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def dewatch(self, ctx):
        '''dewatches a user'''
        for member in ctx.message.mentions:
            try:
                self.bot.guild_data["watching"].remove(int(member.id))
            except ValueError:
                await ctx.send(member.mention + " is not on watch")
            else:
                msg = "**DEWATCH**: {P1} put {P2} off watch\n" \
                    "{name}#{discrim} : {snowflake}".format(
                        P1=ctx.message.author.mention, P2=member.mention, name=member.name,
                        discrim=member.discriminator, snowflake=member.id)
                if self.bot.guild_data["botlogs"] is None:
                    await ctx.send(msg)
                else:
                    try:
                        channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                       ctx.guild.channels)
                        await channel.send(msg)
                    except Exception as e:
                        await ctx.send("botlogs channel couldn't be found\n" + msg)
        if len(ctx.message.mentions) is not 0:
            self.bot.dump()
        else:
            await ctx.send("You must mention users to use this command\n"
                           "$watch mention1 mention2 mentionx")

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def getwatchfile(self, ctx) -> None:
        '''gets the watch file of a user'''
        try:
            await ctx.send(file=discord.File(open("data/watching/users/{id}.txt" \
                                             .format(id=ctx.message.mentions[0].id), 'rb'),
                                                     filename=f'{ctx.message.mentions[0].display_name}_watch_data.txt'))
        except FileNotFoundError:
            await ctx.send("File not found for {user}".format(user=ctx.message.mentions[0]))

    @staticmethod
    async def watchlogging(self, message) -> None:
        '''logs a members messages that are being watched'''
        if self.bot.guild_data["watchmode"] > 0:
            if self.bot.guild_data["watchmode"] is 2 or message.author.id in self.bot.guild_data["watching"]:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "{content}\n" \
                          "".format(nickname=message.author.display_name, name=message.author.name,
                                             discrim=message.author.discriminator, id=message.author.id,
                                             date=message.created_at, mention=message.author.mention,
                                             content=message.content)
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))

    @staticmethod
    async def editlogging(self, before, after) -> None:
        '''used for logging an individuals edits'''
        if self.bot.guild_data["watchmode"] > 0:
            if self.bot.guild_data["watchmode"] is 2 or before.author.id in self.bot.guild_data["watching"]:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "BEFORE EDIT: {content}\n" \
                          "AFTER EDIT: {content2}\n".format(nickname=before.author.display_name, name=before.author.name,
                                             discrim=before.author.discriminator, id=before.author.id,
                                             date=before.edited_at, mention=before.author.mention,
                                             content=before.content, content2=after.content)
                    datamanagement.write_to_user_watch_file(before.author.id, msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))

    @staticmethod
    async def deletelogging(self, message) -> None:
        '''used for logging an individuals deletions'''
        if self.bot.guild_data["watchmode"] > 0:
            if self.bot.guild_data["watchmode"] is 2 or message.author.id in self.bot.guild_data["watching"]:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "DELETED: {content}\n".format(nickname=message.author.display_name, name=message.author.name,
                                             discrim=message.author.discriminator, id=message.author.id,
                                             date=message.created_at, mention=message.author.mention,
                                             content=message.content)
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))

    @staticmethod
    async def channellogging(self, message) -> None:
        '''used for logging a channel's messages'''
        if self.bot.guild_data["watchmode"] is True:
            if self.bot.guild_data["channelwatch"] is True:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "DELETED: {content}\n".format(nickname=message.author.display_name, name=message.author.name,
                                                        discrim=message.author.discriminator, id=message.author.id,
                                                        date=message.created_at, mention=message.author.mention,
                                                        content=message.content)
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))


def setup(bot):
    bot.add_cog(Watch(bot))
