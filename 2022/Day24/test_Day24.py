import Day24
import unittest


class Tests(unittest.TestCase):
    data = Day24.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            '#.######',
            '#>>.<^<#',
            '#.<..<<#',
            '#>v.><>#',
            '#<^v^^>#',
            '######.#'
        ]
        self.assertEqual(self.data, expected)

    def test_solve_p1(self):
        result = Day24.solve(self.data)
        self.assertEqual(result, 18)

    def test_solve_p2(self):
        result = Day24.solve(self.data, trips=3)
        self.assertEqual(result, 54)


if __name__ == '__main__':
    unittest.main()
