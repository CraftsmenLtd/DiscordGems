"""Discord gems entrypoint"""
import calendar
import datetime
import json
import logging
from typing import Any, Dict, List, Optional

from nacl.signing import VerifyKey

from command import GemsMessage, is_rank_command, is_opt_out_command, is_opt_in_command, slash_command_response
from communication import send_channel_message
from constants import load_environment_variables
from message_gems_decorator import replace_gem_template_with_real_gem
from dynamo import (get_monthly_rank, has_receiver_opted_out, insert_gem_to_dynamo, insert_opt_out,
                    remove_opt_out, sender_gem_count_today, sender_to_receiver_gem_count_today)

PING_PONG = {"type": 1}
MAX_GEMS_TO_SELF_PER_DAY = 1

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def handler(event, _):
    """Discord gems lambda handler"""
    LOGGER.info(f"Lambda event {json.dumps(event)}")

    env_vars = load_environment_variables()
    if _trigger_from_cron(event, env_vars.monthly_cron_rule):
        _handle_trigger_from_cron(env_vars)
        return

    LOGGER.info(f"Discord event body {event.get('body')}")

    # verify the signature
    try:
        verify_signature(event, env_vars.discord_public_key)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    # check if message is a ping
    body: Dict[str, Any] = json.loads(event["body"])
    if body.get("type") == 1:
        return PING_PONG

    return gem_handler(body, env_vars)


def _trigger_from_cron(event: Dict[str, Any], monthly_cron_rule) -> bool:
    resources: List[str] = event.get("resources", [])
    return monthly_cron_rule in resources and event.get("source") == "aws.events"


def verify_signature(event: Dict[str, Any], public_key: str):
    """verify discord bot signature. Raises exception if not valid signature

    :param event: aws lambda event
    :param public_key: discord bot public key
    """
    raw_body: str = event.get("body")
    auth_sig: str = event["headers"].get("x-signature-ed25519")
    auth_ts: str = event["headers"].get("x-signature-timestamp")

    message: bytes = auth_ts.encode() + raw_body.encode()
    verify_key: VerifyKey = VerifyKey(bytes.fromhex(public_key))
    verify_key.verify(message, bytes.fromhex(auth_sig))


def gem_handler(body: Dict[str, Any], env_vars):
    """Handle gems and respond to user"""
    gems_channel: Optional[str] = env_vars.discord_gems_channel
    if gems_channel and body.get("channel_id") != gems_channel:
        return slash_command_response(
            f"**:currency_exchange: Use channel <#{env_vars.discord_gems_channel}> to give 💎s :currency_exchange:**"
        )

    try:
        if is_rank_command(body):
            return handle_rank_command()
        
        if is_opt_out_command(body):
            user_discord_id: str = _get_sender_discord_id(body)
            return handle_opt_out(user_discord_id)    
        
        if is_opt_in_command(body):
            user_discord_id: str = _get_sender_discord_id(body)
            return handle_opt_in(user_discord_id)

        gems_message: GemsMessage = GemsMessage.from_slash_command(body)
        LOGGER.info(f"Gem message: {gems_message}")

        if not has_receiver_opted_out(gems_message.receiver_discord_id):
            return slash_command_response(f"""
                **:pleading_face: {gems_message.receiver_discord_id} has chosen solitude and is temporarily not receiving any gems. 
                Thank you for the acknowledgment, by the way :heart:**
            """)

        if gems_message.sender_discord_id == gems_message.receiver_discord_id:
            return self_gem(gems_message)

        if gems_message.is_invalid_receiver:
            return slash_command_response("**:x: Invalid 💎s receiver :x:**")

        if not gems_message.gem_count:
            return slash_command_response("**:x: No 💎s found in message :x:**")

        max_gem: int = int(env_vars.max_gems_per_day)
        gems_today: int = sender_gem_count_today(
            gems_message.sender_discord_id)
        if gems_today + gems_message.gem_count <= max_gem:
            insert_gem_to_dynamo(gems_message)
            return slash_command_response(
                f"**:heart_eyes: {gems_message.sender_username} to **"
                f"<@{gems_message.receiver_discord_id}>: "
                f"{replace_gem_template_with_real_gem(gems_message.gem_message, gems_message.gem_count)}"
            )
        return slash_command_response(
            f"**:1234: You have {max_gem - gems_today} 💎(s) left for today :1234:**"
        )
    except Exception as error:
        LOGGER.error(f"Command failed with {error}")

    return slash_command_response("**:man_shrugging: Message parsing failed. Please contact with admin :man_shrugging:**")


def _get_sender_discord_id(body: Dict[str, Any]):
    return body["member"]["user"]["id"]


def _handle_trigger_from_cron(env_vars):
    """Handles auto triggers from cron job"""
    last_month_last_day = datetime.datetime.today().replace(day=1) - datetime.timedelta(
        days=1
    )
    month: int = last_month_last_day.month
    rank: Dict[str, int] = get_monthly_rank(month, last_month_last_day.year)

    message: str = _rank_message(
        rank, f"**:calendar: Top members of {calendar.month_name[month]} :calendar:**")

    send_channel_message(
        env_vars.discord_bot_token,
        int(env_vars.discord_gems_channel),
        message
    )


def self_gem(gems_message: GemsMessage):
    """Processes messages where the sender is trying to send gems to themselves"""
    total_gems_given_to_self = sender_to_receiver_gem_count_today(
        gems_message.sender_discord_id, gems_message.receiver_discord_id)
    if total_gems_given_to_self < MAX_GEMS_TO_SELF_PER_DAY:
        insert_gem_to_dynamo(gems_message)
        return slash_command_response(
            f"**:face_holding_back_tears: {gems_message.sender_username} to **"
            f"themselves; they must've needed this one but we don't judge: "
            f"{replace_gem_template_with_real_gem(gems_message.gem_message, gems_message.gem_count)}"
        )
    return slash_command_response("**:x: You can not give more than one 💎s to yourself in one day :x:**")


def handle_opt_out(user_discord_id: str):
    """Opt-out user from receiving gems"""
    if has_receiver_opted_out(user_discord_id):
        expire_on = insert_opt_out(user_discord_id)
        expire_on_readable = datetime.datetime.fromtimestamp(expire_on).strftime('%d-%m-%Y')
        return slash_command_response(f"**:pleading_face: You have successfully opted out of receiving gems, effective until {expire_on_readable}**")
    return slash_command_response(f"**:pleading_face: You are already opted out**")


def handle_opt_in(user_discord_id: str):
    """Opt-in again"""
    if not has_receiver_opted_out(user_discord_id):
        remove_opt_out(user_discord_id)
        return slash_command_response("**:star_struck: You have successfully opted in to receive gems**")
    return slash_command_response(f"**:star_struck: You are already opted in**")


def handle_rank_command():
    """Rank command to view current month top 5 members"""
    today = datetime.datetime.today()
    rank: Dict[str, int] = get_monthly_rank(
        today.month, today.year
    )
    message: str = _rank_message(
        rank, "**:heart_hands: Top 5 most appreciated :gem:s this month :heart_hands:**")
    return slash_command_response(message)


def _rank_message(rank: Dict[str, int], headline: str, max_count: int = 5) -> str:
    if not rank:
        message: str = "No 💎s found to rank 😢"
    else:
        message: str = f"{headline}"
        top_rank_count: int = 0
        for discord_id, gems in rank.items():
            message += f"\n<@{discord_id}>: {gems}"
            top_rank_count += 1
            if top_rank_count == max_count:
                break

    return message
