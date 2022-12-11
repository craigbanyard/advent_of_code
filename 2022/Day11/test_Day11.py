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
        expected = [Day11.Monkey(notes) for notes in expected]
        self.assertEqual(self.data, expected)

    def test_monkey_business_sample1(self):
        test_data = [101, 95, 7, 105]
        result = Day11.monkey_business(test_data)
        self.assertEqual(result, 10605)

    def test_monkey_business_sample2(self):
        test_data = [52166, 47830, 1938, 52013]
        result = Day11.monkey_business(test_data)
        self.assertEqual(result, 2713310158)

    def test_monkey_business_n3(self):
        test_data = [1, 2, 3, 4, 5]
        result = Day11.monkey_business(test_data, n=3)
        self.assertEqual(result, 60)

    def test_solve_p1(self):
        result = Day11.solve(self.data, rounds=20, wrc=3)
        self.assertEqual(result, 10605)

    def test_solve_p2(self):
        result = Day11.solve(self.data, rounds=10000, wrc=1)
        self.assertEqual(result, 2713310158)


if __name__ == '__main__':
    unittest.main()
