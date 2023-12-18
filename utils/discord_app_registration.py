"""Configure the discord bot"""
import requests


class DiscordAppRegistration:
    """Class to register the discord bot"""
    base_url: str = "https://discord.com/api"

    def __init__(self, app_id: str, bot_token: str):
        self.app_id = app_id
        self.bot_token = bot_token

    def register_command(self, command: str, guild_id: str):
        """Register a discord bot slash command

        :param command: discord slash command to register
        :param guild_id: discord server id
        """
        url = f"{self.base_url}/v8/applications/{self.app_id}/guilds/{guild_id}/commands"

        payload = {
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
                },
                {
                    "name": "opt-out",
                    "description": "Opt-out from receiving gem",
                    "type": 1
                },
                {
                    "name": "opt-in",
                    "description": "Opt-in to receive gem",
                    "type": 1
                }
            ]
        }

        response = requests.post(url, headers={
            "Authorization": f"Bot {self.bot_token}"
        }, json=payload)
        response.raise_for_status()
        return response.json()

    def add_interaction_endpoint_url(self, endpoint_url: str):
        """Add an interaction endpoint url to discord bot

        :param endpoint_url: the endpoint url to which discord bot will send slash commands
        """
        url = f"{self.base_url}/v9/applications/{self.app_id}"

        payload = {
            "interactions_endpoint_url": endpoint_url,
        }

        response = requests.patch(url, headers={
            "Authorization": f"Bot {self.bot_token}"
        }, json=payload)
        response.raise_for_status()
        return response.json()
