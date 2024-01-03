"""Discord slash command helpers"""
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from message_gems_parser import get_gem_count_in_message


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
    def from_slash_command(cls, body: Dict[str, Any],
                           gem_counter: Callable = get_gem_count_in_message):
        sender: Dict[str, Any] = body["member"]["user"]
        gems_message = cls(
            sender_discord_id=sender["id"],
            sender_username=sender["username"],
            receiver_discord_id="",
        )

        options: List[Dict[str, Any]] = body["data"]["options"][0]["options"]
        for option in options:
            option_name: Optional[str] = option.get("name")
            if option_name == "user":
                gems_message.receiver_discord_id = option["value"]
            elif option_name == "gems":
                gems_message.gem_message = option["value"]
                gems_message.gem_count = gem_counter(gems_message.gem_message)

        receiver_resolved: Dict[str, Any] = body["data"]["resolved"]
        is_role: bool = bool(receiver_resolved.get("roles", False))
        is_bot: bool = receiver_resolved.get("users", {}).get(
            gems_message.receiver_discord_id, {}).get("bot", False)

        gems_message.is_invalid_receiver = is_bot or is_role
        if not gems_message.is_invalid_receiver:
            gems_message.receiver_username = receiver_resolved[
                "users"][gems_message.receiver_discord_id]["username"]

        return gems_message

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
