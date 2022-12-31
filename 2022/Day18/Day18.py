from helper import aoc_timer
from collections import deque
from matplotlib import pyplot as plt
import numpy as np
import re
from scipy.ndimage import correlate


@aoc_timer
def get_input(path: str) -> np.ndarray:
    '''
    Return a numpy array representation of the lava droplet.
    The array is padded along all axes with zeros such that
    we have space to perform the correlation operation.
    '''
    coords = [tuple(map(int, re.findall(r'\d+', line)))
              for line in open(path).read().splitlines()]
    x, y, z = tuple(map(max, zip(*coords)))
    G = np.pad(np.zeros((x, y, z), dtype=int), (0, 1))
    for x, y, z in coords:
        G[x, y, z] = 1
    return np.pad(G, (1,))


def render(droplet: np.ndarray,
           slice: str | None = None,
           surface: np.ndarray | None = None) -> None:
    '''
    Render the lava droplet as a 3D volumetric plot.
    The plot can be sliced along any combination of axes
    (x, y, z) using the optional `slice` argument.
    The external surface of the droplet can be shaded in
    a different colour to the internal surface by passing
    a numpy array of pixels as the optional `surface`
    argument.
    '''

    if slice is not None:
        mx, my, mz = map(lambda x: x // 2, droplet.shape)
        X, Y, Z = np.indices(droplet.shape)
        if 'x' in slice:
            droplet &= (X < mx)
        if 'y' in slice:
            droplet &= (Y < my)
        if 'z' in slice:
            droplet &= (Z < mz)

    colours = np.empty_like(droplet, dtype=object)
    colours[np.where(droplet == 1)] = 'mediumvioletred'
    if surface is not None:
        colours[np.where(surface > 0)] = 'darkmagenta'
        colours[np.where(surface > 2)] = 'rebeccapurple'
        colours[np.where(surface > 4)] = 'indigo'

    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(droplet, facecolors=colours, edgecolor='k')
    ax.set_box_aspect([1, 1, 1])
    plt.axis('off')
    plt.show()


@aoc_timer
def solve(G: np.ndarray, vis: bool = False, **kwargs) -> tuple[int, int]:

    KERNEL = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    ], dtype=int)

    D = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]

    C = np.where(G == 0, correlate(G, KERNEL), 0)
    X, Y, Z = G.shape

    def neighbours(x, y, z):
        for dx, dy, dz in D:
            xx, yy, zz = x + dx, y + dy, z + dz
            if 0 <= xx < X and 0 <= yy < Y and 0 <= zz < Z:
                yield xx, yy, zz

    visited = {}
    Q = deque([(0, 0, 0)])
    while Q:
        x, y, z = Q.popleft()
        if (x, y, z) in visited:
            continue
        visited[(x, y, z)] = C[x, y, z]
        if G[x, y, z]:
            continue
        for xx, yy, zz in neighbours(x, y, z):
            Q.append((xx, yy, zz))

    if vis:
        surface = np.zeros_like(G)
        for (x, y, z), v in visited.items():
            if not v:
                continue
            for xx, yy, zz in neighbours(x, y, z):
                if G[xx, yy, zz]:
                    surface[xx, yy, zz] += 1
        render(G, kwargs.get('slice', None), surface)

    return C.sum(), sum(visited.values())


# %% Output
def main() -> None:
    print("AoC 2022\nDay 18")
    data = get_input('input.txt')
    p1, p2 = solve(data, vis=True, slice='z')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
