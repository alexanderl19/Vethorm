import discord

from discord.ext import commands

from discord.ext.commands import Context

import utilities.vqueries as vquery

def setup(bot):
    bot.add_cog(VoiceChannel(bot))

class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command(name='crvc')
    async def create_voice_channel(self, ctx, channel_name, category=None):
        """
            Creates a voice/text/role pairing in the databse and on the server\
        """
        guild = ctx.guild
        reason = f"Created voice/text pairing"

        voice_channel = await guild.create_voice_channel(name=channel_name, category=category, reason=reason)
        text_channel = await guild.create_text_channel(name=channel_name, category=category, reason=reason)
        role = await guild.create_role(name=channel_name, reason=reason)

        permissions = {
            'read_messages' : True,
            'send_messages' : True,
            'read_message_history' : True
        }
        await text_channel.set_permissions(role, **permissions)
        for p in permissions.keys():
            permissions[p] = False
        await text_channel.set_permissions(guild.default_role, **permissions)

        await vquery.insert_voice_channel(self.bot, guild.id, voice_channel.id, text_channel.id, role.id)

        # TODO: change to embed
        await ctx.send(f'New voice channel created\n Voice id=`{voice_channel.id}`\n Text id=`{text_channel.id}`\n Role id=`{role.id}`')

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command(name='delvc')
    async def delete_voice_channel(self, ctx: Context, voice_id: int):
        """
            Deletes a voice channel and any associated text channel or role
        """
        voice_id = int(voice_id)
        guild = ctx.guild

        if guild.id in self.bot.Vvc and voice_id in self.bot.Vvc[guild.id]:
            text_id = self.bot.Vvc[guild.id][voice_id]['text_id']
            role_id = self.bot.Vvc[guild.id][voice_id]['role_id']
            
            voice_channel = guild.get_channel(voice_id)
            text_channel = guild.get_channel(text_id)
            role = guild.get_role(role_id)

            if voice_channel:
                await voice_channel.delete()
            if text_channel:
                await text_channel.delete()
            if role:
                await role.delete()

            await vquery.remove_voice_channel(self.bot, guild.id, voice_id)

            await ctx.send('Removed voice channel and associated roles')
        else:
            await ctx.send(f'No channel id ({voice_id}) found for the guild ({guild.id})')



