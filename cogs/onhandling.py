# LIBRARY IMPORTS

from datetime import datetime

# THIRD PARTY IMPORTS

from discord.ext import commands

# PROJECT IMPORTS

import utilities.vqueries as vquery

# CONSTANTS



# FUNCTIONS



# CLASSES

class OnHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _user_logging(self, message, msg_type: str, msg_time: datetime):
        """
            Takes a users message and inserts it into the database

            msg_type should correspond to 'Original', 'Edit: before', 'Edit: after', 'Deletion'
        """
        if msg_type not in ['Original', 'Edit: before', 'Edit: after', 'Deletion']:
            # this should probably be switched to a custom exception later
            raise TypeError
        await vquery.insert_user_message(self.bot, message.id, message.author.id, message.guild.id, message.clean_content, msg_type, msg_time)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the message is logged for the user
        """
        # This first check should probably be registered as a check to the bot later and used as a decorator
        if message.guild.id not in self.bot.Vusers or message.author.id not in self.bot.Vusers[message.guild.id]:
            await vquery.insert_user(self.bot, message.author.id, message.guild.id)
        if self.bot.Vservers[message.guild.id]['watch_mode']:
            await self._user_logging(message, 'Original', message.created_at)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the edit is logged for the user
        """
        if before.guild.id not in self.bot.Vusers or before.author.id not in self.bot.Vusers[before.guild.id]:
            await vquery.insert_user(self.bot, before.author.id, before.guild.id)
        if self.bot.Vservers[before.guild.id]['watch_mode']:
            await self._user_logging(before, 'Edit: before', before.edited_at)
            await self._user_logging(after, 'Edit: after', after.edited_at)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
            Checks to see if the user has been added to the database and adds them if not

            If the server has watching enabled then the deletion is logged for the user
        """
        if message.guild.id not in self.bot.Vusers or message.author.id not in self.bot.Vusers[message.guild.id]:
            await vquery.insert_user(self.bot, message.author.id, message.guild.id)
        if self.bot.Vservers[message.guild.id]['watch_mode']:
            await self._user_logging(message, 'Deletion', message.created_at)

def setup(bot):
    bot.add_cog(OnHandling(bot))