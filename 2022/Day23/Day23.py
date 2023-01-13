from helper import aoc_timer
from collections import deque
import itertools as it
import numpy as np
from scipy.ndimage import correlate


# NumPy/SciPy solution

KERNEL_N = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0]
], dtype=int)
KERNEL_W = np.rot90(KERNEL_N)
KERNEL_S = np.rot90(KERNEL_W)
KERNEL_E = np.rot90(KERNEL_S)
KERNEL = KERNEL_N | KERNEL_W | KERNEL_S | KERNEL_E


@aoc_timer
def get_input_np(path: str) -> np.ndarray:
    M = {'.': 0, '#': 1}
    G = [[M[c] for c in line]
         for line in open(path).read().splitlines()]
    return np.array(G, dtype=bool)


def bounding_box_np(G: np.ndarray) -> np.ndarray:
    rows = np.any(G, axis=1)
    cols = np.any(G, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return G[rmin:rmax+1, cmin:cmax+1]


def move_np(G, kernel_cycle):
    G = np.pad(G, [(1,)], mode='constant', constant_values=0)
    G_ = G * ((correlate(G, KERNEL, mode='constant') * G) > 0)
    P = np.zeros_like(G_, dtype=bool)   # Proposed
    M = np.zeros_like(G_, dtype=bool)   # Moved
    C = np.zeros_like(G_, dtype=bool)   # Collisions
    rollback = []
    # Propose movements
    for k, d, ax in kernel_cycle:
        H = ~P * G_ * ((correlate(G, k, mode='constant') * G_) == 0)
        P |= H
        m = np.roll(H, d, ax)
        C |= (M & m)
        M |= m
        rollback.append((-d, ax))
    # Rollback collisions
    R = ~P & G
    if C.any():
        for d, ax in rollback:
            R |= (np.roll(C, d, ax) & G)
    return bounding_box_np(M & ~C | R)


def draw_np(G: np.ndarray) -> str:
    return '\n'.join(''.join('#' if c else '.' for c in r) for r in G)


@aoc_timer
def solve_np(data: np.ndarray, rounds: int | None = None,
             part1: bool = True) -> int:
    kernel_cycle = deque([
        (KERNEL_N, -1, 0),
        (KERNEL_S, 1, 0),
        (KERNEL_W, -1, 1),
        (KERNEL_E, 1, 1),
    ])
    G = data
    for round in it.count(start=1):
        if np.array_equal(G, (G := move_np(G, kernel_cycle))):
            break
        if part1 and round == rounds:
            return (~G).sum()
        kernel_cycle.rotate(-1)
    return round


# Base Python solution

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
          part1: bool = True, vis: bool = False) -> int:

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
    print("\nBase Python solution...")
    data = get_input('input.txt')
    print("Part 1:", solve(data, rounds=10))
    print("Part 2:", solve(data, part1=False))
    print("\nNumPy/SciPy solution...")
    data = get_input_np('input.txt')
    print("Part 1:", solve_np(data, rounds=10))
    print("Part 2:", solve_np(data, part1=False))


if __name__ == '__main__':
    main()
