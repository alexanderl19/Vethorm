import discord

import secret

import addons.helpers as helpers
import utilities.error_handling as error_handling

from discord.ext import commands


class Alerts:
    def __init__(self, bot):
        self.bot = bot
        self.id_to_alert = secret.PROFILE_ID
        self.id_to_watch = secret.LOOKOUT_ID

    async def on_join_check(self) -> bool:
        """
        used to check whether join alerts are enabled
        if alerts or the on_join key arent apart of the guild data then they are create
        :return: bool signifying the status of "on_join"
        """
        try:
            return self.bot.guild_data['alerts']['on_join']
        except KeyError:
            if 'alerts' not in self.bot.guild_data:
                self.bot.guild_data['alerts'] = {}
                self.bot.dump()
            if 'on_join' not in self.bot.guild_data['alerts']:
                self.bot.guild_data['alerts']['on_join'] = False
                self.bot.dump()
                return False
        except Exception as e:
            error_handling.ErrorHandling.print_error_to_console(e, "on_join_check")
            await error_handling.ErrorHandling.dm_error(self, e, "on_join_check")

    @commands.has_permissions(administrator=True)
    @commands.command(name="joinalerts")
    async def alert_on_join(self, ctx):
        """call this command to toggle join alerts"""
        message_false = "Alerts on join have been set: **False**"
        message_true  = "Alerts on join have been set: **True**"

        try:
            if 'alerts' not in self.bot.guild_data:
                self.bot.guild_data['alerts'] = {}
            if 'on_join' not in self.bot.guild_data['alerts']:
                self.bot.guild_data['alerts']['on_join'] = True
                await ctx.send(message_true)
            else:
                if self.bot.guild_data['alerts']['on_join']:
                    self.bot.guild_data['alerts']['on_join'] = False
                    await ctx.send(message_false)
                else:
                    self.bot.guild_data['alerts']['on_join'] = True
                    await ctx.send(message_true)
        except Exception as e:
            error_handling.ErrorHandling.print_error_to_console(e, 'alert_on_join')
            await error_handling.ErrorHandling.dm_error(self, e, 'alert_on_join')
        self.bot.dump()

    async def join_alert(self, member: discord.Member) -> None:
        """
        send an alert for the member that joined
        :param member: discord.Member
        :return: None
        """
        user = self.bot.get_user(secret.PROFILE_ID)
        dm = user.dm_channel
        if dm is None:
            await user.create_dm()
            dm = user.dm_channel
        embed = discord.Embed(title="Member joined UCI", description="Joined at: " + str(member.joined_at),
                              color=0x00812a)
        embed.add_field(name="Tag", value=member.name + "#" + member.discriminator, inline=False)
        embed.add_field(name="Snowflake", value=str(member.id))

        await dm.send(embed=embed)

    async def on_mention_check(self) -> bool:
        """
        check to see if on_mention is enabled, if it doesnt exist it is added to the guild data
        :return:
        """
        try:
            return self.bot.guild_data['alerts']['on_mention']
        except KeyError:
            if 'alerts' not in self.bot.guild_data:
                self.bot.guild_data['alerts'] = {}
                self.bot.dump()
            if 'on_mention' not in self.bot.guild_data['alerts']:
                self.bot.guild_data['alerts']['on_mention'] = False
                self.bot.dump()
                return False
        except Exception as e:
            error_handling.ErrorHandling.print_error_to_console(e, "on_mention_check")
            await error_handling.ErrorHandling.dm_error(self, e, "on_mention_check")

    @commands.has_permissions(administrator=True)
    @commands.command(name="mentionalerts")
    async def alert_on_mention(self, ctx):
        """call to toggle alerts on mention (mentions or just the name)"""
        message_false = "Alerts on mention have been set: **False**"
        message_true  = "Alerts on mention have been set: **True**"

        try:
            if 'alerts' not in self.bot.guild_data:
                self.bot.guild_data['alerts'] = {}
            if 'on_mention' not in self.bot.guild_data['alerts']:
                self.bot.guild_data['alerts']['on_mention'] = True
                await ctx.send(message_true)
            else:
                if self.bot.guild_data['alerts']['on_mention']:
                    self.bot.guild_data['alerts']['on_mention'] = False
                    await ctx.send(message_false)
                else:
                    self.bot.guild_data['alerts']['on_mention'] = True
                    await ctx.send(message_true)
        except Exception as e:
            error_handling.ErrorHandling.print_error_to_console(e, 'alert_on_mention')
            await error_handling.ErrorHandling.dm_error(self, e, 'alert_on_mention')
        self.bot.dump()

    async def mentioned(self, message: discord.Message) -> bool:
        """
        checked to see if a specified user is mentioned
        :param message:
        :return: bool - true if they are mentioned, false if not
        """
        return secret.LOOKOUT_NAME in message.clean_content.lower()

    async def mention_alert(self, message: discord.Message):
        """
        sends an alert to a specified user with the person who sent the message and the content of the message
        :param message:
        :return:
        """
        user = self.bot.get_user(secret.PROFILE_ID)
        dm = await helpers.get_dm_channel(user)
        embed = discord.Embed(title="Profile mentioned")
        embed.add_field(name="Mentioned by", value=message.author.name + " (" + str(message.author.id) + ")", inline=False)
        embed.add_field(name="Content", value=message.clean_content, inline=False)
        embed.add_field(name="Time", value=str(message.created_at))
        await dm.send(embed=embed)


def setup(bot):
    bot.add_cog(Alerts(bot))
