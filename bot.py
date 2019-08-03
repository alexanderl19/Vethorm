# STL



# THIRD PARTY



# PROJECT

from discord.ext import commands

# CONSTANTS



# FUNCTIONS

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id} ', '$']
    return base

# CLASSES

class Vethorm(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable)

        self.client_id = 

# MAIN



