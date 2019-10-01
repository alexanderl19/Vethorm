
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

# Update functions to match new schema
# TODO: add msg_type check for original, edit, deletion

# FUNCTIONS

async def init_database_connection() -> asyncpg.pool.Pool:
    """
        Creates a connection pool for the bot database

        Return value asyncpg.pool.Pool
    """
    return await asyncpg.create_pool(host=secret.HOST, port=secret.PORT, user=secret.USERNAME, password=secret.PASSWORD, database=secret.DATABASE_NAME)

# Catalogue functions: UNIT TESTED
# Aliases stored by guild id then by alias
async def insert_catalogue_alias(bot: Bot, department: str, alias: str, guild_id: int):
    """
        Inserts a new catalogue alias to the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' 
            INSERT INTO catalogue_alias 
            VALUES ($1, $2, $3)''', department.upper(), guild_id, alias.upper())

            bot.Valiases[guild_id][alias] = department

async def remove_catalogue_alias(bot: Bot, alias: str, guild_id: int):
    """
        Removes a department alias from the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute('''
            DELETE FROM catalogue_alias 
            WHERE guild_id = $1 AND alias = $2''', guild_id, alias.upper())

            del bot.Valiases[guild_id][alias.upper()]

            # to_delete = None
            
            # for alias, dep in bot.Valiases[guild_id].items():
            #     if department == dep:
            #         to_delete = alias

            # if to_delete is not None:
            #     del bot.Valiases[guild_id][alias]

async def request_catalogue_aliases(bot: Bot) -> {str : str}:
    """
        Requests all the aliases from the database and returns as a dictionary

        {
            guild_id : {alias : department, ...},
            ...
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
        SELECT * 
        FROM catalogue_alias
        ''')

        results = defaultdict(dict)
        for row in await stmt.fetch():
            results[row['guild_id']][row['alias']] = row['department']
        return results

# Channel functions: UNIT TESTED
# Stored by guild id then channel id
async def insert_channel(bot: Bot, chan_id, guild_id, watching: bool = False):
    """
        Inserts a channel into the database and updates the channels variable
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO channels VALUES ($1, $2, $3) ''', chan_id, guild_id, watching)

            bot.Vchans[guild_id].add(chan_id)
        
async def remove_channel(bot: Bot, chan_id, guild_id):
    """
        Removes a channel from the database and updates the Vchan bot variable
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' 
            DELETE FROM channels
            WHERE guild_id = $1 AND chan_id = $2
            ''', guild_id, chan_id)

            bot.Vchans[guild_id].discard(chan_id)

async def insert_channel_message(bot: Bot, message_id: int, chan_id: int, guild_id: int, message: str, message_type: str, date: datetime, user_id: int, ):
    """
        Inserts a channel message into the database
    """
    # print(f'INSERT: {message_id}, {chan_id}, {guild_id}, {message}, {message_type}, {date}, {user_id}')
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' 
                INSERT INTO channel_logs (message_id, channel_id, guild_id, msg, msg_type, msg_date, user_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7) ''', message_id, chan_id, guild_id, message, message_type, date, user_id)
            # print(f'INSERT: {message_id}, {chan_id}, {guild_id}, {message}, {message_type}, {date}')

async def request_channel_logs(bot: Bot, chan_id: int, guild_id: int) -> [dict]:
    """
        Requests all the channel logs for a channel and a list of dictionary objects representing the message
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * 
            FROM channel_logs 
            WHERE chan_id = $1 AND guild_id = $2
            ORDER BY msg_date DESC
            ''')
        return [{
            'message_id'    : item['message_id'],
            'user_id'       : item['user_id'],
            'channel_id'    : item['chan_id'],
            'guild_id'      : item['guild_id'],
            'msg'           : item['msg'],
            'msg_type'      : item['msg_type'],
            'msg_date'      : item['msg_date']
        } for item in await stmt.fetch(chan_id, guild_id)]

async def request_channels(bot: Bot):
    """
        Requests all the registered channels

        {
            guild_id : set(chan_id, ...)
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare('''
        SELECT * FROM channels
        ''')

        results = defaultdict(set)

        for item in await stmt.fetch():
            results[item['guild_id']].add(item['chan_id'])
        
        return results

# Guild functions: UNIT TESTED
async def insert_guild(bot: Bot, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new server to the database and updates the servers variable
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO guilds VALUES ($1, $2) ''', guild_id, watch_mode)

            bot.Vguilds[guild_id]['watch_mode'] = watch_mode

async def remove_guild(bot: Bot, guild_id):
    """
        Removes a guild from the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute('''
            DELETE FROM guilds
            WHERE guild_id = $1
            ''', guild_id)

            del bot.Vguilds[guild_id]

async def update_guild_watch_mode(bot: Bot, guild_id: int, watch_mode: bool):
    """
        Updates a server watch mode
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' UPDATE guilds SET watch_mode = $1 WHERE guild_id = $2 ''', watch_mode, guild_id)

            bot.Vguilds[guild_id]['watch_mode'] = watch_mode

async def request_guilds(bot: Bot) -> {int: dict}:
    """
        Returns a dictionary of guilds where they key is the guild id and the value is attributes of the server

        {
            guild_id : { watch_mode : bool },
            ...
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' SELECT * FROM guilds ''')

        results = defaultdict(dict)
        
        for row in await stmt.fetch():
            results[ row[ 'guild_id' ] ][ 'watch_mode' ] = row[ 'watch_mode' ]

        return  results

# Tag functions: UNIT TESTED
async def insert_tag(bot: Bot, tag: str, guild_id: int, info: str):
    """
        Inserts a tag into the database and updates the tags variable for the bot
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO tags VALUES ($1, $2, $3) ''', tag, guild_id, info)
            bot.Vtags[guild_id][tag] = info

async def remove_tag(bot: Bot, tag: str, guild_id: int):
    """
        Removes a tag into the database and updates the tags variable for the bot
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' DELETE FROM tags WHERE guild_id = $1 AND tag = $2 ''', guild_id, tag)
            del bot.Vtags[guild_id][tag]

async def request_tags(bot: Bot) -> {int: dict}:
    """
        Requests the tags from the database and returns them as a dictionary

        {
            guild_id : {tag : info, ...},
            ...
        }
    """
    async with bot.Vpool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * FROM tags
            ''')

        tags = defaultdict(dict)
        for row in await stmt.fetch():
            tags[ row[ 'guild_id' ] ][ row[ 'tag' ] ] = row[ 'info' ]

        return tags

# User functions: UNIT TESTED
async def insert_user(bot: Bot, user_id: int, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new user to the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO users VALUES ($1, $2) ''', user_id, guild_id)
            bot.Vusers[guild_id].add(user_id)

async def remove_user(bot: Bot, user_id: int, guild_id: int):
    """
        Removes a user from the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute('''
            DELETE FROM users
            WHERE user_id = $1 AND guild_id = $2
            ''', user_id, guild_id)

            bot.Vusers[guild_id].discard(user_id)

async def insert_user_message(bot: Bot, message_id:int, user_id: int, guild_id: int, message: str, message_type: str, date: datetime):
    """
        Inserts a new user message into the database
    """
    async with bot.Vpool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' 
                INSERT INTO user_logs(message_id, user_id, guild_id, msg, msg_type, msg_date) 
                VALUES ($1, $2, $3, $4, $5, $6) 
                ''', message_id, user_id, guild_id, message, message_type, date)
            # print(f'INSERT: {message_id}, {user_id}, {guild_id}, {message}, {message_type}, {date}')

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
            ORDER BY msg_date DESC
            ''')
        return [{
            'message_id'    : item['message_id'],
            'user_id'       : item['user_id'],
            'guild_id'      : item['guild_id'],
            'msg'           : item['msg'],
            'msg_type'      : item['msg_type'],
            'msg_date'      : item['msg_date']
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
            results[item['guild_id']].add(item['user_id'])
        return results




# MAIN

if __name__ == '__main__':
    pass
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
    # test = defaultdict(set)
    # test['item'].add(1)
    # print(test)

