import Day06
import unittest


class Tests(unittest.TestCase):
    def test_get_input(self):
        data = Day06.get_input('sample.txt')
        self.assertEqual(data, 'mjqjpqmgbljsphdztnvjfqwrcgsmlb')

    def test_solve_p1_ex1(self):
        data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
        result = Day06.solve(data, chunk_size=4)
        self.assertEqual(result, 7)

    def test_solve_p1_ex2(self):
        data = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
        result = Day06.solve(data, chunk_size=4)
        self.assertEqual(result, 5)

    def test_solve_p1_ex3(self):
        data = 'nppdvjthqldpwncqszvftbrmjlhg'
        result = Day06.solve(data, chunk_size=4)
        self.assertEqual(result, 6)

    def test_solve_p1_ex4(self):
        data = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
        result = Day06.solve(data, chunk_size=4)
        self.assertEqual(result, 10)

    def test_solve_p1_ex5(self):
        data = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
        result = Day06.solve(data, chunk_size=4)
        self.assertEqual(result, 11)

    def test_solve_p2_ex1(self):
        data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
        result = Day06.solve(data, chunk_size=14)
        self.assertEqual(result, 19)

    def test_solve_p2_ex2(self):
        data = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
        result = Day06.solve(data, chunk_size=14)
        self.assertEqual(result, 23)

    def test_solve_p2_ex3(self):
        data = 'nppdvjthqldpwncqszvftbrmjlhg'
        result = Day06.solve(data, chunk_size=14)
        self.assertEqual(result, 23)

    def test_solve_p2_ex4(self):
        data = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
        result = Day06.solve(data, chunk_size=14)
        self.assertEqual(result, 29)

    def test_solve_p2_ex5(self):
        data = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
        result = Day06.solve(data, chunk_size=14)
        self.assertEqual(result, 26)


if __name__ == '__main__':
    unittest.main()
