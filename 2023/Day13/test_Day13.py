import Day13
import numpy as np
import unittest


class Tests(unittest.TestCase):
    data = list(Day13.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            np.array([[1, 0, 1, 1, 0, 0, 1, 1, 0],
                      [0, 0, 1, 0, 1, 1, 0, 1, 0],
                      [1, 1, 0, 0, 0, 0, 0, 0, 1],
                      [1, 1, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 1, 0, 1, 1, 0, 1, 0],
                      [0, 0, 1, 1, 0, 0, 1, 1, 0],
                      [1, 0, 1, 0, 1, 1, 0, 1, 0]], dtype=bool),
            np.array([[1, 0, 0, 0, 1, 1, 0, 0, 1],
                      [1, 0, 0, 0, 0, 1, 0, 0, 1],
                      [0, 0, 1, 1, 0, 0, 1, 1, 1],
                      [1, 1, 1, 1, 1, 0, 1, 1, 0],
                      [1, 1, 1, 1, 1, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0, 0, 1, 1, 1],
                      [1, 0, 0, 0, 0, 1, 0, 0, 1]], dtype=bool)
        ]
        np.testing.assert_array_equal(self.data, expected)

    def test_solve(self):
        result = Day13.solve(self.data)
        self.assertEqual(result, (405, 400))


if __name__ == '__main__':
    unittest.main()
