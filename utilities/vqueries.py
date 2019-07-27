
# STL

import asyncio
from datetime import datetime
from collections import defaultdict

# THIRD PARTY

import asyncpg
from discord.ext.commands import Bot

# PROJECT

try:
    import utilities.secret as secret
except ModuleNotFoundError:
    import secret

# CONSTANTS



# FUNCTIONS

async def init_database_connection() -> asyncpg.pool.Pool:
    """
        Creates a connection pool for the bot database

        Return value asyncpg.pool.Pool
    """
    return await asyncpg.create_pool(host=secret.HOST, port=secret.PORT, user=secret.USERNAME, password=secret.PASSWORD, database=secret.DATABASE_NAME)

# Catalogue functions
async def insert_catalogue_alias(bot: Bot, department: str, alias: str, guild_id: int):
    """
        Inserts a new catalogue alias to the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO catalogue_alias VALUES ($1, $2, $3)''', department, guild_id, alias)
            bot.Valiases[department] = alias

async def remove_catalogue_alias(bot: Bot, department: str, guild_id: int):
    """
        Removes a department alias from the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute('''DELETE FROM catalogue_alias WHERE department = $1''', department)
            del bot.Valiases[department]

async def request_catalogue_aliases(bot: Bot) -> {str : str}:
    """
        Requests all the aliases from the database and returns as a dictionary

        Return value {department : alias, ...}
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' SELECT * FROM catalogue_alias ''')

        return {item['alias'] : item['department'] for item in await stmt.fetch()}

# Channel functions
async def insert_channels(bot: Bot, channel_id, guild_id, watching: bool = False):
    """
        Inserts a channel into the database and updates the channels variable
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO channels VALUES ($1, $2, $3) ''', channel_id, guild_id, watching)
            bot.Vchannels[channel_id] = {
                'guild_id' : guild_id,
                'watching' : watching
            }
            
async def insert_channel_message(bot: Bot, message_id:int, channel_id: int, guild_id: int, message: str, message_type: str, date: datetime):
    """
        Inserts a channel message into the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO user_logs VALUES ($1, $2, $3, $4, $5, $6) ''', message_id, channel_id, guild_id, message, message_type, date)

async def request_channel_logs(bot: Bot, channel_id: int, guild_id: int) -> [dict]:
    """
        Requests all the channel logs for a channel and a list of dictionary objects representing the message
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * 
            FROM channel_logs 
            WHERE channel_id = $1 AND guild_id = $2
            ORDER BY date DESC
            ''')
        return [{
            'message_id'    : item['message_id'],
            'channel_id'    : item['channel_id'],
            'guild_id'      : item['guild_id'],
            'message'       : item['message'],
            'message_type'  : item['mtype'],
            'date'          : item['date']
        } for item in await stmt.fetch(channel_id, guild_id)]

# Server functions
async def insert_server(bot: Bot, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new server to the database and updates the servers variable
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO servers VALUES ($1, $2) ''', guild_id, watch_mode)
            bot.Vservers[guild_id] = watch_mode

async def update_server_watch_mode(bot: Bot, guild_id: int, watch_mode: bool):
    """
        Updates a server watch mode
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' UPDATE servers SET watch_mode = $1 WHERE id = $2 ''', watch_mode, guild_id)
            bot.Vservers[guild_id] = watch_mode

async def request_servers(bot: Bot) -> {int: dict}:
    """
        Returns a dictionary of servers where they key is the guild id and the value is attributes of the server

        {
            guild_id : { watch_mode : bool },
            ...
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' SELECT * FROM servers ''')
        return  {   item['id'] : {
                        'watch_mode' : item['watch_mode']
                    } 
                    for item in await stmt.fetch()
                }

# Tag functions
async def insert_tag(bot: Bot, tag: str, guild_id: int, info: str):
    """
        Inserts a tag into the database and updates the tags variable for the bot
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO tags VALUES ($1, $2, $3) ''', tag, guild_id, info)
            bot.Vtags[tag] = info

async def remove_tag(bot: Bot, tag: str, guild_id: int):
    """
        Removes a tag into the database and updates the tags variable for the bot
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' DELETE FROM tags WHERE guild_id = $1 AND tag = $2 ''', guild_id, tag)
            del bot.Vtags[tag]

async def request_tags(bot: Bot, guild_id: int) -> {str : str}:
    """
        Requests the tags from the database and returns them as a dictionary
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * FROM tags 
            WHERE guild_id = $1 
            ''')
        return { item['tag'] : item['info']
            for item in await stmt.fetch(guild_id)
        }

# User functions
async def insert_user(bot: Bot, id: int, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new user to the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO users VALUES ($1, $2, $3) ''', id, guild_id, watch_mode)
            bot.Vusers[guild_id].add(id)

async def insert_user_message(bot: Bot, message_id:int, user_id: int, guild_id: int, message: str, message_type: str, date: datetime):
    """
        Inserts a new user message into the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO user_logs VALUES ($1, $2, $3, $4, $5, $6) ''', message_id, user_id, guild_id, message, message_type, date)

async def request_user_logs(bot: Bot, user_id: int, guild_id: int) -> [dict]:
    """
        Retrieves the logs for a user on a specific server
        [
            'message_id'    : int,
            'user_id'       : int,
            'guild_id'      : int,
            'message'       : str,
            'message_type'  : str,
            'date'          : datetime
        ]
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * FROM user_logs 
            WHERE user_id = $1 AND guild_id = $2 
            ORDER BY date DESC
            ''')
        return [{
            'message_id'    : item['message_id'],
            'user_id'       : item['user_id'],
            'guild_id'      : item['guild_id'],
            'message'       : item['message'],
            'message_type'  : item['mtype'],
            'date'          : item['date']
        } for item in await stmt.fetch(user_id, guild_id)]

async def request_users(bot: Bot) -> {int : set}:
    """
        Requests all the registered users

        {
            guild_id : set(user_id, ...)
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare('''
        SELECT * FROM users
        ''')
        results = defaultdict(set)
        for item in await stmt.fetch():
            results[item['guild_id']].add(item['id'])
        return results




# MAIN

if __name__ == '__main__':
    # print(' ==== VQUERIES MAIN EXECUTION ==== ')
    # try:
    #     import uvloop
    # except ImportError:
    #     print("uvloop was unable to import\n"
    #         "regular asyncio will run instead of uvloop")
    # else:
    #     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # loop = asyncio.get_event_loop()
    # pool = loop.run_until_complete(init_database_connection())
    # # loop.run_until_complete(insert_server(pool, 1738, False))
    # # loop.run_until_complete(insert_user(pool, 14, 1738, False))
    # # loop.run_until_complete(insert_user_message(pool, 17, 14, 1738, 'big message', 'sent', datetime.now()))
    # # loop.run_until_complete(insert_catalogue_alias(pool, 'I&C SCI', 'ICS', 1738))
    # # result = loop.run_until_complete(request_user_logs(pool, 14, 1738))
    # result = loop.run_until_complete(request_catalogue_aliases(pool)).items()
    # print(type(result))
    test = defaultdict(set)
    test['item'].add(1)
    print(test)

