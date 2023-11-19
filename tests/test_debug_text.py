import unittest
from ..debug_tools.debug_text import debug_text


class test_debug_text(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_nested_objects(self):
        debug_text("%B%USome Object%E [%c#%%E] -> %r%%E", 12, {"a": 34})
        self.assertTrue(True)
