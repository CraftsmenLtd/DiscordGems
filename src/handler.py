"""Discord gems entrypoint"""
import calendar
import datetime
import json
import logging
from typing import Any, Dict, List

from nacl.signing import VerifyKey

from command import GemsMessage, is_rank_command, slash_command_response
from communication import send_channel_message
from constants import load_environment_variables
from dynamo import (get_monthly_rank, insert_gem_to_dynamo,
                    sender_gem_count_today)
from secrets_manager_helper import get_secret

PING_PONG = {"type": 1}

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
        # TODO: add discord public key in lambda cache
        verify_signature(event, get_secret(env_vars.discord_public_key_secrets_arn))
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
    if body.get("channel_id") != env_vars.discord_gems_channel:
        return slash_command_response(
            f"Use channel <#{env_vars.discord_gems_channel}> to give 💎"
        )

    try:
        if is_rank_command(body):
            return handle_rank_command()

        gems_message: GemsMessage = GemsMessage.from_slash_command(body)
        LOGGER.info(f"Gem message: {gems_message}")

        if gems_message.sender_discord_id == gems_message.receiver_discord_id:
            return slash_command_response("You can not give 💎 to yourself")

        if gems_message.is_invalid_receiver:
            return slash_command_response("Invalid 💎 receiver")

        if not gems_message.gem_count:
            return slash_command_response("No 💎 found in message")

        max_gem: int = int(env_vars.max_gems_per_day)
        gems_today: int = sender_gem_count_today(
            gems_message.sender_discord_id)
        if gems_today + gems_message.gem_count <= max_gem:
            insert_gem_to_dynamo(gems_message)
            return slash_command_response(
                f"{gems_message.sender_username} to "
                f"<@{gems_message.receiver_discord_id}>: "
                f"{gems_message.gem_message}"
            )
        else:
            return slash_command_response(
                f"You have {max_gem - gems_today} 💎 left for today"
            )
    except Exception as error:
        LOGGER.error(f"Command failed with {error}")

    return slash_command_response("Message parsing failed. Please contact with admin.")


def _handle_trigger_from_cron(env_vars):
    discord_bot_token: str = get_secret(
        env_vars.discord_bot_token_secret_arn
    )

    last_month_last_day = datetime.datetime.today().replace(day=1) - datetime.timedelta(
        days=1
    )
    month: int = last_month_last_day.month
    rank: Dict[str, int] = get_monthly_rank(month, last_month_last_day.year)

    message: str = _rank_message(
        rank, f"Top members of {calendar.month_name[month]}")

    send_channel_message(
        discord_bot_token,
        int(env_vars.discord_gems_channel),
        message
    )


def handle_rank_command():
    """Rank command to view current month top 5 members"""
    today = datetime.datetime.today()
    rank: Dict[str, int] = get_monthly_rank(
        today.month, today.year
    )
    message: str = _rank_message(rank, "Top members of this month")
    return slash_command_response(message)


def _rank_message(rank: Dict[str, int], headline: str, max_count: int = 5) -> str:
    if not rank:
        message: str = "No 💎 found to make rank 😢"
    else:
        message: str = f"{headline}\n--------------"
        top_rank_count: int = 0
        for discord_id, gems in rank.items():
            message += f"\n<@{discord_id}>: {gems}"
            top_rank_count += 1
            if top_rank_count == max_count:
                break

    return message
