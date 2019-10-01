# Vethorm

Vethorm is a discord bot currently written in python using the discord.py API wrapper

Source: [discord.py](https://github.com/Rapptz/discord.py)

This branch is the work-in-progress of the rewrite. The original version of the discord bot was written and developed while I was learning python.
The rewrite is an attempt to improve on the original with

* cleaner code

   Many functions are not written in the cleanest way, nor is the structure of the project very clean.
   Most of the project was written without a specific direction in mind. The rewrite aims to fix this

* more modularity

   Certain pieces of the code aren't very modular or independently testable in an accessible way.

* improve performance

   Many areas contain poor performance, namely storing and updating the guild data for the bot.
   Most of the data for the bot is stored in text files which is most likely causing performance issues as files start to scale.
   One main solution planned is to introduce the existance of a database to store all of the data. Which database I will use has yet to be determined but it will most likely be either MongoDB or Postgre

* scalability

   I plan to develop the bot so it can be added to more than just the UCI server and still use the functionality

### TODO List

* create more testable portions of code
* clean up messy functions
* implement the addition of a database (MongoDB or Postgre)
* build a web interface for others to interact with the bot and set options
* implement caching to various data handling portions
  * Catalogue Scraper
  * Tags?
* After database implementation look into doing batch inserts for user logs and performance gains vs complexity


# Vethorm
This is a bot for a school discord server

## Setup

### Install postgres

> sudo apt install postgresql postgresql-contrib

Create user

> sudo -u postgres createuser --interactive
User should be "vethorm" and a superuser

Create database

> sudo -u postgres createdb vethorm

Add user

> sudo adduser vethorm

Log with

> sudo -i -u vethorm
> psql
or
> sudo -u vethorm psql

### Create Postgre database

This command assumes you are in the base directory `Vethorm`

If you are in another directory you will need to change the directory following `-f`

> sudo -u vethorm psql -f postgre_files/create_vethorm_database.sql vethorm

### Create Secret

Assumes you are in base directory

> touch utilities/secret.py

Add the following to secret.py

```
# POSTGRES
HOST = 'postgre database address'
PORT = 'postgre port' # this should be an int not a string
USERNAME = 'vethorm'
PASSWORD = 'password created for psql account vethorm'
DATABASE_NAME = 'database name'

# DISCORD
BOT_TOKEN = 'your bot token'

# USERS
OWNER = 'your discord id' # this should be an int not a string

# ALERT - if you want to disable alerts set both to None, id's should be int snowflake id's
PROFILE_ID = 'id to alert' 
LOOKOUT_ID = 'id to watch for'
```




