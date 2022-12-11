import Day11
import unittest


class Tests(unittest.TestCase):
    data = Day11.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            [
                'Monkey 0:',
                '  Starting items: 79, 98',
                '  Operation: new = old * 19',
                '  Test: divisible by 23',
                '    If true: throw to monkey 2',
                '    If false: throw to monkey 3'
            ],
            [
                'Monkey 1:',
                '  Starting items: 54, 65, 75, 74',
                '  Operation: new = old + 6',
                '  Test: divisible by 19',
                '    If true: throw to monkey 2',
                '    If false: throw to monkey 0'
            ],
            [
                'Monkey 2:',
                '  Starting items: 79, 60, 97',
                '  Operation: new = old * old',
                '  Test: divisible by 13',
                '    If true: throw to monkey 1',
                '    If false: throw to monkey 3'
            ],
            [
                'Monkey 3:',
                '  Starting items: 74',
                '  Operation: new = old + 3',
                '  Test: divisible by 17',
                '    If true: throw to monkey 0',
                '    If false: throw to monkey 1'
            ]
        ]
        expected = ['\n'.join(line for line in notes) for notes in expected]
        self.assertListEqual(self.data, expected)

    def test_solve_p1(self):
        result = Day11.solve(self.data, rounds=20, wrc=3)
        self.assertEqual(result, 10605)

    def test_solve_p2(self):
        result = Day11.solve(self.data, rounds=1000, wrc=1)
        self.assertEqual(result, 27019168)


if __name__ == '__main__':
    unittest.main()
