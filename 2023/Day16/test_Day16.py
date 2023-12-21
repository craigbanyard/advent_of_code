import Day16
import unittest


class Tests(unittest.TestCase):
    data = Day16.get_input('sample.txt')

    def test_get_input(self):
        expected = [
            '.|...\\....',
            '|.-.\\.....',
            '.....|-...',
            '........|.',
            '..........',
            '.........\\',
            '..../.\\\\..',
            '.-.-/..|..',
            '.|....-|.\\',
            '..//.|....'
        ]
        self.assertEqual(self.data, expected)

    def test_solve(self):
        result = Day16.solve(self.data)
        self.assertEqual(result, (46, 51))


if __name__ == '__main__':
    unittest.main()
