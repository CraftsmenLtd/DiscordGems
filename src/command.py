"""Discord slash command helpers"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class GemsMessage:
    sender_discord_id: str
    sender_username: str
    receiver_discord_id: str
    receiver_username: Optional[str] = None
    is_invalid_receiver: bool = False
    gem_message: Optional[str] = None
    gem_count: int = 0

    @classmethod
    def from_slash_command(cls, body: Dict[str, Any]):
        options: List[Dict[str, Any]] = body["data"]["options"][0]["options"]
        for option in options:
            option_name: Optional[str] = option.get("name")
            if option_name == "user":
                cls.receiver_discord_id = option["value"]
            elif option_name == "gems":
                cls.gem_message = option["value"]
                cls.gem_count = cls.gem_message.count("💎")

        receiver_resolved: Dict[str, Any] = body["data"]["resolved"]
        is_role: bool = bool(receiver_resolved.get("roles", False))
        is_bot: bool = receiver_resolved.get("users", {}).get(
            cls.receiver_discord_id, {}).get("bot", False)
        cls.is_invalid_receiver = is_bot or is_role
        if not cls.is_invalid_receiver:
            cls.receiver_username = receiver_resolved["users"][cls.receiver_discord_id]["username"]
        cls.sender_username = body["member"]["user"]["username"]
        cls.sender_discord_id = body["member"]["user"]["id"]
        return cls

    def __repr__(self):
        return f"Sender username: {self.sender_username}\n" \
               f"Receiver username: {self.receiver_username}\n" \
               f"Gem message: {self.gem_message}"


def is_rank_command(body: Dict[str, Any]) -> bool:
    """Check if the command is for ranking"""
    for option in body["data"]["options"]:
        if option.get("name") == "rank":
            return True
    return False


def slash_command_response(content: str):
    """Slash command response"""
    return {
        "type": 4,
        "data": {
            "content": content
        }
    }
