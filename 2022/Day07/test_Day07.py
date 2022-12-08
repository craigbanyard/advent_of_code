import Day07
import unittest


class Tests(unittest.TestCase):
    data = list(Day07.get_input('sample.txt'))
    dirs, tree = Day07.construct_tree(data)

    def test_get_input(self):
        expected = [
            '$ cd /',
            '$ ls',
            'dir a',
            '14848514 b.txt',
            '8504156 c.dat',
            'dir d',
            '$ cd a',
            '$ ls',
            'dir e',
            '29116 f',
            '2557 g',
            '62596 h.lst',
            '$ cd e',
            '$ ls',
            '584 i',
            '$ cd ..',
            '$ cd ..',
            '$ cd d',
            '$ ls',
            '4060174 j',
            '8033020 d.log',
            '5626152 d.ext',
            '7214296 k'
        ]
        self.assertEqual(self.data, expected)

    def test_construct_tree_dirs(self):
        result, _ = Day07.construct_tree(self.data)
        expected = {
            '/': 23352670,
            '/a/': 94269,
            '/d/': 24933642,
            '/a/e/': 584,
        }
        self.assertDictEqual(result, expected)

    def test_construct_tree_tree(self):
        _, result = Day07.construct_tree(self.data)
        expected = {
            '/': ['/a/', '/d/'],
            '/a/': ['/a/e/']
        }
        self.assertDictEqual(result, expected)

    def test_dir_size_a(self):
        result = Day07.dir_size('/a/', self.tree, self.dirs, {})
        self.assertEqual(result, 94853)

    def test_dir_size_d(self):
        result = Day07.dir_size('/d/', self.tree, self.dirs, {})
        self.assertEqual(result, 24933642)

    def test_dir_size_e(self):
        result = Day07.dir_size('/a/e/', self.tree, self.dirs, {})
        self.assertEqual(result, 584)

    def test_dir_size_root(self):
        result = Day07.dir_size('/', self.tree, self.dirs, {})
        self.assertEqual(result, 48381165)

    def test_solve_p1(self):
        result, _ = Day07.solve(self.data)
        self.assertEqual(result, 95437)

    def test_solve_p2(self):
        _, result = Day07.solve(self.data)
        self.assertEqual(result, 24933642)

    def test_solve_alt_p1(self):
        result, _ = Day07.solve_alt(self.data)
        self.assertEqual(result, 95437)

    def test_solve_alt_p2(self):
        _, result = Day07.solve_alt(self.data)
        self.assertEqual(result, 24933642)


if __name__ == '__main__':
    unittest.main()
