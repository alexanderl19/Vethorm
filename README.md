# Vethorm

Vethorm is a discord bot currently written in python using the discord.py API wrapper

Source: [discord.py](https://github.com/Rapptz/discord.py)

This branch is the work-in-progress of the rewrite. The original version of the discord bot was written and developed while I was learning python.
The rewrite is an attempt to improve on the original with
* cleaner code
.. Many functions are not written in the cleanest way, nor is the structure of the project very clean.
.. Most of the project was written without a specific direction in mind. The rewrite aims to fix this

* more modularity
.. Certain pieces of the code aren't very modular or independently testable in an accessible way.

* improve performance
.. Many areas contain poor performance, namely storing and updating the guild data for the bot.
.. Most of the data for the bot is stored in text files which is most likely causing performance issues as files start to scale.
.. One main solution planned is to introduce the existance of a database to store all of the data. Which database I will use has yet to be determined but it will most likely be either MongoDB or Postgre

* scalability
.. I plan to develop the bot so it can be added to more than just the UCI server and still use the functionality


### TODO List
* create more testable portions of code
* clean up messy functions
* implement the addition of a database (MongoDB or Postgre)
* build a web interface for others to interact with the bot and set options
* implement caching to various data handling portions
..* Catalogue Scraper
..* Tags?
* After database implementation look into doing batch inserts for user logs and performance gains vs complexity


