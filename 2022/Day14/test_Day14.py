import Day14
import unittest


class Tests(unittest.TestCase):
    data = list(Day14.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            [(498, 4), (498, 6), (496, 6)],
            [(503, 4), (502, 4), (502, 9), (494, 9)]
        ]
        self.assertEqual(self.data, expected)

    def test_process_pair_x(self):
        expected = {1, 2, 3, 4}
        result = Day14.process_pair((1, 0), (4, 0))
        self.assertSetEqual(result, expected)

    def test_process_pair_y(self):
        expected = {1j, 2j, 3j, 4j}
        result = Day14.process_pair((0, 1), (0, 4))
        self.assertSetEqual(result, expected)

    def test_fall(self):
        expected = 500 + 2j
        result = Day14.fall({499 + 3j, 500 + 3j, 501 + 3j}, {})
        self.assertEqual(result, expected)

    def test_draw(self):
        expected = '..+..\n.....\n.....\n.###.\n.....\n'
        result = Day14.draw({499 + 3j, 500 + 3j, 501 + 3j}, {})
        self.assertEqual(result, expected)

    def test_draw_sand(self):
        expected = '..+..\n.....\n..o..\n.###.\n.....\n'
        result = Day14.draw({499 + 3j, 500 + 3j, 501 + 3j}, {500 + 2j})
        self.assertEqual(result, expected)

    def test_solve_p1(self):
        result, _ = Day14.solve(self.data)
        self.assertEqual(result, 24)

    def test_solve_p2(self):
        _, result = Day14.solve(self.data)
        self.assertEqual(result, 93)


if __name__ == '__main__':
    unittest.main()
