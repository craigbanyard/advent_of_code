import Day08
import unittest


class Tests(unittest.TestCase):
    data1 = Day08.get_input('sample.txt')
    data2 = Day08.get_input('sample2.txt')
    data3 = Day08.get_input('sample3.txt')

    def test_get_input_sample1(self):
        expected = (
            'RL',
            {
                'AAA': ('BBB', 'CCC'),
                'BBB': ('DDD', 'EEE'),
                'CCC': ('ZZZ', 'GGG'),
                'DDD': ('DDD', 'DDD'),
                'EEE': ('EEE', 'EEE'),
                'GGG': ('GGG', 'GGG'),
                'ZZZ': ('ZZZ', 'ZZZ')
            }
        )
        self.assertEqual(self.data1, expected)

    def test_get_input_sample2(self):
        expected = (
            'LLR',
            {
                'AAA': ('BBB', 'BBB'),
                'BBB': ('AAA', 'ZZZ'),
                'ZZZ': ('ZZZ', 'ZZZ')
            }
        )
        self.assertEqual(self.data2, expected)

    def test_get_input_sample3(self):
        expected = (
            'LR',
            {
                '11A': ('11B', 'XXX'),
                '11B': ('XXX', '11Z'),
                '11Z': ('11B', 'XXX'),
                '22A': ('22B', 'XXX'),
                '22B': ('22C', '22C'),
                '22C': ('22Z', '22Z'),
                '22Z': ('22B', '22B'),
                'XXX': ('XXX', 'XXX'),
            },
        )
        self.assertEqual(self.data3, expected)

    def test_solve_sample1(self):
        result = Day08.solve(self.data1)
        self.assertEqual(result, 2)

    def test_solve_sample2(self):
        result = Day08.solve(self.data2)
        self.assertEqual(result, 6)

    def test_solve_sample3(self):
        result = Day08.solve(self.data3, start_suffix='A', end_suffix='Z')
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()
