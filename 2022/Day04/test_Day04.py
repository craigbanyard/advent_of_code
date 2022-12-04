import Day04
import unittest


class Tests(unittest.TestCase):
    data = list(Day04.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            [2, 4, 6, 8],
            [2, 3, 4, 5],
            [5, 7, 7, 9],
            [2, 8, 3, 7],
            [6, 6, 4, 6],
            [2, 6, 4, 8]
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day04.solve(self.data)
        self.assertEqual(result, (2, 4))


if __name__ == '__main__':
    unittest.main()
