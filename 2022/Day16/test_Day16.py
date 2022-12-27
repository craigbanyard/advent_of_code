import Day16
import unittest


class Tests(unittest.TestCase):
    data = Day16.get_input('sample.txt')

    def test_get_input_tunnels(self):
        result, _ = self.data
        expected = {
            'AA': ['DD', 'II', 'BB'],
            'BB': ['CC', 'AA'],
            'CC': ['DD', 'BB'],
            'DD': ['CC', 'AA', 'EE'],
            'EE': ['FF', 'DD'],
            'FF': ['EE', 'GG'],
            'GG': ['FF', 'HH'],
            'HH': ['GG'],
            'II': ['AA', 'JJ'],
            'JJ': ['II']
        }
        self.assertDictEqual(result, expected)

    def test_get_input_valves(self):
        _, result = self.data
        expected = {
            'AA': 0,
            'BB': 13,
            'CC': 2,
            'DD': 20,
            'EE': 3,
            'FF': 0,
            'GG': 0,
            'HH': 22,
            'II': 0,
            'JJ': 21
        }
        self.assertDictEqual(result, expected)

    def test_get_costs_AA(self):
        expected = {'DD': 1, 'BB': 1, 'CC': 2, 'EE': 2, 'JJ': 2, 'HH': 5}
        result = Day16.get_costs(self.data)
        self.assertDictEqual(result, expected)

    def test_get_costs_BB(self):
        expected = {'CC': 1, 'DD': 2, 'EE': 3, 'JJ': 3, 'HH': 6}
        result = Day16.get_costs(self.data, start='BB')
        self.assertDictEqual(result, expected)

    def test_prune(self):
        expected = {
            'AA': {'DD': 1, 'BB': 1, 'CC': 2, 'EE': 2, 'JJ': 2, 'HH': 5},
            'BB': {'CC': 1, 'DD': 2, 'EE': 3, 'JJ': 3, 'HH': 6},
            'CC': {'DD': 1, 'BB': 1, 'EE': 2, 'JJ': 4, 'HH': 5},
            'DD': {'CC': 1, 'EE': 1, 'BB': 2, 'JJ': 3, 'HH': 4},
            'EE': {'DD': 1, 'CC': 2, 'HH': 3, 'BB': 3, 'JJ': 4},
            'HH': {'EE': 3, 'DD': 4, 'CC': 5, 'BB': 6, 'JJ': 7},
            'JJ': {'DD': 3, 'BB': 3, 'CC': 4, 'EE': 4, 'HH': 7}
        }
        result = Day16.prune(self.data)
        self.assertDictEqual(result, expected)

    def test_solve_p1(self):
        result, _ = Day16.solve(self.data)
        self.assertEqual(result, 1651)

    def test_solve_p2(self):
        _, result = Day16.solve(self.data)
        self.assertEqual(result, 1707)


if __name__ == '__main__':
    unittest.main()
