import unittest
import random
from ..json.json_helper import JsonHelper

class TestJsonHelper(unittest.TestCase):
    def setUp(self):
        self.js = {"sdas": 123, "some_array": [{"a": 1}, {"b": "321"}]}

    def test_selector_set_value_star_array(self):
        random_value = random.randint(0, 12345677)
        next_js = JsonHelper.selector_set_value(self.js, "some_array.*.b", random_value)
        bl = next_js["some_array"][0]["b"] == random_value
        bl &= next_js["some_array"][1]["b"] == random_value
        self.assertTrue(bl)

    def test_selector_set_value_index_array(self):
        random_value = random.randint(0, 12345677)
        random_index = random.randint(0, 1)
        next_js = JsonHelper.selector_set_value(
            self.js, "some_array.__{}.b".format(random_index), random_value
        )
        bl = next_js["some_array"][random_index]["b"] == random_value
        bl &= (
            not "b" in next_js["some_array"][1 - random_index]
            or next_js["some_array"][1 - random_index]["b"] != random_value
        )
        self.assertTrue(bl)

    def test_selector_get_value_star_array(self):
        values = JsonHelper.selector_get_value(self.js, "some_array.*.b")
        self.assertEqual(values[1], self.js["some_array"][1]["b"])

    def test_selector_get_Value_index_array(self):
        value = JsonHelper.selector_get_value(self.js, "some_array.__1")
        self.assertEqual(value, self.js["some_array"][1])

    def test_apply_structure_list(self):
        next_js = JsonHelper.apply_stucture(self.js, {"some_array.__1": []})
        self.assertEqual(next_js["some_array"][1], [self.js["some_array"][1]])


if __name__ == "__main__":
    unittest.main()
