import Day17
import unittest


class Tests(unittest.TestCase):
    data1 = Day17.get_input('sample.txt')
    data2 = Day17.get_input('sample2.txt')

    def test_get_input1(self):
        expected = [
            [2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
            [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
            [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
            [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
            [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
            [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
            [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
            [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
            [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
            [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
            [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
            [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
            [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3]
        ]
        self.assertEqual(self.data1, expected)

    def test_get_input2(self):
        expected = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1]
        ]
        self.assertEqual(self.data2, expected)

    def test_solve_part1_sample1(self):
        result = Day17.solve(self.data1)
        self.assertEqual(result, 102)

    def test_solve_part2_sample1(self):
        result = Day17.solve(self.data1, minspeed=4, maxspeed=10)
        self.assertEqual(result, 94)

    def test_solve_part2_sample2(self):
        result = Day17.solve(self.data2, minspeed=4, maxspeed=10)
        self.assertEqual(result, 71)


if __name__ == '__main__':
    unittest.main()
