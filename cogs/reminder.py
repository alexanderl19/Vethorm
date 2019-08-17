# STL

import asyncio
import time

# THIRD PARTY

import discord
from discord.ext import commands

# PROJECT



# CONSTANTS



# FUNCTIONS



# CLASSES

class Reminder:
    def __init__(self, guild: int, owner: int, delta: int, content: str):
        """
            Reminder object
            @param guild    - snowflake id for the guild of the reminder
            @param owner    - snowflake id for the user of the reminder
            @param delta     - time in seconds for the reminder duration
            @param content  - content of the reminder
        """
        assert type(guild)   == int
        assert type(owner)   == int
        assert type(delta)    == int
        assert type(content) == str
        self.guild = guild
        self.owner = owner
        self.created_at = time.time()
        self.remind_at = self.created_at + delta
        self.content = content
    
    def __str__(self):
        return f'Owner: {self.owner}, Length: {self.delta}'

    def __repr__(self):
        return str(self)

    def __lt__(self, right):
        assert type(right) == Reminder
        return self.remind_at < right.remind_at

    def __gt__(self, right):
        assert type(right) == Reminder
        return self.remind_at > right.remind_at

    def __le__(self, right):
        assert type(right) == Reminder
        return self.remind_at <= right.remind_at

    def __ge__(self, right):
        assert type(right) == Reminder
        return self.remind_at >= right.remind_at

    def __eq__(self, right):
        assert type(right) == Reminder
        return self.remind_at == right.remind_at

    def __ne__(self, right):
        assert type(right) == Reminder
        return self.remind_at != right.remind_at

class ReminderManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()


# MAIN

if __name__ == '__main__':
    # item = Reminder(1, 10, 500, 'yeet boi')
    # print(item)
    import time
    import datetime
    dt = datetime.datetime.utcnow()
    rt = time.time()
    print(f'==== Now ====')
    print(dt)
    print(rt)
    print(f'==== Future ====')
    print((dt + datetime.timedelta(seconds=60)).now())
    print(type(rt + 60))
    # datetime.time