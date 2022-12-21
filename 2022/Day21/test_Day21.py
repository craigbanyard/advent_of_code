import Day21
import unittest


class Tests(unittest.TestCase):
    data = Day21.get_input('sample.txt')

    def test_get_input(self):
        expected = {
            'root': ['pppw', '+', 'sjmn'],
            'dbpl': ['5'],
            'cczh': ['sllz', '+', 'lgvd'],
            'zczc': ['2'],
            'ptdq': ['humn', '-', 'dvpt'],
            'dvpt': ['3'],
            'lfqf': ['4'],
            'humn': ['5'],
            'ljgn': ['2'],
            'sjmn': ['drzm', '*', 'dbpl'],
            'sllz': ['4'],
            'pppw': ['cczh', '/', 'lfqf'],
            'lgvd': ['ljgn', '*', 'ptdq'],
            'drzm': ['hmdt', '-', 'zczc'],
            'hmdt': ['32']
        }
        self.assertDictEqual(self.data, expected)

    def test_solve_p1(self):
        result = Day21.solve(self.data)
        self.assertEqual(result, 152)

    def test_solve_p2(self):
        result = Day21.solve(self.data, part1=False)
        self.assertEqual(result, 301)


if __name__ == '__main__':
    unittest.main()
