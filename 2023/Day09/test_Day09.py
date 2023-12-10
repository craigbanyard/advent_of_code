import Day09
import numpy as np
import unittest


class Tests(unittest.TestCase):
    data = Day09.get_input('sample.txt')

    def test_get_input(self):
        expected = np.array(
            [[0,  3,  6,  9, 12, 15],
             [1,  3,  6, 10, 15, 21],
             [10, 13, 16, 21, 30, 45]]
        )
        np.testing.assert_array_equal(self.data, expected)

    def test_extrapolate_forwards(self):
        result = Day09.extrapolate(self.data[0])
        self.assertEqual(result, 18)

    def test_extrapolate_backwards(self):
        result = Day09.extrapolate(self.data[0][::-1])
        self.assertEqual(result, -3)

    def test_solve_part1(self):
        result = Day09.solve(self.data)
        self.assertEqual(result, 114)

    def test_solve_part2(self):
        result = Day09.solve(np.fliplr(self.data))
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
