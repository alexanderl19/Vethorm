import datamanagement
import discord
from pathlib import Path
from discord.ext import commands
from discord.utils import find


class Watch:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def watchmode(self, ctx, mode: str):
        '''toggles watch mode'''
        if mode == "on":
            self.bot.guild_data["watchmode"] = True
            await ctx.send("Watch mode has been set to on")
            self.bot.dump()
        elif mode == "off":
            self.bot.guild_data["watchmode"] = False
            await ctx.send("Watch mode has been set to off")
            self.bot.dump()
        else:
            await ctx.send("That is not a valid use of the command")

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def checkwatchmodes(self, ctx):
        await ctx.send("Watchmode: {wmode}\n"
                       "ChannelWatch: {cwatch}\n"
                       "Watch All: {wall}".format(wmode=self.bot.guild_data["watchmode"],
                                                  cwatch=self.bot.guild_data["channelwatch"],
                                                  wall=self.bot.guild_data["watchall"]))

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
        if ctx.message.mentions is not list():
            self.bot.dump()

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def dewatch(self, ctx):
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
        if ctx.message.mentions is not list():
            self.bot.dump()

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def getwatchfile(self, ctx) -> None:
        '''grabs the requested watch file and then sends the file to the channel it was requested from'''
        await ctx.send(file=discord.File(open("data/watching/{id}.txt".format(id=ctx.message.mentions[0].id), 'rb'),
                                         filename=f'{ctx.message.mentions[0].display_name}_watch_data'))

    @staticmethod
    async def watchlogging(self, message) -> None:
        '''logs a members messages that are being watched'''
        if self.bot.guild_data["watchmode"] is True:
            if self.bot.guild_data["watchall"] is True or message.author.id in self.bot.guild_data["watching"]:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "{content}\n" \
                          "".format(nickname=message.author.display_name, name=message.author.name,
                                             discrim=message.author.discriminator, id=message.author.id,
                                             date=message.created_at, mention=message.author.mention,
                                             content=message.content)
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                    channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                   message.guild.channels)
                    await channel.send(msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))

    @staticmethod
    async def editlogging(self, before, after) -> None:
        '''used for logging an individuals edits'''
        if self.bot.guild_data["watchmode"] is True:
            if self.bot.guild_data["watchall"] is True or before.author.id in self.bot.guild_data["watching"]:
                try:
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "BEFORE EDIT: {content}\n" \
                          "AFTER EDIT: {content2}\n".format(nickname=before.author.display_name, name=before.author.name,
                                             discrim=before.author.discriminator, id=before.author.id,
                                             date=before.edited_at, mention=before.author.mention,
                                             content=before.content, content2=after.content)
                    datamanagement.write_to_user_watch_file(before.author.id, msg)
                    channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                   before.guild.channels)
                    await channel.send(msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))

    @staticmethod
    async def deletelogging(self, message) -> None:
        '''used for logging an individuals deletions'''
        if self.bot.guild_data["watchmode"] is True:
            if self.bot.guild_data["watchall"] is True or message.author.id in self.bot.guild_data["watching"]:
                try:
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "DELETED: {content}\n".format(nickname=message.author.display_name, name=message.author.name,
                                             discrim=message.author.discriminator, id=message.author.id,
                                             date=message.created_at, mention=message.author.mention,
                                             content=message.content)
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                    channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                   message.guild.channels)
                    await channel.send(msg)
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
                    datamanagement.write_to_user_watch_file(message.author.id, msg)
                    msg = "{nickname}: {name}#{discrim} {id} {date}\n" \
                          "{mention}\n" \
                          "DELETED: {content}\n".format(nickname=message.author.display_name, name=message.author.name,
                                                        discrim=message.author.discriminator, id=message.author.id,
                                                        date=message.created_at, mention=message.author.mention,
                                                        content=message.content)
                    channel = find(lambda channel: channel.id == self.bot.guild_data["botlogs"],
                                   message.guild.channels)
                    await channel.send(msg)
                except AttributeError:
                    pass
                except Exception as e:
                    print("ERROR - {error_name}: {error}".format(error_name=type(e).__name__, error=e))


def setup(bot):
    bot.add_cog(Watch(bot))
