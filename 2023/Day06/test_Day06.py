import Day06
import unittest


class Tests(unittest.TestCase):
    data_spaces = list(Day06.get_input('sample.txt', spaces=True))
    data_no_spaces = list(Day06.get_input('sample.txt', spaces=False))

    def test_get_input_spaces(self):
        expected = [
            (7, 9),
            (15, 40),
            (30, 200)
        ]
        self.assertEqual(self.data_spaces, expected)

    def test_get_input_no_spaces(self):
        expected = [
            (71530, 940200)
        ]
        self.assertEqual(self.data_no_spaces, expected)

    def test_solve_part1(self):
        result = Day06.solve(self.data_spaces)
        self.assertEqual(result, 288)

    def test_solve_part2(self):
        result = Day06.solve(self.data_no_spaces)
        self.assertEqual(result, 71503)


if __name__ == '__main__':
    unittest.main()
