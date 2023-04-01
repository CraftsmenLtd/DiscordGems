import logging
import os

from discord_app_registration import DiscordAppRegistration

COMMAND = os.environ["COMMAND"]
APP_ID = os.environ["APP_ID"]
GUILD_ID = os.environ["GUILD_ID"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
INTERACTIONS_ENDPOINT_URL = os.environ["INTERACTIONS_ENDPOINT_URL"]

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    app_registration = DiscordAppRegistration(APP_ID, BOT_TOKEN)
    LOGGER.info(app_registration.register_command(COMMAND, GUILD_ID))
    LOGGER.info(app_registration.add_interaction_endpoint_url(
        INTERACTIONS_ENDPOINT_URL))
