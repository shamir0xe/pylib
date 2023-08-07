import unittest
from helpers.path.path_helper import PathHelper


class TestPath(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_backward_steps(self):
        print(PathHelper.from_root(backward_times=4))
        self.assertTrue(1)


if __name__ == "__main__":
    unittest.main()
