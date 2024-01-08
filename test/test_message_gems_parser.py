from src.message_gems_parser import get_gem_count_in_message
from src import emojis


def test_message_with_gem_returns_correct_gem_count():
    gems_count = get_gem_count_in_message(f'{emojis.GEM*3} for the help')
    assert gems_count == 3


def test_message_with_no_gem_returns_0_gem_count():
    gems_count = get_gem_count_in_message('no gems given')
    assert gems_count == 0


def test_message_with_extra_gem_returns_correct_gem_count():
    gems_count = get_gem_count_in_message(f'{emojis.GEM*6} for the help')
    assert gems_count == 6


def test_message_with_gem_string_returns_correct_gem_count():
    gems_count = get_gem_count_in_message('gems-2 for the help')
    assert gems_count == 2


def test_message_with_1000_gem_string_returns_correct_gem_count():
    gems_count = get_gem_count_in_message('gems-1000 for the help')
    assert gems_count == 1000


def test_message_with_0_gem_string_returns_correct_gem_count():
    gems_count = get_gem_count_in_message('gems-0 for the help')
    assert gems_count == 0


def test_message_with_gem_string_with_multiple_spaces_returns_correct_gem_count():
    gems_count = get_gem_count_in_message('  gems-2  for the help')
    assert gems_count == 2


def test_message_with_multiple_gem_strings_returns_first_gem_count():
    gems_count = get_gem_count_in_message('gems-2 gems-3 for the help')
    assert gems_count == 2


def test_message_with_multiple_hyphens_in_gem_string_returns_integer_gem_count():
    gems_count = get_gem_count_in_message('gems------3---- for the help')
    assert gems_count == 0


def test_message_with_decimal_number_gem_string_returns_0_gem_count():
    gems_count = get_gem_count_in_message('gems-10.12 for the help')
    assert gems_count == 0


def test_message_with_gem_string_with_string_returns_0_gem_count():
    gems_count = get_gem_count_in_message('gems-abcd for the help')
    assert gems_count == 0


def test_message_with_gem_string_with_string_hyphen_number_returns_0_gem_count():
    gems_count = get_gem_count_in_message('gems-abcd-10 for the help')
    assert gems_count == 0


def test_message_with_gem_string_with_string_and_number_returns_0_gem_count():
    gems_count = get_gem_count_in_message('gems-abcd10 for the help')
    assert gems_count == 0


def test_message_with_multiple_gem_strings_together_returns_0_count():
    gems_count = get_gem_count_in_message('gems-2gems-3 for the help')
    assert gems_count == 0


def test_message_with_valid_and_invalid_gem_strings_returns_valid_count():
    gems_count = get_gem_count_in_message('gems-abcde gems-3 for the help')
    assert gems_count == 3


def test_message_with_no_gem_string_returns_0_gem_count():
    gems_count = get_gem_count_in_message('no gems given')
    assert gems_count == 0


def test_message_with_gem_and_gem_string_returns_gem_count():
    gems_count = get_gem_count_in_message(
        f'{emojis.GEM*3} gems-5 for the help')
    assert gems_count == 3


def test_message_with_gem_string_and_gem_returns_gem_count():
    gems_count = get_gem_count_in_message(
        f'gems-5 {emojis.GEM*3} for the help')
    assert gems_count == 3
