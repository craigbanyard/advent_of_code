import Day20
import unittest


class Tests(unittest.TestCase):
    data = Day20.get_input('sample.txt')

    def test_get_input(self):
        self.assertListEqual(self.data, [1, 2, -3, 3, -2, 0, 4])

    def test_solve_p1(self):
        result = Day20.solve(self.data)
        self.assertEqual(result, 3)

    def test_solve_p2(self):
        result = Day20.solve(self.data, key=811589153, t=10)
        self.assertEqual(result, 1623178306)


if __name__ == '__main__':
    unittest.main()
