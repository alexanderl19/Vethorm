import json
import os


def build_app_structure() -> None:
    '''builds the application structure for necessary data management files'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    os.makedirs("data", exist_ok=True)
    os.makedirs("data/watching", exist_ok=True)
    os.makedirs("data/watching/users", exist_ok=True)

    if not os.path.isfile("data/guild_data.json"):
        with open("data/guild_data.json", "w") as file:
            file.write("{}")


def load_guild_data() -> dict():
    '''loads guild data from a json file to a dictionary'''
    with open("data/guild_data.json") as file:
        return json.load(file)


def write_to_user_watch_file(snowflake: str, message: str) -> None:
    '''writes to a users watch file'''
    if not os.path.isfile("data/watching/users/{id}.txt".format(id=snowflake)):
        with open("data/watching/users/{id}.txt".format(id=snowflake), "a") as file:
            pass
    with open("data/watching/users/{id}.txt".format(id=snowflake), "r+") as file:
        body = file.read()
        file.seek(0)
        file.write(message)
        file.write("\n")
        file.write(body)


def write_to_channel_watch_file(name: str, message: str) -> None:
    '''writes to a channel watch file'''
    '''writes to a channel watch file'''
    if not os.path.isfile("data/watching/channels/{channel_name}.txt".format(channel_name=name)):
        with open("data/watching/channels/{channel_name}.txt".format(channel_name=name), 'a') as file:
            pass
    with open("data/watching/channels/{channel_name}.txt".format(channel_name=name), 'a') as file:
        file.seek(0)
        file.write(message)
        file.write("\n")
        file.write(body)


def setup() -> dict:
    '''runs the setup and returns the loaded data'''
    build_app_structure()
    return load_guild_data()
