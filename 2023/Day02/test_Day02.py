import Day02
import unittest


class Tests(unittest.TestCase):
    data = list(Day02.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
            'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
            'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
            'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
            'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day02.solve(self.data)
        self.assertEqual(result, (8, 2286))


if __name__ == '__main__':
    unittest.main()
