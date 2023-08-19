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
                gems_message.gem_count = GemsCounterFromMessage().get_gem_count_in_message(gems_message.gem_message)

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


class GemsCounterFromMessage:
    def __get_int_converted_gem_count(self, gem_count_string: str):
        if gem_count_string.isdigit():
            return int(gem_count_string)
        try:
            gem_count_float = float(gem_count_string)
            return int(gem_count_float)
        except ValueError:
            return 0

    def _get_gem_count_from_gem_string(self, message: str):
        gem_message_string_anchor = '$gem-'
        if message.count(gem_message_string_anchor) == 0:
            return 0

        gem_message_words = message.split()
        # consider first $gem-number for multiple $gem-number in message
        for message_segment in gem_message_words:
            if gem_message_string_anchor in message_segment:
                if message_segment.count(gem_message_string_anchor) > 1:
                    return 0
                
                gem_count_string = message_segment.replace(gem_message_string_anchor, '')
                gem_count = self.__get_int_converted_gem_count(gem_count_string)
                if gem_count > 0:
                    return gem_count

        return 0

    def get_gem_count_in_message(self, message: str):
        gem_count_in_message = message.count("💎")
        if gem_count_in_message > 0:
            return gem_count_in_message 
        
        return self._get_gem_count_from_gem_string(message)


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
