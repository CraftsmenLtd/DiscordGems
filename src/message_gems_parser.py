"""Process formatted gem message"""
import re

import emojis

gem_template_string_anchor = 'gems-'
gem_message_string_regex = fr'(?:\s|^){gem_template_string_anchor}\d+(?:\s|$)'


def get_gem_count_from_gem_string(message: str):
    probable_gem_message_word = re.search(gem_message_string_regex, message)
    if not probable_gem_message_word:
        return 0

    gem_message_word = probable_gem_message_word.group().strip()
    return int(gem_message_word[len(gem_template_string_anchor):])


def get_gem_count_in_message(message: str):
    gem_count_in_message = message.count(emojis.GEM)
    if gem_count_in_message > 0:
        return gem_count_in_message

    return get_gem_count_from_gem_string(message)
