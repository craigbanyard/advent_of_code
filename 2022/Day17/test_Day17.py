import Day17
import unittest


class Tests(unittest.TestCase):
    data = Day17.get_input('sample.txt')

    def test_get_input(self):
        self.assertEqual(self.data, '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>')

    def test_solve_p1(self):
        result = Day17.solve(self.data, max_steps=2022)
        self.assertEqual(result, 3068)

    def test_solve_p2(self):
        result = Day17.solve(self.data, max_steps=1000000000000)
        self.assertEqual(result, 1514285714288)


if __name__ == '__main__':
    unittest.main()
