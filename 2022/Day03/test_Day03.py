import Day03
import unittest


class Tests(unittest.TestCase):
    data = list(Day03.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            'vJrwpWtwJgWrhcsFMMfFFhFp',
            'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
            'PmmdzqPrVvPwwTWBwg',
            'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
            'ttgJtRGJQctTZtZT',
            'CrZsJsPPZsGzwwsLwLmpwMDw'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day03.solve(self.data)
        self.assertEqual(result, (157, 70))


if __name__ == '__main__':
    unittest.main()
