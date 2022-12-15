from helper import aoc_timer, sign, Colours
import itertools as it
from typing import Iterator


SOURCE = 500
FLOOR_DY = 2


@aoc_timer
def get_input(path: str) -> Iterator[list[tuple[int, int]]]:
    for line in open(path).read().splitlines():
        yield [(int(x), int(y)) for x, y in
               [pair.split(',') for pair in line.split(' -> ')]]


def process_pair(a: tuple[int], b: tuple[int]) -> set[complex]:
    '''
    Return the set of coordinates in complex space (where x is the
    real part and y is the imaginary part) whose path is traced by
    the given coordinate pair.
    '''
    x1, y1 = a
    dx, dy = (q - p for p, q in zip(a, b))
    return {complex(x1 + x*sign(dx), y1 + y*sign(dy)) for x, y in
            it.product(range(abs(dx) + 1), range(abs(dy) + 1))}


def fall(rock: set[complex], sand: set[complex]) -> complex:
    '''
    Simulate a falling unit of sand until it comes to rest.
    Return its resting position.
    '''
    s = SOURCE
    rest = False
    dy = 1j
    while not rest:
        if (ss := s + dy) not in rock and ss not in sand:
            s = ss
            continue
        for dx in (-1, 1):
            if (ss := s + dy + dx) not in rock and ss not in sand:
                s = ss
                break
        else:
            rest = True
    return s


def draw(rock: set[complex], sand: set[complex], theme: str = 'bw') -> str:
    '''Return a string represenatation of the cave in a given theme.'''
    T = {
        'bw': {
            'source': '+',
            'rock': '#',
            'sand': 'o',
            'air': '.'
        },
        'colour': {
            'source': f'{Colours.fg.RED}+{Colours.ENDC}',
            'rock': f'{Colours.fg.BLUE}#{Colours.ENDC}',
            'sand': f'{Colours.fg.YELLOW}o{Colours.ENDC}',
            'air': '.'
        },
        'xmas': {
            'source': f'{Colours.fg.YELLOW}+{Colours.ENDC}',
            'rock': f'{Colours.fg.RED}#{Colours.ENDC}',
            'sand': f'{Colours.fg.GREEN}o{Colours.ENDC}',
            'air': '.'
        },
    }
    theme = theme if theme in T else 'bw'
    bounds = rock | {SOURCE}
    min_x = int(min(bounds, key=lambda r: r.real).real)
    min_y = int(min(bounds, key=lambda r: r.imag).imag)
    max_x = int(max(bounds, key=lambda r: r.real).real)
    max_y = int(max(bounds, key=lambda r: r.imag).imag)
    cave = ''
    for y in range(min_y, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            r = complex(x, y)
            if r == SOURCE:
                cave += T[theme]['source']
            elif r in rock:
                cave += T[theme]['rock']
            elif r in sand:
                cave += T[theme]['sand']
            else:
                cave += T[theme]['air']
        cave += '\n'
    return cave


@aoc_timer
def solve(data: Iterator[list[tuple[int, int]]],
          vis: bool = False, theme: str = 'bw') -> tuple[int, int]:
    R, S = set(), set()
    for path in data:
        for pair in zip(path, path[1:]):
            R |= process_pair(*pair)
    bottom = int(max(R, key=lambda r: r.imag).imag)
    p2_bottom = bottom + FLOOR_DY
    floor = {complex(x, p2_bottom) for x in
             range(SOURCE - p2_bottom, SOURCE + p2_bottom + 1)}
    R |= floor
    p1 = False
    if vis:
        print(draw(R - floor, S, theme))
    for t in it.count():
        s = fall(R, S)
        if not p1 and s.imag >= bottom:
            p1 = t
            if vis:
                print(draw(R - floor, S, theme))
        S.add(s)
        if SOURCE in R or SOURCE in S:
            p2 = t + 1
            if vis:
                print(draw(R, S, theme))
            return p1, p2
    return None


# %% Output
def main() -> None:
    print("AoC 2022\nDay 14")
    data = get_input('input.txt')
    p1, p2 = solve(data, vis=True, theme='xmas')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
