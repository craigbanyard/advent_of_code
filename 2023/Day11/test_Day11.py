import Day11
import unittest


class Tests(unittest.TestCase):
    data = Day11.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            (0, 3),
            (1, 7),
            (2, 0),
            (4, 6),
            (5, 1),
            (6, 9),
            (8, 7),
            (9, 0),
            (9, 4)
        ]
        self.assertEqual(self.data, expected)

    def test_solve_f2(self):
        result = Day11.solve(self.data)
        self.assertEqual(result, 374)

    def test_solve_f10(self):
        result = Day11.solve(self.data, expansion_factor=10)
        self.assertEqual(result, 1030)

    def test_solve_f100(self):
        result = Day11.solve(self.data, expansion_factor=100)
        self.assertEqual(result, 8410)


if __name__ == '__main__':
    unittest.main()
