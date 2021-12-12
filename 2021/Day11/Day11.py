from helper import aoc_timer
import numpy as np
from scipy.ndimage import correlate


KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=int)


@aoc_timer
def get_input(path: str) -> np.ndarray:
    G = []
    for line in open(path).read().splitlines():
        G.append([*line])
    return np.array(G, dtype=int)


def evolve(G: np.ndarray, N=None, F=None) -> tuple[np.ndarray, int]:
    # Initialise neighbours (N) and flashes (F)
    if N is None:
        N = np.full(G.shape, 1, dtype=int)
    if F is None:
        F = np.full(G.shape, False)
    # Evolve grid recursively until no high-energy octopuses (H) remain
    G += N
    H = G > 9
    F |= H
    G[F] = 0
    if np.any(H):
        # Convert H from bool to int to calculate neighbours
        N = correlate(H * 1, KERNEL, mode='constant', cval=0)
        return evolve(G, N, F)
    return G, F.sum()


@aoc_timer
def Day11(G: np.ndarray, steps=100) -> tuple[int, int]:
    p1 = p2 = t = 0
    s1 = s2 = False
    octs = G.size
    while not (s1 and s2):
        t += 1
        G, flashes = evolve(G)
        # Part 1: count flashes up to input timestep
        if t <= steps:
            p1 += flashes
        else:
            s1 = True
        # Part 2: timestep at which all octopuses flash simultaneously
        if not s2 and flashes == octs:
            p2 = t
            s2 = True
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 11")
    data = get_input('input.txt')
    p1, p2 = Day11(G=data, steps=100)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
