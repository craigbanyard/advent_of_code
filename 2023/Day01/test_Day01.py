import Day01
import unittest


class Tests(unittest.TestCase):
    data_p1 = Day01.get_input('sample.txt')
    data_p2 = Day01.get_input('sample2.txt')

    def test_get_input_p1(self):
        expected = [
            '1abc2',
            'pqr3stu8vwx',
            'a1b2c3d4e5f',
            'treb7uchet'
        ]
        self.assertEqual(self.data_p1, expected)

    def test_get_input_p2(self):
        expected = [
            'two1nine',
            'eightwothree',
            'abcone2threexyz',
            'xtwone3four',
            '4nineeightseven2',
            'zoneight234',
            '7pqrstsixteen'
        ]
        self.assertEqual(self.data_p2, expected)

    def test_solve_p1(self):
        result = Day01.solve(self.data_p1, sub_words=False)
        self.assertEqual(result, 142)

    def test_solve_p2(self):
        result = Day01.solve(self.data_p2, sub_words=True)
        self.assertEqual(result, 281)


if __name__ == '__main__':
    unittest.main()
