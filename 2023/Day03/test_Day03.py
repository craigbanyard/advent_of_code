import Day03
import unittest


class Tests(unittest.TestCase):
    data = Day03.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            '467..114..',
            '...*......',
            '..35..633.',
            '......#...',
            '617*......',
            '.....+.58.',
            '..592.....',
            '......755.',
            '...$.*....',
            '.664.598..'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day03.solve(self.data)
        self.assertEqual(result, (4361, 467835))


if __name__ == '__main__':
    unittest.main()
