import Day15
import unittest


class Tests(unittest.TestCase):
    data = Day15.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            ((2+18j), (2+15j)),
            ((9+16j), (10+16j)),
            ((13+2j), (15+3j)),
            ((12+14j), (10+16j)),
            ((10+20j), (10+16j)),
            ((14+17j), (10+16j)),
            ((8+7j), (2+10j)),
            ((2+0j), (2+10j)),
            (11j, (2+10j)),
            ((20+14j), (25+17j)),
            ((17+20j), (21+22j)),
            ((16+7j), (15+3j)),
            ((14+3j), (15+3j)),
            ((20+1j), (15+3j))
        ]
        self.assertEqual(self.data, expected)

    def test_manhattan_both_complex(self):
        result = Day15.manhattan(1+1j, 7-4j)
        self.assertEqual(result, 11)

    def test_manhattan_both_real(self):
        result = Day15.manhattan(1, 14)
        self.assertEqual(result, 13)

    def test_manhattan_complex_real(self):
        result = Day15.manhattan(1+1j, 14)
        self.assertEqual(result, 14)

    def test_solve_p1(self):
        result, _ = Day15.solve(self.data)
        self.assertEqual(result, 26)

    def test_solve_p2(self):
        _, result = Day15.solve(self.data)
        self.assertEqual(result, 56000011)


if __name__ == '__main__':
    unittest.main()
