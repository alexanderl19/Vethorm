# STANDARD LIBRARY

import asyncio
import json
import sys

# THIRD PARTY IMPORTS

import discord
from discord.ext import commands

try:
    import uvloop
except ImportError:
    print('uvloop failed to import', file=sys.stderr)
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# PROJECT

from bot import Vethorm

# CONSTANTS



# FUNCTIONS

def run_bot():
    bot = Vethorm()
    bot.run()

def main():
    run_bot()

# MAIN

if __name__ == '__main__':
    main()

