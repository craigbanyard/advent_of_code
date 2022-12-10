import Day09
import unittest


class Tests(unittest.TestCase):
    sample1 = list(Day09.get_input('sample.txt'))
    sample2 = list(Day09.get_input('sample2.txt'))

    def test_get_input_ex1(self):
        expected = [
            ('R', 4),
            ('U', 4),
            ('L', 3),
            ('D', 1),
            ('R', 4),
            ('D', 1),
            ('L', 5),
            ('R', 2)
        ]
        self.assertListEqual(self.sample1, expected)

    def test_get_input_ex2(self):
        expected = [
            ('R', 5),
            ('U', 8),
            ('L', 8),
            ('D', 3),
            ('R', 17),
            ('D', 10),
            ('L', 25),
            ('U', 20)
        ]
        self.assertListEqual(self.sample2, expected)

    def test_solve_p1_ex1(self):
        result, = Day09.solve(self.sample1, knots=[2])
        self.assertEqual(result, 13)

    def test_solve_p2_ex1(self):
        result, = Day09.solve(self.sample1, knots=[10])
        self.assertEqual(result, 1)

    def test_solve_p1_ex2(self):
        result, = Day09.solve(self.sample2, knots=[2])
        self.assertEqual(result, 88)

    def test_solve_p2_ex2(self):
        result, = Day09.solve(self.sample2, knots=[10])
        self.assertEqual(result, 36)


if __name__ == '__main__':
    unittest.main()
