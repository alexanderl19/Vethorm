
# STL

import asyncio
from datetime import datetime

# THIRD PARTY

import asyncpg

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

async def insert_catalogue_alias(pool: asyncpg.pool.Pool, course_id: str, alias: str, guild_id: int):
    """
        Inserts a new catalogue alias to the database
    """
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO catalogue_alias VALUES ($1, $2, $3)''', course_id, guild_id, alias)

async def insert_channels(pool: asyncpg.pool.Pool, channel_id, guild_id, watching: bool = False):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO channels VALUES ($1, $2, $3) ''', channel_id, guild_id, watching)

async def insert_channel_message(pool: asyncpg.pool.Pool, message_id:int, channel_id: int, guild_id: int, message: str, message_type: str, date: datetime):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO user_logs VALUES ($1, $2, $3, $4, $5, $6) ''', message_id, channel_id, guild_id, message, message_type, date)

async def insert_server(pool: asyncpg.pool.Pool, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new server to the database
    """
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO servers VALUES ($1, $2) ''', guild_id, watch_mode)

async def insert_tag(pool: asyncpg.pool.Pool, tag: str, guild_id: int, info: str):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO tags VALUES ($1, $2, $3) ''', tag, guild_id, info)

async def insert_user_message(pool: asyncpg.pool.Pool, message_id:int, user_id: int, guild_id: int, message: str, message_type: str, date: datetime):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO user_logs VALUES ($1, $2, $3, $4, $5, $6) ''', message_id, user_id, guild_id, message, message_type, date)

async def insert_user(pool: asyncpg.pool.Pool, id: int, guild_id: int, watch_mode: bool = False):
    """
        Inserts a new user to the database
    """
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(''' INSERT INTO users VALUES ($1, $2, $3) ''', id, guild_id, watch_mode)

async def request_catalogue_aliases(pool: asyncpg.pool.Pool) -> {str : str}:
    async with pool.acquire() as conn:
        stmt = await conn.prepare(''' SELECT * FROM catalogue_alias ''')

        return {item['course_id'] : item['alias'] for item in await stmt.fetch()}

async def request_channel_logs(pool: asyncpg.pool.Pool, channel_id: int, guild_id: int):
    async with pool.acquire() as conn:
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

async def request_servers(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:
        stmt = await conn.prepare(''' SELECT * FROM servers ''')
        return [{
            'guild_id'   : item['id'],
            'watch_mode' : item['watch_mode']
        } for item in await stmt.fetch()]

async def request_tags(pool: asyncpg.pool.Pool, guild_id: int):
    async with pool.acquire() as conn:
        stmt = await conn.prepare(''' 
            SELECT * FROM tags 
            WHERE guild_id = $1 
            ''')
        return [{
            'tag'  : item['tag'],
            'info' : item['info']
        } for item in await stmt.fetch(guild_id)]
        
async def request_user_logs(pool: asyncpg.pool.Pool, user_id: int, guild_id: int):
    async with pool.acquire() as conn:
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

# MAIN

if __name__ == '__main__':
    print(' ==== VQUERIES MAIN EXECUTION ==== ')
    try:
        import uvloop
    except ImportError:
        print("uvloop was unable to import\n"
            "regular asyncio will run instead of uvloop")
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(init_database_connection())
    loop.run_until_complete(test(pool))
    loop.run_until_complete(insert_server(pool, 1738, False))
    loop.run_until_complete(insert_user(pool, 14, 1738, False))
    loop.run_until_complete(insert_user_message(pool, 17, 14, 1738, 'big message', 'sent', datetime.now()))
    loop.run_until_complete(insert_catalogue_alias(pool, 'I&C SCI', 'ICS', 1738))
    result = loop.run_until_complete(request_user_logs(pool, 14, 1738))
    print(result)

