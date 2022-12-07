from helper import aoc_timer
from collections import defaultdict
import re


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str]) -> tuple[int, int]:

    DMAX = 100000
    DISK = 70000000
    NEED = 30000000

    dirs = defaultdict(int)
    tree = defaultdict(list)
    parent = {}
    totals = {}
    curr = ''

    for cmd in data:
        match cmd.split():
            case ['$', 'cd', '/']:
                curr = '/'
            case ['$', 'cd', '..']:
                curr = parent[curr]
            case ['$', 'cd', d]:
                curr += f'{d}/'
            case ['$', 'ls']:
                pass
            case ['dir', d]:
                d = curr + f'{d}/'
                tree[curr].append(d)
                parent[d] = curr
            case [s, _]:
                dirs[curr] += int(s)
            case _:
                assert False, f'Unexpected terminal output: {cmd}.'

    def dir_size(dir, tree, dirs):
        '''Naive (non-DP) recursive directory walk.'''
        total = dirs[dir]
        if dir not in tree:
            return total
        for sub_dir in tree[dir]:
            total += dir_size(sub_dir, tree, dirs)
        return total

    def dir_size_memo(dir, tree, dirs, memo):
        '''DP version of dir_size function.'''
        if dir in memo:
            return memo[dir]
        memo[dir] = dirs[dir]
        if dir not in tree:
            return memo[dir]
        for sub_dir in tree[dir]:
            memo[dir] += dir_size_memo(sub_dir, tree, dirs, memo)
        return memo[dir]

    p1, p2 = 0, NEED
    unused = DISK - dir_size_memo('/', tree, dirs, {})
    to_delete = NEED - unused

    all_dirs = set(dirs.keys()) | set(tree.keys())
    for dir in all_dirs:
        totals[dir] = dir_size_memo(dir, tree, dirs, {})
        if totals[dir] <= DMAX:
            p1 += totals[dir]
        if totals[dir] > to_delete:
            p2 = min(p2, totals[dir])

    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 07")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
