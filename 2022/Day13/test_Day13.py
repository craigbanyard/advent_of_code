import Day13
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
    data = [
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [[1], 4],
        [9],
        [[8, 7, 6]],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [7, 7, 7, 7],
        [7, 7, 7],
        [],
        [3],
        [[[]]],
        [[]],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    ]
    test_cases = [
        (Day13.string_safe, (str(data),), True),
        (Day13.string_safe, ('[1,2,potentially malicious text,3]',), False),
        (Day13.get_input, ('sample.txt',), data),
        (Day13.lt, (data[0], data[1]), True),
        (Day13.lt, (data[2], data[3]), True),
        (Day13.lt, (data[4], data[5]), False),
        (Day13.lt, (data[6], data[7]), True),
        (Day13.lt, (data[8], data[9]), False),
        (Day13.lt, (data[10], data[11]), True),
        (Day13.lt, (data[12], data[13]), False),
        (Day13.lt, (data[14], data[15]), False),
        (Day13.solve, (data,), (13, 140)),
    ]
    suite = unittest.TestSuite()
    suite.addTests(Tests(f, input, output)
                   for f, input, output in test_cases)
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
