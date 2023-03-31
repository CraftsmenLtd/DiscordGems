import os

from register_bot_command import register_command

COMMAND = os.environ["COMMAND"]
APP_ID = os.environ["APP_ID"]
GUILD_ID = os.environ["GUILD_ID"]
BOT_TOKEN = os.environ["BOT_TOKEN"]


if __name__ == "__main__":
    register_command(COMMAND, APP_ID, GUILD_ID, BOT_TOKEN)
