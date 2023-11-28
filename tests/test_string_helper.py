import unittest
from ..string.string_helper import StringHelper


class TestStringHelper(unittest.TestCase):
    def test_camel_to_snake(self) -> None:
        self.assertEqual(StringHelper.camel_to_snake("AbcdEfgHIJ"), "abcd_efg_hij")
        self.assertEqual(StringHelper.camel_to_snake("ABcd"), "a_bcd")
        self.assertEqual(StringHelper.camel_to_snake("abc"), "abc")
        self.assertEqual(StringHelper.camel_to_snake("ABC"), "abc")
        self.assertEqual(StringHelper.camel_to_snake("AbC"), "ab_c")

    def test_snake_to_camel(self) -> None:
        self.assertEqual(StringHelper.snake_to_camel("a_bcd_efg_hij"), "aBcdEfgHij")
        self.assertEqual(
            StringHelper.snake_to_camel("a_bcd_efg_hij", True), "ABcdEfgHij"
        )


if __name__ == "__main__":
    unittest.main()
