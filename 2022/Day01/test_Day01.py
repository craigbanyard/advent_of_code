import Day01
import unittest


class Tests(unittest.TestCase):
    data = Day01.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            [1000, 2000, 3000],
            [4000],
            [5000, 6000],
            [7000, 8000, 9000],
            [10000]
        ]
        self.assertEqual(self.data, expected)

    def test_solve_p1(self):
        result = Day01.solve(self.data, n=1)
        self.assertEqual(result, 24000)

    def test_solve_p2(self):
        result = Day01.solve(self.data, n=3)
        self.assertEqual(result, 45000)


if __name__ == '__main__':
    unittest.main()
