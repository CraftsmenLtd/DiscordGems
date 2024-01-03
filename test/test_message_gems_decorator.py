from src.message_gems_decorator import replace_gem_template_with_real_gem
from src import emojis


def test_message_with_gem_template_string_constructs_message_with_correct_gem_count():
    undecorated_message = 'gems-4 for the help'
    gem_count = 4
    result = replace_gem_template_with_real_gem(undecorated_message, gem_count)
    expected = f'{emojis.GEM*4} for the help'
    assert result == expected


# def test_message_with_gem_template_string_constructs_message_with_zero_gem_count():
#     undecorated_message = 'gems-0 for the help'
#     gem_count = 0
#     result = replace_gem_template_with_real_gem(undecorated_message, gem_count)
#     expected = 'for the help'
#     assert result == expected


# def test_message_with_multiple_gem_template_string_constructs_message_with_first_converted_to_gem():
#     undecorated_message = f'{emojis.GEM*4} gems-3 for the help'
#     result = replace_gem_template_with_real_gem(undecorated_message, 4)
#     expected = 'gems-4 gems-3 for the help'
#     assert result == expected


# def test_message_with_gem_template_string_and_gem_remains_unchanged():
#     undecorated_message = f'{emojis.GEM*3} gems-4 for the help'
#     result = replace_gem_template_with_real_gem(undecorated_message, 3)
#     expected = f'{emojis.GEM*3} gems-4 for the help'
#     assert result == expected


# def test_message_with_gem_template_string_in_middle_constructs_message_with_correct_gem_count():
#     undecorated_message = f'giving {emojis.GEM*3} to you for the help'
#     result = replace_gem_template_with_real_gem(undecorated_message, 3)
#     expected = 'giving gems-3 to you for the help'
#     assert result == expected


# def test_message_with_invalid_gem_template_string_remains_unchanged():
#     undecorated_message = 'gems-1234abcd for the help'
#     result = replace_gem_template_with_real_gem(undecorated_message, 0)
#     expected = 'gems-1234abcd for the help'
#     assert result == expected
