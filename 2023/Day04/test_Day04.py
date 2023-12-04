import Day04
import unittest


class Tests(unittest.TestCase):
    data = list(Day04.get_input('sample.txt'))

    def test_get_input(self):
        expected = [
            ({'17', '41', '48', '83', '86'},
             {'17', '31', '48', '53', '6', '83', '86', '9'}),
            ({'13', '16', '20', '32', '61'},
             {'17', '19', '24', '30', '32', '61', '68', '82'}),
            ({'1', '21', '44', '53', '59'},
             {'1', '14', '16', '21', '63', '69', '72', '82'}),
            ({'41', '69', '73', '84', '92'},
             {'5', '51', '54', '58', '59', '76', '83', '84'}),
            ({'26', '28', '32', '83', '87'},
             {'12', '22', '30', '36', '70', '82', '88', '93'}),
            ({'13', '18', '31', '56', '72'},
             {'10', '11', '23', '35', '36', '67', '74', '77'})
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day04.solve(self.data)
        self.assertEqual(result, (13, 30))


if __name__ == '__main__':
    unittest.main()
