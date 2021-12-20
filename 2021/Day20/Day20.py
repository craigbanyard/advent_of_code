from helper import aoc_timer
import numpy as np
from scipy.ndimage import correlate


KERNEL = 2 ** np.arange(9)[::-1].reshape(3, 3)


@aoc_timer
def get_input(path):
    M = {
        '.': 0,
        '#': 1
    }
    alg, img = open(path).read().split('\n\n')
    A = np.array([M[c] for c in alg], dtype=int)
    G = np.array([[M[c] for c in line] for line in img.splitlines()], dtype=int)
    return A, G


def enhance(A, G, t):
    t %= 2
    G = np.pad(G, [(1,)], mode='constant', constant_values=t)
    idx = correlate(G, KERNEL, mode='constant', cval=t)
    return A[idx]


@aoc_timer
def Day20(data, steps=2):
    A, G = data
    flip_indicator = A[0]
    if flip_indicator:
        assert not A[-1], "Infinite lights, forever!"
    for t in range(steps):
        G = enhance(A, G, t * flip_indicator)
    return G.sum()


# %% Output
def main():
    print("AoC 2021\nDay 20")
    data = get_input('input.txt')
    print("Part 1:", Day20(data, steps=2))
    print("Part 2:", Day20(data, steps=50))


if __name__ == '__main__':
    main()
