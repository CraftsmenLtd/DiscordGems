import re
from message_gems_parser import gem_message_string_regex

def replace_gem_template_with_real_gem(message_with_gem_template: str, gem_count: int):
    if '💎' in message_with_gem_template or gem_count == 0:
        return message_with_gem_template
    
    gem_substituted_message = re.sub(gem_message_string_regex, '💎' * gem_count, message_with_gem_template)

    if gem_substituted_message[0] != '💎':
        gem_substituted_message = gem_substituted_message.replace('💎', ' 💎', 1)
    
    gem_last_index = gem_substituted_message.rfind('💎')
    if gem_last_index != -1 and gem_last_index != len(gem_substituted_message) - 1:
        gem_substituted_message = gem_substituted_message[:gem_last_index] + '💎 ' + gem_substituted_message[gem_last_index + 1:]

    return gem_substituted_message
