import Day12
import unittest


class Tests(unittest.TestCase):
    data = Day12.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            ['S', 'a', 'b', 'q', 'p', 'o', 'n', 'm'],
            ['a', 'b', 'c', 'r', 'y', 'x', 'x', 'l'],
            ['a', 'c', 'c', 's', 'z', 'E', 'x', 'k'],
            ['a', 'c', 'c', 't', 'u', 'v', 'w', 'j'],
            ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i']
        ]
        self.assertEqual(self.data, expected)

    def test_solve_p1(self):
        result, _ = Day12.solve(self.data)
        self.assertEqual(result, 31)

    def test_solve_p2(self):
        _, result = Day12.solve(self.data)
        self.assertEqual(result, 29)


if __name__ == '__main__':
    unittest.main()
