from src.message_gems_decorator import replace_gem_template_with_real_gem
from src import emojis


def test_should_return_4_gem_count_for_gems_4_template_string():
    undecorated_message = 'gems-4 for the help'
    gem_count = 4
    result = replace_gem_template_with_real_gem(undecorated_message, gem_count)
    expected = f'{emojis.GEM*4} for the help'
    assert result == expected


def test_should_return_0_gem_count_for_gems_0_template_string():
    undecorated_message = 'gems-0 for the help'
    gem_count = 0
    result = replace_gem_template_with_real_gem(undecorated_message, gem_count)
    expected = 'gems-0 for the help'
    assert result == expected


def test_should_return_gem_count_from_first_template_string_for_multiple_template_strings():
    undecorated_message = 'gems-4 gems-3 for the help'
    result = replace_gem_template_with_real_gem(undecorated_message, 4)
    expected = f'{emojis.GEM*4} gems-3 for the help'
    assert result == expected


def test_should_return_unchanged_message_for_gem_emoji_and_template_string():
    undecorated_message = f'{emojis.GEM*3} gems-4 for the help'
    result = replace_gem_template_with_real_gem(undecorated_message, 3)
    expected = f'{emojis.GEM*3} gems-4 for the help'
    assert result == expected


def test_should_return_correct_gem_count_for_template_string_in_middle():
    undecorated_message = 'giving gems-3 to you for the help'
    result = replace_gem_template_with_real_gem(undecorated_message, 3)
    expected = f'giving {emojis.GEM*3} to you for the help'
    assert result == expected


def test_should_return_unchanged_message_for_invalid_template_string():
    undecorated_message = 'gems-1234abcd for the help'
    result = replace_gem_template_with_real_gem(undecorated_message, 0)
    expected = 'gems-1234abcd for the help'
    assert result == expected
