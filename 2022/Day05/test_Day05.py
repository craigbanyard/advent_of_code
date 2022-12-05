import Day05
from collections import deque
import unittest


class Tests(unittest.TestCase):
    def test_get_input_stack(self):
        result, _ = Day05.get_input('sample.txt')
        expected = {
            1: deque(['N', 'Z']),
            2: deque(['D', 'C', 'M']),
            3: deque(['P']),
        }
        self.assertDictEqual(result, expected)

    def test_get_input_moves(self):
        _, result = Day05.get_input('sample.txt')
        expected = [
            [1, 2, 1],
            [3, 1, 3],
            [2, 2, 1],
            [1, 1, 2]
        ]
        self.assertListEqual(result, expected)

    def test_solve_p1(self):
        stack, moves = Day05.get_input('sample.txt')
        result = Day05.solve(stack, moves, part1=True)
        self.assertEqual(result, 'CMZ')

    def test_solve_p2(self):
        stack, moves = Day05.get_input('sample.txt')
        result = Day05.solve(stack, moves, part1=False)
        self.assertEqual(result, 'MCD')


if __name__ == '__main__':
    unittest.main()
