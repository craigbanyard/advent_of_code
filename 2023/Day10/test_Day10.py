import Day10
import unittest


class Tests(unittest.TestCase):
    data1 = Day10.get_input('sample.txt')
    data2 = Day10.get_input('sample2.txt')
    data3 = Day10.get_input('sample3.txt')
    data4 = Day10.get_input('sample4.txt')
    data5 = Day10.get_input('sample5.txt')
    data6 = Day10.get_input('sample6.txt')

    def _split(self, data: list[str]) -> list[list[str]]:
        return [[*line] for line in data]

    def test_get_input_sample1(self):
        expected = [
            '═╚║╔╗',
            '╗S═╗║',
            '╚║╗║║',
            '═╚═╝║',
            '╚║═╝╔'
        ]
        self.assertEqual(self.data1, self._split(expected))

    def test_get_input_sample2(self):
        expected = [
            '╗═╔╗═',
            '.╔╝║╗',
            'S╝╚╚╗',
            '║╔══╝',
            '╚╝.╚╝'
        ]
        self.assertEqual(self.data2, self._split(expected))

    def test_get_input_sample3(self):
        expected = [
            '...........',
            '.S═══════╗.',
            '.║╔═════╗║.',
            '.║║.....║║.',
            '.║║.....║║.',
            '.║╚═╗.╔═╝║.',
            '.║..║.║..║.',
            '.╚══╝.╚══╝.',
            '...........'
        ]
        self.assertEqual(self.data3, self._split(expected))

    def test_get_input_sample4(self):
        expected = [
            '..........',
            '.S══════╗.',
            '.║╔════╗║.',
            '.║║....║║.',
            '.║║....║║.',
            '.║╚═╗╔═╝║.',
            '.║..║║..║.',
            '.╚══╝╚══╝.',
            '..........'
        ]
        self.assertEqual(self.data4, self._split(expected))

    def test_get_input_sample5(self):
        expected = [
            '.╔════╗╔╗╔╗╔╗╔═╗....',
            '.║╔══╗║║║║║║║║╔╝....',
            '.║║.╔╝║║║║║║║║╚╗....',
            '╔╝╚╗╚╗╚╝╚╝║║╚╝.╚═╗..',
            '╚══╝.╚╗...╚╝S╗╔═╗╚╗.',
            '....╔═╝..╔╗╔╝║╚╗╚╗╚╗',
            '....╚╗.╔╗║║╚╗║.╚╗╚╗║',
            '.....║╔╝╚╝║╔╝║╔╗║.╚╝',
            '....╔╝╚═╗.║║.║║║║...',
            '....╚═══╝.╚╝.╚╝╚╝...'
        ]
        self.assertEqual(self.data5, self._split(expected))

    def test_get_input_sample6(self):
        expected = [
            '╔╔╗╔S╔╗╔╗╔╗╔╗╔╗╔═══╗',
            '╚║╚╝║║║║║║║║║║║║╔══╝',
            '╔╚═╗╚╝╚╝║║║║║║╚╝╚═╗╗',
            '╔══╝╔══╗║║╚╝╚╝╗╔╗╔╝═',
            '╚═══╝╔═╝╚╝.║║═╔╝╚╝╝╗',
            '║╔║╔═╝╔═══╗╔╗═╚╗╚║╗║',
            '║╔╔╝╔╗╚╗╔═╝╔╗║╝╚═══╗',
            '╗═╚═╝╚╗║║╔╗║╚╗╔═╗╔╗║',
            '╚.╚╗╚╔╝║║║║║╔╝╚╗║║╚╝',
            '╚╗╝╚╝╚═╝╚╝╚╝╚══╝╚╝.╚'
        ]
        self.assertEqual(self.data6, self._split(expected))

    def test_solve_sample1(self):
        result, _ = Day10.solve(self.data1)
        self.assertEqual(result, 4)

    def test_solve_sample2(self):
        result, _ = Day10.solve(self.data2)
        self.assertEqual(result, 8)

    def test_solve_sample3(self):
        _, result = Day10.solve(self.data3)
        self.assertEqual(result, 4)

    def test_solve_sample4(self):
        _, result = Day10.solve(self.data4)
        self.assertEqual(result, 4)

    def test_solve_sample5(self):
        _, result = Day10.solve(self.data5)
        self.assertEqual(result, 8)

    def test_solve_sample6(self):
        _, result = Day10.solve(self.data6)
        self.assertEqual(result, 10)


if __name__ == '__main__':
    unittest.main()
