"""Format formatted gem message"""
import re

import emojis
from message_gems_parser import gem_message_string_regex


def replace_gem_template_with_real_gem(message_with_gem_template: str, gem_count: int):
    if emojis.GEM in message_with_gem_template or gem_count == 0:
        return message_with_gem_template

    gem_substituted_message = re.sub(
        gem_message_string_regex, emojis.GEM * gem_count, message_with_gem_template)

    if gem_substituted_message[0:len(emojis.GEM)] != emojis.GEM:
        gem_substituted_message = gem_substituted_message.replace(
            emojis.GEM, f' {emojis.GEM}', 1)

    gem_last_index = gem_substituted_message.rfind(emojis.GEM)
    if gem_last_index != -1 and gem_last_index != len(gem_substituted_message) - len(emojis.GEM):
        gem_substituted_message = gem_substituted_message[:gem_last_index] + \
            f'{emojis.GEM} ' + gem_substituted_message[gem_last_index + len(emojis.GEM):]

    return gem_substituted_message
