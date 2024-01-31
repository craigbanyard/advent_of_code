import DayXX
import unittest


class Tests(unittest.TestCase):
    data = DayXX.get_input('sample.txt')

    def test_get_input(self):
        expected = []
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = DayXX.solve(self.data)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
