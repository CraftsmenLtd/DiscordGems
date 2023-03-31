import collections
import os
from typing import List, Set, Type

LAMBDA_ENVIRONMENT_VARIABLES: Set[str] = {
    "gems_table_name",
    "discord_public_key_secrets_arn",
    "max_gems_per_day",
    "discord_gems_channel",
    "monthly_cron_rule",
    "discord_bot_token_secret_arn",
}


def load_environment_variables():
    """Check that all required configuration is present at runtime.

    :return: A named tuple, where each key is the variable key, and
        it's value the environment variable value.
    :rtype: collections.namedtuple
    """
    config_object: Type[tuple] = collections.namedtuple(
        "EnvironmentVariables", list(LAMBDA_ENVIRONMENT_VARIABLES))
    _configs: List[str] = []
    for _variable_key in LAMBDA_ENVIRONMENT_VARIABLES:
        _configs.append(os.environ[_variable_key])
    return config_object(*_configs)
