import Day19
import unittest


class Tests(unittest.TestCase):
    data = Day19.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            (1, 4, 2, 3, 14, 2, 7),
            (2, 2, 3, 3, 8, 3, 12)
        ]
        self.assertListEqual(self.data, expected)

    def test_solve_p1(self):
        result = Day19.solve(self.data)
        self.assertEqual(result, 33)

    def test_solve_p2(self):
        result = Day19.solve(self.data[:3], time_limit=32, part2=True)
        self.assertEqual(result, 3472)


if __name__ == '__main__':
    unittest.main()
