from dataclasses import dataclass
from typing import List, Optional

import discord

intents = discord.Intents.default()
intents.message_content = True


@dataclass
class Message:
    discord_id: int
    content: str
    file_path: Optional[str] = None


def send_channel_message(bot_token: str, channel_id: int, message: str):
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send(message)
        await client.close()

    client.run(bot_token)
