# LIBRARY IMPORTS

from datetime import datetime

# THIRD PARTY IMPORTS

import discord
from discord.ext import commands

# PROJECT IMPORTS

import utilities.secret as secret
import utilities.vqueries as vquery

# CONSTANTS



# FUNCTIONS



# CLASSES

class OnHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.valid_msg_types = ['Original', 'Edit: before', 'Edit: after', 'Deletion']
        self.id_to_alert = secret.PROFILE_ID
        self.id_to_watch = secret.LOOKOUT_ID

    async def _user_logging(self, msg, msg_type: str, msg_time: datetime):
        """
            Takes a users message and inserts it into the database

            msg_type should correspond to 'Original', 'Edit: before', 'Edit: after', 'Deletion'
        """
        if msg_type not in self.valid_msg_types:
            # this should probably be switched to a custom exception later
            raise TypeError
        await vquery.insert_user_message(self.bot, msg.id, msg.author.id, msg.guild.id, msg.clean_content, msg_type, msg_time)

    async def _chan_logging(self, msg, msg_type: str, msg_time: datetime):
        """

        """
        if msg_type not in self.valid_msg_types:
            raise TypeError
        await vquery.insert_channel_message( self.bot, msg.id, msg.channel.id, msg.guild.id, msg.clean_content, msg_type, msg_time, msg.author.id)

    async def _member_join_alert(self, member):
        if self.id_to_alert is None:
            return

        user = self.bot.get_user(self.id_to_alert)
        dm = user.dm_channel
        if dm is None:
            await user.create_dm()
            dm = user.dm_channel
        embed = discord.Embed(title="Member joined UCI", description=f'Joined at: {member.joined_at}', color=0x00812a)

        embed.add_field(name='Username', value=f'{member.name}#{member.discriminator}', inline=False)
        embed.add_field(name='Snowflake', value=str(member.id), inline=False)

        await dm.send(embed=embed)

    async def _mentioned(self, msg) -> bool:
        """
            Checks if a specified user was mentioned in the message
        """
        user = self.bot.get_user(self.id_to_watch)
        return user.name.lower() in msg.clean_content.lower()

    async def _mention_alert(self, msg):
        """
            Sends an alert to a specified user with message author, author snowflake, and content 
        """
        if self.id_to_alert is None:
            return
        user = self.bot.get_user(self.id_to_alert)
        dm = user.dm_channel
        if dm is None:
            await user.create_dm()
            dm = user.dm_channel
        embed = discord.Embed(title='Profile mentioned')
        embed.add_field(name='Mentioned by', value=f'{msg.author.name}#{msg.author.discriminator} - ({msg.author.id})', inline=False)
        embed.add_field(name='Guild', value=msg.channel.guild.name, inline=False)
        embed.add_field(name='Channel', value=msg.channel.name, inline=False)
        embed.add_field(name='Content', value=msg.clean_content, inline=False)
        embed.add_field(name='Time', value=str(msg.created_at))

        await dm.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the message is logged for the user
        """
        # This first check should probably be registered as a check to the bot later and used as a decorator
        if message.author.bot:
            return
        if await self._mentioned(message):
            await self._mention_alert(message)
        if message.guild.id not in self.bot.Vguilds:
            await vquery.insert_guild(self.bot, message.guild.id)
        if message.author.id not in self.bot.Vusers[message.guild.id]:
            await vquery.insert_user(self.bot, message.author.id, message.guild.id)
        if message.channel.id not in self.bot.Vchans[message.guild.id]:
            print(f'Inserting channel {message.channel.id}')
            await vquery.insert_channel(self.bot, message.channel.id, message.guild.id)

        if self.bot.Vguilds[message.guild.id]['watch_mode']:
            await self._user_logging(message, 'Original', message.created_at)
            await self._chan_logging(message, 'Original', message.created_at)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the edit is logged for the user
        """
        if before.author.bot:
            return
        if before.guild.id not in self.bot.Vusers or before.author.id not in self.bot.Vusers[before.guild.id]:
            await vquery.insert_user(self.bot, before.author.id, before.guild.id)
        if before.guild.id not in self.bot.Vchans or before.channel.id not in self.bot.Vchans[before.guild.id]:
            await vquery.insert_channel(self.bot, before.channel.id, before.guild.id)

        if self.bot.Vguilds[before.guild.id]['watch_mode']:
            await self._user_logging(before, 'Edit: before', before.created_at)
            await self._user_logging(after, 'Edit: after', after.created_at)

            await self._chan_logging(before, 'Edit: before', before.created_at)
            await self._chan_logging(after, 'Edit: after', after.created_at)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the deletion is logged for the user
        """
        if message.author.bot:
            return
        if message.guild.id not in self.bot.Vusers or message.author.id not in self.bot.Vusers[message.guild.id]:
            await vquery.insert_user(self.bot, message.author.id, message.guild.id)
        if message.guild.id not in self.bot.Vchans or message.channel.id not in self.bot.Vchans[message.guild.id]:
            await vquery.insert_channel(self.bot, message.channel.id, message.guild.id)

        if self.bot.Vguilds[message.guild.id]['watch_mode']:
            await self._user_logging(message, 'Deletion', message.created_at)

            await self._chan_logging(message, 'Deletion', message.created_at)

    # TODO: Create method of catching errors so I can debug issues while in beta
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     print(self.bot.owner_id)
    #     owner = await self.bot.fetch_user(self.bot.owner_id)
    #     await ctx.send(f'Error: {error}\n{owner.mention} - Error type: {error')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
            Alerts a specified user on member joins
        """
        await self._member_join_alert(member)


def setup(bot):
    bot.add_cog(OnHandling(bot))