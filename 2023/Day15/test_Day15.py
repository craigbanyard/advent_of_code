import Day15
import unittest


class Tests(unittest.TestCase):
    data = list(Day15.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            'rn=1',
            'cm-',
            'qp=3',
            'cm=2',
            'qp-',
            'pc=4',
            'ot=9',
            'ab=5',
            'pc-',
            'pc=6',
            'ot=7'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day15.solve(self.data)
        self.assertEqual(result, (1320, 145))


if __name__ == '__main__':
    unittest.main()
