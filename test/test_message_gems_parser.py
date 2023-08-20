import unittest
from src.message_gems_parser import get_gem_count_in_message

def assert_gem_count(unittest_instance, discord_message, expected_gems_count):
    gems_count = get_gem_count_in_message(discord_message)
    unittest_instance.assertEqual(gems_count, expected_gems_count)

class TestGemsCounterFromGemMessage(unittest.TestCase):
    def test_message_with_gem_returns_correct_gem_count(self):
        assert_gem_count(self, '💎💎💎 for the help', 3)

    def test_message_with_no_gem_returns_0_gem_count(self):
        assert_gem_count(self, 'no gems given', 0)
    
    def test_message_with_extra_gem_returns_correct_gem_count(self):
        assert_gem_count(self, '💎💎💎💎💎💎 for the help', 6)

class TestGemsCounterFromStringMessage(unittest.TestCase):
    def test_message_with_gem_string_returns_correct_gem_count(self):
        assert_gem_count(self, '$gem-2 for the help', 2)
    
    def test_message_with_1000_gem_string_returns_correct_gem_count(self):
        assert_gem_count(self, '$gem-1000 for the help', 1000)
    
    def test_message_with_0_gem_string_returns_correct_gem_count(self):
        assert_gem_count(self, '$gem-0 for the help', 0)

    def test_message_with_gem_string_with_multiple_spaces_returns_correct_gem_count(self):
        assert_gem_count(self, '  $gem-2  for the help', 2)

    def test_message_with_multiple_gem_strings_returns_first_gem_count(self):
        assert_gem_count(self, '$gem-2 $gem-3 for the help', 2)
    
    def test_message_with_multiple_hyphens_in_gem_string_returns_integer_gem_count(self):
        assert_gem_count(self, '$gem----3 for the help', 0)
    
    def test_message_with_decimal_number_gem_string_returns_0_gem_count(self):
        assert_gem_count(self, '$gem-10.12 for the help', 0)
    
    def test_message_with_gem_string_with_string_returns_0_gem_count(self):
        assert_gem_count(self, '$gem-abcd for the help', 0)
    
    def test_message_with_gem_string_with_string_hyphen_number_returns_0_gem_count(self):
        assert_gem_count(self, '$gem-abcd-10 for the help', 0)

    def test_message_with_gem_string_with_string_and_number_returns_0_gem_count(self):
        assert_gem_count(self, '$gem-abcd10 for the help', 0)
    
    def test_message_with_multiple_gem_strings_together_returns_0_count(self):
        assert_gem_count(self, '$gem-2$gem-3 for the help', 0)
    
    def test_message_with_valid_and_invalid_gem_strings_returns_valid_count(self):
        assert_gem_count(self, '$gem-abcde $gem-3 for the help', 3)

    def test_message_with_no_gem_string_returns_0_gem_count(self):
        assert_gem_count(self, 'no gems given', 0)

class TestGemsAndGemsStringCounterFromMessage(unittest.TestCase):
    def test_message_with_gem_and_gem_string_returns_gem_count(self):
        assert_gem_count(self, '💎💎💎 $gem-5 for the help', 3)
    
    def test_message_with_gem_string_and_gem_returns_gem_count(self):
        assert_gem_count(self, '$gem-5 💎💎💎 for the help', 3)

if __name__ == '__main__':
    unittest.main()