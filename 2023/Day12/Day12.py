# %% Day 12
from helper import aoc_timer
from functools import cache


@aoc_timer
def get_input(path: str) -> list[tuple[str, tuple[int]]]:
    result = []
    for line in open(path).read().splitlines():
        record, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        result.append((record, groups))
    return result


@cache
def arrangements(r: str, g: tuple[int]) -> int:
    '''
    Recursively determine the number of valid arrangements of the condition
    record `r` versus the groups of damaged springs `g`. Uses functools.cache
    for memoization (caching).
    '''
    if not g:
        if '#' not in r:
            return 1
        return 0
    if not r:
        return 0

    rr, gg = r[0], g[0]

    if rr == '.':
        return arrangements(r[1:], g)

    if rr == '#':
        if len(r) < gg or '.' in r[:gg]:
            return 0
        if len(r) == gg:
            if len(g) == 1:
                return 1
            return 0
        if r[gg] in '?.':
            return arrangements(r[gg + 1:], g[1:])

    if rr == '?':
        return arrangements('.' + r[1:], g) + arrangements('#' + r[1:], g)

    return 0


def unfold(r: str, g: tuple[int], n: int) -> tuple[str, tuple[int]]:
    '''Unfold the condition records `n - 1` times to produce `n` copies.'''
    r = (r + '?') * (n - 1) + r
    g *= n
    return r, g


@aoc_timer
def solve(data: list[tuple[str, tuple[int]]], n: int = 1) -> int:
    return sum(arrangements(*unfold(r, g, n)) for r, g in data)


def main() -> None:
    print("AoC 2023\nDay 12")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, n=5))


if __name__ == '__main__':
    main()
