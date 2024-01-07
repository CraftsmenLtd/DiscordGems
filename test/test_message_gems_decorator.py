import unittest
from src.message_gems_decorator import replace_gem_template_with_real_gem
from src import emojis


def assert_decorated_gem_message_correctness(unittest_instance, discord_message, gem_count, expected_message):
    decorated_message = replace_gem_template_with_real_gem(
        discord_message, gem_count)
    unittest_instance.assertEqual(decorated_message, expected_message)
    unittest_instance.assertEqual(
        decorated_message.count(emojis.GEM), gem_count)


class TestGemsMessageDecorator(unittest.TestCase):
    def test_message_with_gem_template_string_constructs_message_with_correct_gem_count(self):
        decorated_message = f'{emojis.GEM*4} for the help'
        assert_decorated_gem_message_correctness(
            self, 'gems-4 for the help', 4, decorated_message)

    def test_message_with_gem_template_string_constructs_message_with_correct_gem_count(self):
        decorated_message = f'{emojis.GEM} for the help'
        assert_decorated_gem_message_correctness(
            self, 'gems-1 for the help', 1, decorated_message)

    def test_message_with_gem_template_string_constructs_message_with_correct_gem_count(self):
        decorated_message = 'gems-0 for the help'
        assert_decorated_gem_message_correctness(
            self, 'gems-0 for the help', 0, decorated_message)

    def test_message_with_multiple_gem_template_string_constructs_message_with_first_converted_to_gem(self):
        decorated_message = f'{emojis.GEM*4} gems-3 for the help'
        assert_decorated_gem_message_correctness(
            self, 'gems-4 gems-3 for the help', 4, decorated_message)

    def test_message_with_gem_template_string_and_gem_remains_unchanged(self):
        decorated_message = f'{emojis.GEM*3} gems-4 for the help'
        assert_decorated_gem_message_correctness(
            self, f'{emojis.GEM*3} gems-4 for the help', 3, decorated_message)

    def test_message_with_gem_template_string_and_gem_remains_unchanged(self):
        decorated_message = f'{emojis.GEM*3} gems-4 for the help'
        assert_decorated_gem_message_correctness(
            self, f'{emojis.GEM*3} gems-4 for the help', 3, decorated_message)

    def test_message_with_gem_template_string_in_middle_constructs_message_with_correct_gem_count(self):
        decorated_message = f'giving {emojis.GEM*3} to you for the help'
        assert_decorated_gem_message_correctness(
            self, 'giving gems-3 to you for the help', 3, decorated_message)

    def test_message_with_invalid_gem_template_string_remains_unchanged(self):
        decorated_message = 'gems-1234abcd for the help'
        assert_decorated_gem_message_correctness(
            self, 'gems-1234abcd for the help', 0, decorated_message)


if __name__ == '__main__':
    unittest.main()
