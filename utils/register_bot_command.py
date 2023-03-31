# global commands are cached and only update every hour
import logging

import requests

# while guild commands update instantly
# they're much better for testing

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def register_command(command: str, app_id: str, guild_id: str, bot_token: str):
    """Register a discord bot slash command"""
    url = f"https://discord.com/api/v8/applications/{app_id}/guilds/{guild_id}/commands"

    json = {
        "name": command,
        "type": 1,
        "description": "Appreciate someone by gem",
        "options": [
            {
                "name": "rank",
                "description": "Get rank",
                "type": 1
            },
            {
                "name": "appreciate",
                "description": "Give gem to someone",
                "type": 1,
                "options": [
                    {
                        "name": "user",
                        "description": "Mention the user to give gem",
                        "type": 9,
                        "required": True
                    },
                    {
                        "name": "gems",
                        "description": "provide gems with :gem: emoticon and add reason",
                        "type": 3,
                        "required": True
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers={
        "Authorization": f"Bot {bot_token}"
    }, json=json)

    print(response.json())
