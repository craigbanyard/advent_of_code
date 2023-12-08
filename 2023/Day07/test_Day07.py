import Day07
import unittest


class Tests(unittest.TestCase):
    data = Day07.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            ('32T3K', 765),
            ('T55J5', 684),
            ('KK677', 28),
            ('KTJJT', 220),
            ('QQQJA', 483)
        ]
        self.assertEqual(self.data, expected)

    def test_solve_no_wildcard(self):
        result = Day07.solve(self.data)
        self.assertEqual(result, 6440)

    def test_solve_wildcard(self):
        result = Day07.solve(self.data, order='J23456789TQKA', wildcard='J')
        self.assertEqual(result, 5905)


if __name__ == '__main__':
    unittest.main()
