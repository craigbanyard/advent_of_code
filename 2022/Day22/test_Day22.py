import Day22
import unittest


class Tests(unittest.TestCase):
    data = Day22.get_input('sample.txt')

    def test_get_input_board(self):
        result, _ = self.data
        expected = {
            (9+1j): True,
            (10+1j): True,
            (11+1j): True,
            (12+1j): False,
            (9+2j): True,
            (10+2j): False,
            (11+2j): True,
            (12+2j): True,
            (9+3j): False,
            (10+3j): True,
            (11+3j): True,
            (12+3j): True,
            (9+4j): True,
            (10+4j): True,
            (11+4j): True,
            (12+4j): True,
            (1+5j): True,
            (2+5j): True,
            (3+5j): True,
            (4+5j): False,
            (5+5j): True,
            (6+5j): True,
            (7+5j): True,
            (8+5j): True,
            (9+5j): True,
            (10+5j): True,
            (11+5j): True,
            (12+5j): False,
            (1+6j): True,
            (2+6j): True,
            (3+6j): True,
            (4+6j): True,
            (5+6j): True,
            (6+6j): True,
            (7+6j): True,
            (8+6j): True,
            (9+6j): False,
            (10+6j): True,
            (11+6j): True,
            (12+6j): True,
            (1+7j): True,
            (2+7j): True,
            (3+7j): False,
            (4+7j): True,
            (5+7j): True,
            (6+7j): True,
            (7+7j): True,
            (8+7j): False,
            (9+7j): True,
            (10+7j): True,
            (11+7j): True,
            (12+7j): True,
            (1+8j): True,
            (2+8j): True,
            (3+8j): True,
            (4+8j): True,
            (5+8j): True,
            (6+8j): True,
            (7+8j): True,
            (8+8j): True,
            (9+8j): True,
            (10+8j): True,
            (11+8j): False,
            (12+8j): True,
            (9+9j): True,
            (10+9j): True,
            (11+9j): True,
            (12+9j): False,
            (13+9j): True,
            (14+9j): True,
            (15+9j): True,
            (16+9j): True,
            (9+10j): True,
            (10+10j): True,
            (11+10j): True,
            (12+10j): True,
            (13+10j): True,
            (14+10j): False,
            (15+10j): True,
            (16+10j): True,
            (9+11j): True,
            (10+11j): False,
            (11+11j): True,
            (12+11j): True,
            (13+11j): True,
            (14+11j): True,
            (15+11j): True,
            (16+11j): True,
            (9+12j): True,
            (10+12j): True,
            (11+12j): True,
            (12+12j): True,
            (13+12j): True,
            (14+12j): True,
            (15+12j): False,
            (16+12j): True
        }
        self.assertDictEqual(result, expected)

    def test_get_input_instr(self):
        _, result = self.data
        expected = [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]
        self.assertListEqual(result, expected)

    def test_solve_p1(self):
        result = Day22.solve(self.data)
        self.assertEqual(result, 6032)

    def test_solve_p2(self):
        result = Day22.solve(self.data, dims=3, net_func=Day22.cube_net_0)
        self.assertEqual(result, 5031)


if __name__ == '__main__':
    unittest.main()
