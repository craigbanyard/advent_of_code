import Day06
import unittest


class Tests(unittest.TestCase):
    def __init__(self, f, input, output):
        super(Tests, self).__init__()
        self.f = f
        self.input = input
        self.output = output

    def runTest(self):
        self.assertEqual(self.f(*self.input), self.output)


def suite():
    test_cases = [
        (Day06.get_input, ('sample.txt', ), 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'),
        (Day06.solve, ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4), 7),
        (Day06.solve, ('bvwbjplbgvbhsrlpgdmjqwftvncz', 4), 5),
        (Day06.solve, ('nppdvjthqldpwncqszvftbrmjlhg', 4), 6),
        (Day06.solve, ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4), 10),
        (Day06.solve, ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4), 11),
        (Day06.solve, ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14), 19),
        (Day06.solve, ('bvwbjplbgvbhsrlpgdmjqwftvncz', 14), 23),
        (Day06.solve, ('nppdvjthqldpwncqszvftbrmjlhg', 14), 23),
        (Day06.solve, ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14), 29),
        (Day06.solve, ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14), 26),
    ]
    suite = unittest.TestSuite()
    suite.addTests(Tests(f, input, output)
                   for f, input, output in test_cases)
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
