import Day08
import unittest


class Tests(unittest.TestCase):
    data = Day08.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0]
        ]
        self.assertListEqual(self.data, expected)

    def test_solve_p1(self):
        result, _ = Day08.solve(self.data)
        self.assertEqual(result, 21)

    def test_solve_p2(self):
        _, result = Day08.solve(self.data)
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()
