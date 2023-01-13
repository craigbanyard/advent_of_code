import Day23
import unittest
import numpy as np


class Tests(unittest.TestCase):
    data = Day23.get_input('sample.txt')
    G = Day23.get_input_np('sample.txt')

    def test_get_input(self):
        expected = {
            (1+3j),
            (1+5j),
            (1+6j),
            (2+1j),
            (2+4j),
            (3+1j),
            (3+4j),
            (3+5j),
            (4+0j),
            (4+1j),
            (4+2j),
            (4+4j),
            (4+6j),
            (5+3j),
            (5+5j),
            (6+1j),
            (6+2j),
            (6+3j),
            (6+5j),
            2j,
            4j,
            5j
        }
        self.assertEqual(self.data, expected)

    def test_get_input_np(self):
        expected = np.array(
            [[0, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 1, 1, 0, 1],
             [1, 0, 0, 0, 1, 0, 1],
             [0, 1, 0, 0, 0, 1, 1],
             [1, 0, 1, 1, 1, 0, 0],
             [1, 1, 0, 1, 0, 1, 1],
             [0, 1, 0, 0, 1, 0, 0]]
        ).astype(bool)
        np.testing.assert_array_equal(self.G, expected)

    def test_solve_p1(self):
        result = Day23.solve(self.data, rounds=10)
        self.assertEqual(result, 110)

    def test_solve_p2(self):
        result = Day23.solve(self.data, part1=False)
        self.assertEqual(result, 20)

    def test_solve_np_p1(self):
        result = Day23.solve_np(self.G, rounds=10)
        self.assertEqual(result, 110)

    def test_solve_np_p2(self):
        result = Day23.solve_np(self.G, part1=False)
        self.assertEqual(result, 20)


if __name__ == '__main__':
    unittest.main()
