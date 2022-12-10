from helper import aoc_timer
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[tuple[str, int]]:
    yield from [(d, int(n)) for d, n in [line.split()
                for line in open(path).read().splitlines()]]


def sign(n: int) -> int:
    '''Return the sign of n.'''
    if n == 0:
        return 0
    return (-1, 1)[n > 0]


def adjacent(h: complex, t: complex) -> bool:
    '''Determine whether two complex points are adjacent.'''
    return abs(h - t) <= abs(1 + 1j)


def follow(h: complex, t: complex) -> complex:
    '''Return the distance t must move to follow h.'''
    move = 0
    if adjacent(h, t):
        return move
    if h.real == t.real:
        # Same vertical plane
        move += sign(h.imag - t.imag) * 1j
    elif h.imag == t.imag:
        # Same horizonal plane
        move += sign(h.real - t.real)
    else:
        # Diagonally apart
        move += sign(h.real - t.real) + sign(h.imag - t.imag) * 1j
    return move


@aoc_timer
def solve(data: Iterator[tuple[str, int]],
          knots: list[int]) -> tuple[int, ...]:
    D = {
        'U': 1j,
        'R': 1,
        'D': -1j,
        'L': -1,
    }
    s = 0
    rope = [s] * max(knots)
    visited = {k - 1: set([s]) for k in knots}
    for d, n in data:
        for _ in range(n):
            rope[0] += D[d]
            for k, (h, t) in enumerate(zip(rope, rope[1:]), start=1):
                rope[k] += follow(h, t)
                if k in visited:
                    visited[k].add(rope[k])
    return tuple(len(v) for _, v in visited.items())


# %% Output
def main() -> None:
    print("AoC 2022\nDay 09")
    data = get_input('input.txt')
    p1, p2 = solve(data, knots=[2, 10])
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
