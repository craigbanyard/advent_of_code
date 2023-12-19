import Day14
import numpy as np
import unittest


class Tests(unittest.TestCase):
    data = Day14.get_input('sample.txt')

    def test_get_input(self):
        expected = np.array(
            [['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
             ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
             ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
             ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
             ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
             ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
             ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
             ['.', '.', '.', '.', '.', '.', '.', 'O', '.', '.'],
             ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
             ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.']]
        )
        np.testing.assert_array_equal(self.data, expected)

    def test_solve_part1(self):
        result = Day14.solve(self.data)
        self.assertEqual(result, 136)

    def test_solve_part2(self):
        result = Day14.solve(self.data, lim=1000000000)
        self.assertEqual(result, 64)


if __name__ == '__main__':
    unittest.main()
