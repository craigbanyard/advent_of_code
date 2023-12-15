import Day12
import unittest


class Tests(unittest.TestCase):
    data = Day12.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            ('???.###', (1, 1, 3)),
            ('.??..??...?##.', (1, 1, 3)),
            ('?#?#?#?#?#?#?#?', (1, 3, 1, 6)),
            ('????.#...#...', (4, 1, 1)),
            ('????.######..#####.', (1, 6, 5)),
            ('?###????????', (3, 2, 1))
        ]
        self.assertEqual(self.data, expected)

    def test_solve_part1(self):
        result = Day12.solve(self.data)
        self.assertEqual(result, 21)

    def test_solve_part2(self):
        result = Day12.solve(self.data, n=5)
        self.assertEqual(result, 525152)


if __name__ == '__main__':
    unittest.main()
