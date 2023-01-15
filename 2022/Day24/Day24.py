from helper import aoc_timer, Colours
from collections import defaultdict, deque
import math
from typing import Iterator


K = {'^': -1j, 'v': 1j, '<': -1, '>': 1}
K_ = {v: k for k, v in K.items()}


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


def scan(data: list[str]) -> tuple[dict[complex, list[complex]],
                                   set[complex]]:
    v = defaultdict(list)
    w = set()
    for r, line in enumerate(data):
        for c, ch in enumerate(line):
            if ch == '.':
                continue
            if ch == '#':
                w.add(complex(c, r))
                continue
            v[complex(c, r)].append(K[ch])
    return v, w


def evolve(v: dict[complex, list[complex]], w: set[complex],
           R: int, C: int) -> dict[complex, list[complex]]:
    v_ = defaultdict(list)
    for p, b in v.items():
        for d in b:
            p_ = p + d
            if p_ in w:
                r = (p_.imag + d.imag) % R
                c = (p_.real + d.real) % C
                v_[complex(c, r)].append(d)
                continue
            v_[p_].append(d)
    return v_


def blizzard(v: dict[complex, list[complex]], w: set[complex],
             R: int, C: int) -> list[dict[complex, list[complex]]]:
    n = math.lcm(R - 1, C - 1)
    result = [v]
    for _ in range(n - 1):
        result.append((v := evolve(v, w, R, C)))
    return result


def valid(e: complex, R: int, C: int) -> bool:
    return 0 <= e.imag <= R and 0 < e.real < C


def neighbours(e: complex, v: dict[complex, list[complex]],
               w: set[complex], R: int, C: int) -> Iterator[complex]:
    for d in K_:
        ee = e + d
        if valid(ee, R, C) and ee not in v and ee not in w:
            yield ee
    if e not in v:
        yield e


def draw(v: dict[complex, list[complex]], w: set[complex],
         R: int, C: int, e: complex | None = None) -> str:
    result = ''
    for r in range(R + 1):
        for c in range(C + 1):
            p = complex(c, r)
            if p == e:
                result += f'{Colours.fg.CYAN}E{Colours.ENDC}'
            elif p in w:
                result += '#'
            elif p not in v:
                result += '.'
            elif (n := len(v[p])) > 1:
                result += str(n)
            else:
                result += K_[v[p][0]]
        result += '\n'
    return result


@aoc_timer
def solve(data: list[str], trips: int = 1, vis: bool = False) -> int:
    R, C = len(data) - 1, len(data[0]) - 1
    start = complex(data[0].index('.'), 0)
    end = complex(data[R].index('.'), R)
    v, w = scan(data)
    if vis:
        print(f'\nInitial state:\n{draw(v, w, R, C, start)}')
    b = blizzard(v, w, R, C)
    n = len(b)
    visited = set()
    Q = deque([(start, 0, 1)])
    while Q:
        e, t, trip = Q.popleft()
        if (e, t % n, trip) in visited:
            continue
        visited.add((e, t % n, trip))
        if e == end:
            if vis:
                print(f'Trip {trip}, steps: {t}\n{draw(v, w, R, C, e)}')
            if trip == trips:
                return t
            start, end = end, start
            trip += 1
            Q = deque([(start, t, trip)])
        v = b[(t + 1) % n]
        for ee in neighbours(e, v, w, R, C):
            Q.append((ee, t + 1, trip))
    return None


# %% Output
def main() -> None:
    print("AoC 2022\nDay 24")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, trips=3, vis=True))


if __name__ == '__main__':
    main()
