import unittest
from ..path.path_helper import PathHelper


class TestPath(unittest.TestCase):
    def test_backward_steps(self):
        print(PathHelper.from_root(__file__, root_name="tests"))
        self.assertTrue(1)


if __name__ == "__main__":
    unittest.main()
