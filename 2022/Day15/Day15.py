from helper import aoc_timer, Colours
from collections import defaultdict
import re


# TODO: Would be better as a class with __repr__ for visualisation


@aoc_timer
def get_input(path: str) -> list[tuple[complex, complex]]:
    return [(complex(p, q), complex(r, s)) for p, q, r, s in
            [map(int, re.findall(r'\d+', line)) for line in
             open(path).read().splitlines()]]


def manhattan(a: complex, b: complex) -> int:
    '''Return the Manhattan distance between a and b.'''
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def complex_range(start: complex, stop: complex, step: complex = 1):
    '''Return a generator equivalent to `range` in complex space.'''
    start -= step
    while start != stop:
        start += step
        yield start


def complex_multirange(vertices, steps):
    '''
    Return a generator of the points that lie on the shape traced
    by the given vertices, where the edge between each vertex is
    traced by following the respective step in the steps list.
    '''
    for v1, v2, s in zip(vertices, vertices[1:], steps):
        yield from complex_range(v1, v2, s)


def draw(S: dict[complex, list[complex]],
         B: dict[complex, list[complex]],
         V: set[complex],
         X: set[complex],
         theme: str = 'bw') -> str:
    '''Return a string represenatation of the cave in a given theme.'''
    T = {
        'bw': {
            'sensor': 'S',
            'beacon': 'B',
            'vertex': '+',
            'exclusion': '#',
            'air': '.'
        },
        'colour': {
            'sensor': f'{Colours.fg.GREEN}S{Colours.ENDC}',
            'beacon': f'{Colours.fg.CYAN}B{Colours.ENDC}',
            'vertex': f'{Colours.fg.PURPLE}+{Colours.ENDC}',
            'exclusion': f'{Colours.fg.YELLOW}#{Colours.ENDC}',
            'air': '.'
        },
        'xmas': {
            'sensor': f'{Colours.fg.GREEN}S{Colours.ENDC}',
            'beacon': f'{Colours.fg.RED}B{Colours.ENDC}',
            'vertex': f'{Colours.fg.CYAN}+{Colours.ENDC}',
            'exclusion': f'{Colours.fg.YELLOW}#{Colours.ENDC}',
            'air': '.'
        },
    }
    theme = theme if theme in T else 'bw'
    bounds = S.keys() | B.keys() | V | X
    min_x = int(min(bounds, key=lambda r: r.real).real)
    min_y = int(min(bounds, key=lambda r: r.imag).imag)
    max_x = int(max(bounds, key=lambda r: r.real).real)
    max_y = int(max(bounds, key=lambda r: r.imag).imag)
    tunnels = ''
    for y in range(min_y - 1, max_y + 2):
        tunnels += f'{y:03d} '
        for x in range(min_x - 1, max_x + 2):
            r = complex(x, y)
            if r in S:
                tunnels += T[theme]['sensor']
            elif r in B:
                tunnels += T[theme]['beacon']
            elif r in V:
                tunnels += T[theme]['vertex']
            elif r in X:
                tunnels += T[theme]['exclusion']
            else:
                tunnels += T[theme]['air']
        tunnels += '\n'
    return tunnels


def part1(data: list[tuple[complex, complex]], y: int = 10,
          vis: bool = False, theme: str = 'bw') -> int:
    B, S = defaultdict(list), defaultdict(list)
    V, X = set(), set()
    for s, b in data:
        S[s].append(b)
        B[b].append(s)
        d = manhattan(s, b)
        v = [s + ds*d for ds in [-1j, 1, 1j, -1]]
        vu, _, vd, _ = v
        if vu.imag <= y <= vd.imag:
            if y >= s.imag:
                n = 2 * (int(vd.imag) - y) + 1
            else:
                n = 2 * (y - int(vu.imag)) + 1
            X.update(range(int(s.real) - n//2, int(s.real) + n//2 + 1))
        if vis and y < 1000:
            # Can only visualise the sample (or small) input
            scurr = f'sensor ({int(s.real)}, {int(s.imag)})'
            bcurr = f'beacon ({int(b.real)}, {int(b.imag)})'
            print(f'Processing {scurr} and {bcurr}...')
            V |= set(v)
            print(draw(S, B, V, {x + y*1j for x in X}, theme))
    XB = {b.real for b in B if b.imag == y}
    XS = {s.real for s in S if s.imag == y}
    return len(X - XB - XS), S, B


def part2(S: dict[complex, list[complex]],
          B: dict[complex, list[complex]],
          bound: int = 4000000) -> int:
    sensors = sorted(S.keys(), key=lambda x: manhattan(0, x), reverse=True)
    for s1 in sensors:
        ordered_sensors = sorted(sensors, key=lambda x: manhattan(s1, x))[1:]
        # Report progress since the algorithm is slow...
        print(f'Processing sensor ({int(s1.real)}, {int(s1.imag)})...')
        d = manhattan(s1, S[s1][0])
        v = [s1 + ds*(d + 1) for ds in [-1j, 1, 1j, -1]]
        for p in complex_multirange(v + [v[0]], [1+1j, -1+1j, -1-1j, 1-1j]):
            if not (0 <= p.real <= bound and 0 <= p.imag <= bound):
                continue
            if p in S or p in B:
                continue
            for s2 in ordered_sensors:
                if manhattan(p, s2) <= manhattan(s2, S[s2][0]):
                    break
            else:
                return int(p.real * 4000000 + p.imag)
    return None


@aoc_timer
def solve(data: list[tuple[complex, complex]], y: int = 10,
          bound: int = 20, vis: bool = False, theme: str = 'bw') -> int:
    print('Calculating Part 1... ')
    p1, S, B = part1(data, y, vis, theme)
    print(f'Result = {p1}')
    print('Calculating Part 2...')
    p2 = part2(S, B, bound)
    print(f'Result = {p2}')
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 15")
    data = get_input('input.txt')
    p1, p2 = solve(data, y=2000000, bound=4000000)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
