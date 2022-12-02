import Day02
import unittest


class Tests(unittest.TestCase):
    data = Day02.get_input('sample.txt')

    def test_get_input(self):
        self.assertEqual(self.data, ['A Y', 'B X', 'C Z'])

    def test_solve_p1(self):
        result = Day02.solve(self.data, part=1)
        self.assertEqual(result, 15)

    def test_solve_p2(self):
        result = Day02.solve(self.data, part=2)
        self.assertEqual(result, 12)


if __name__ == '__main__':
    unittest.main()
