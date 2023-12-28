import Day18
import unittest


class Tests(unittest.TestCase):
    data = list(Day18.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            ('R', 6, 'R', 461937),
            ('D', 5, 'D', 56407),
            ('L', 2, 'R', 356671),
            ('D', 2, 'D', 863240),
            ('R', 2, 'R', 367720),
            ('D', 2, 'D', 266681),
            ('L', 5, 'L', 577262),
            ('U', 2, 'U', 829975),
            ('L', 1, 'L', 112010),
            ('U', 2, 'D', 829975),
            ('R', 2, 'L', 491645),
            ('U', 3, 'U', 686074),
            ('L', 2, 'L', 5411),
            ('U', 2, 'U', 500254)
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day18.solve(self.data)
        self.assertEqual(result, (62, 952408144115))


if __name__ == '__main__':
    unittest.main()
