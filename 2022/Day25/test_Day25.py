import Day25
import unittest


class Tests(unittest.TestCase):
    data = Day25.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            '1=-0-2',
            '12111',
            '2=0=',
            '21',
            '2=01',
            '111',
            '20012',
            '112',
            '1=-1=',
            '1-12',
            '12',
            '1=',
            '122'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day25.solve(self.data)
        self.assertEqual(result, Day25.SNAFU('2=-1=0'))


if __name__ == '__main__':
    unittest.main()
