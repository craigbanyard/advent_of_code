from helper import aoc_timer
from collections import deque
import itertools as it


@aoc_timer
def get_input(path: str) -> set[complex]:
    E = set()
    for r, line in enumerate(open(path).read().splitlines()):
        for c, ch in enumerate(line):
            if ch == '#':
                E.add(complex(c, r))
    return E


def grove_bounds(elves: set[complex]) -> tuple[int]:
    rmin = int(min(elves, key=lambda x: x.imag).imag)
    rmax = int(max(elves, key=lambda x: x.imag).imag) + 1
    cmin = int(min(elves, key=lambda x: x.real).real)
    cmax = int(max(elves, key=lambda x: x.real).real) + 1
    return rmin, rmax, cmin, cmax


def grove_size(elves: set[complex]) -> int:
    rmin, rmax, cmin, cmax = grove_bounds(elves)
    return (rmax - rmin) * (cmax - cmin)


def draw(elves: set[complex]) -> str:
    result = ''
    rmin, rmax, cmin, cmax = grove_bounds(elves)
    for r in range(rmin, rmax):
        for c in range(cmin, cmax):
            if complex(c, r) in elves:
                result += '#'
            else:
                result += '.'
        result += '\n'
    return result


def no_elf(elf: complex, elves: set[complex],
           dirs: list[complex]) -> bool:
    for d in dirs:
        if elf + d in elves:
            return False
    return True


def move(elves: set[complex], D: deque[complex]) -> set[complex]:
    M = {}
    for elf in elves:
        if no_elf(elf, elves, D):
            M[elf] = elf
            continue
        for d in range(0, 12, 3):
            dir = list(it.islice(D, d, d + 3))
            if no_elf(elf, elves, dir):
                elf_ = elf + dir[1]
                if elf_ in M:
                    other = M.pop(elf_)
                    M[other] = other
                    M[elf] = elf
                else:
                    M[elf_] = elf
                break
        else:
            M[elf] = elf
    return set(M.keys())


@aoc_timer
def solve(elves: set[complex], rounds: int | None = None,
          part1: bool = True) -> int:

    N = len(elves)
    D = deque([
        -1-1j, -1j, 1-1j,   # North
        -1+1j, 1j, 1+1j,    # South
        -1-1j, -1, -1+1j,   # West
        1-1j, 1, 1+1j       # East
    ])

    for round in it.count(start=1):
        if elves == (elves := move(elves, D)):
            break
        D.rotate(-3)
        if part1 and round == rounds:
            return grove_size(elves) - N
    return round


# %% Output
def main() -> None:
    print("AoC 2022\nDay 23")
    data = get_input('input.txt')
    print("Part 1:", solve(data, rounds=10))
    print("Part 2:", solve(data, part1=False))


if __name__ == '__main__':
    main()
