import discord


async def get_dm_channel(user: discord.User) -> discord.DMChannel:
    """
        returns a dm channel with the user
        if one doesn't exist it creates one
        :param user: discord.User
        :return: discord.DMChannel
    """
    dm = user.dm_channel
    if dm is None:
        await user.create_dm()
        dm = user.dm_channel
    return dm

