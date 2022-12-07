from helper import aoc_timer
from collections import defaultdict
from itertools import accumulate
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    yield from open(path).read().splitlines()


def construct_tree(data: Iterator[str]) -> tuple[dict[str, int],
                                                 dict[str, list[str]]]:
    '''
    Returns two dictionaries, both with directories as keys:
      dirs: size of immediately contained files by directory
      tree: list of subdirectories by directory
    '''
    dirs = defaultdict(int)
    tree = defaultdict(list)
    curr = []

    for cmd in data:
        match cmd.split():
            case ['$', 'cd', '/']:
                curr = ['/']
            case ['$', 'cd', '..']:
                curr.pop()
            case ['$', 'cd', d]:
                curr.append(f'{d}/')
            case ['$', 'ls']:
                pass
            case ['dir', d]:
                cd = ''.join(curr)
                tree[cd].append(f'{cd}{d}/')
            case [s, _]:
                cd = ''.join(curr)
                dirs[cd] += int(s)
            case _:
                assert False, f'Unexpected terminal output: {cmd}.'

    return dirs, tree


def dir_size(dir: str, tree: dict[str, list[str]],
             dirs: dict[str, int], memo: dict[str, int]) -> int:
    '''
    Return the size of a given directory by recursively walking
    its directory structure. Uses dynamic programming (DP) such
    that the memo dictionary can be utilised after calling this
    function.
    '''
    if dir in memo:
        return memo[dir]
    memo[dir] = dirs[dir]
    if dir not in tree:
        return memo[dir]
    for sub_dir in tree[dir]:
        memo[dir] += dir_size(sub_dir, tree, dirs, memo)
    return memo[dir]


@aoc_timer
def solve(data: list[str]) -> tuple[int, int]:
    '''Recursive solution.'''
    DMAX = 100000
    DISK = 70000000
    NEED = 30000000

    dirs, tree = construct_tree(data)
    totals = {}

    # Calling dir_size on the root ('/') fully populates the totals dict
    unused = DISK - dir_size('/', tree, dirs, totals)
    delete = NEED - unused

    p1 = sum(v for _, v in totals.items() if v <= DMAX)
    p2 = min(v for _, v in totals.items() if v > delete)

    return p1, p2


@aoc_timer
def solve_alt(data: Iterator[str]) -> tuple[int, int]:
    '''Non-recursive solution.'''
    DMAX = 100000
    DISK = 70000000
    NEED = 30000000

    dirs = defaultdict(int)
    curr = []
    for cmd in data:
        match cmd.split():
            case ['$', 'cd', '/']:
                curr = ['/']
            case ['$', 'cd', '..']:
                curr.pop()
            case ['$', 'cd', d]:
                curr.append(d)
            case ['$', 'ls']:
                pass
            case ['dir', _]:
                pass
            case [s, _]:
                for d in accumulate(curr, func=lambda a, b: f'{a}/{b}'):
                    dirs[d] += int(s)
            case _:
                assert False, f'Unexpected terminal output: {cmd}.'

    unused = DISK - dirs['/']
    delete = NEED - unused

    p1 = sum(v for _, v in dirs.items() if v <= DMAX)
    p2 = min(v for _, v in dirs.items() if v > delete)

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
