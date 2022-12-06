import Day06
import unittest


class Tests(unittest.TestCase):
    data = Day06.get_input('sample.txt')

    def test_get_input(self):
        self.assertEqual(self.data, 'mjqjpqmgbljsphdztnvjfqwrcgsmlb')

    def test_solve_p1(self):
        result = Day06.solve(self.data, chunk_size=4)
        self.assertEqual(result, 7)

    def test_solve_p2(self):
        result = Day06.solve(self.data, chunk_size=14)
        self.assertEqual(result, 19)


if __name__ == '__main__':
    unittest.main()
