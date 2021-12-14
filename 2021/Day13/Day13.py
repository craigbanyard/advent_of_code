from helper import aoc_timer
from collections import defaultdict
import json
from matplotlib import pyplot as plt
import numpy as np


@aoc_timer
def get_input(path: str) -> tuple[set, list, list]:
    '''
    Return a tuple with three elements:
    1. Set of point coordinates (x, y)
    2. List of folds to perform (ax, n)
    3. Dimensions of paper (y, x)
    '''
    AX = {
        'y': 0,
        'x': 1
    }
    coords = set()
    folds = None
    dims = [None, None]
    for line in open(path).read().splitlines():
        if line and folds is None:
            x, y = map(int, line.split(','))
            coords.add((x, y))
        elif not line:
            folds = []
            continue
        else:
            axis, n = line.lstrip('fold along ').split('=')
            axis, n = AX[axis], int(n)
            if dims[axis] is None:
                dims[axis] = 2 * n + 1
            folds.append((axis, n))
    return coords, folds, dims


def ascii(G: np.ndarray) -> str:
    '''Convert 2D numpy array of bool to ASCII art message.'''
    R = len(G)
    C = len(G[0])
    msg = '\n'
    for r in range(R):
        for c in range(C):
            msg += '#' if G[r][c] else ' '
        msg += '\n'
    return msg


def image(G: np.ndarray, **kwargs) -> None:
    '''Plot 2D numpy array of bool as image.'''
    fsize = kwargs.get('figsize', (8, 1))
    plt.figure(figsize=fsize)
    plt.imshow(G, aspect="auto", cmap="Greys")
    plt.axis("off")
    plt.show()
    return None


def ocr(points: set, **kwargs) -> str:
    '''
    Process 2D numpy array of bool as text using OCR.
    Accepts 'chars', 'px' and 'ocr' as keyword arguments.
    Reads OCR coordinate map (.json) from path 'ocr'
    Assumes text is 'chars' characters long,
    and each character is 'px' pixels wide.
    '''
    ocr_file = kwargs.get('ocr', 'ocr.json')
    with open(ocr_file) as f:
        tmp = json.load(f)
    ocr_map = {tuple((x, y) for x, y in sorted(v)): k for k, v in tmp.items()}
    chars = kwargs.get('chars', 8)
    px = kwargs.get('px', 4)
    characters = defaultdict(set)
    for x, y in points:
        characters[x // (px + 1)].add((x % (px + 1), y))
    msg = ['?'] * chars
    for idx, coords in characters.items():
        msg[idx] = ocr_map.get(tuple(sorted(coords)), '?')
    return ''.join(msg)


def coords_to_array(coords: set, dims=None) -> np.ndarray:
    '''Process set of coordinates into 2D numpy array of bool.'''
    if dims is None:
        X, Y = map(lambda x: max(x) + 1, zip(*coords))
    else:
        X, Y = dims
    G = np.zeros((Y, X), dtype=bool)
    for x, y in coords:
        G[y][x] = True
    return G


def array_to_coords(G: np.ndarray) -> set:
    '''Process 2D numpy array of bool into set of coordinates.'''
    return set((x, y) for y, x in zip(*np.where(G)))


def visualise(data, **kwargs):
    '''Visualise data using provided keyword arguments.'''
    f = kwargs.pop('vis', lambda x: None)
    match data, f.__name__:
        case set(), 'ocr':
            pass
        case np.ndarray(), 'ocr':
            data = array_to_coords(data)
        case set(), ('image' | 'ascii'):
            data = coords_to_array(data)
        case np.ndarray(), ('image' | 'ascii'):
            pass
        case _:
            return None
    return f(data, **kwargs)


@aoc_timer
def Day13(data: tuple[set, list, list], **kwargs) -> tuple[int, str]:
    '''
    Initial Day 13 solution using numpy slice and flip.
    Memory inefficient since it involves allocating a dense 2D array.
    '''
    coords, folds, (y, x) = data
    G = coords_to_array(coords, dims=(x, y))
    p1 = None
    for axis, n in folds:
        g1, _, g2 = np.split(G, [n, n + 1], axis)
        G = g1 + np.flip(g2, axis)
        if p1 is None:
            p1 = G.sum()
    p2 = visualise(G, **kwargs)
    return p1, p2


@aoc_timer
def solve(data: tuple[set, list, list], **kwargs) -> tuple[int, str]:
    '''
    Faster, more memory efficient alternative solution to Day 13.
    Uses a set of coordinates that (likely) reduces in size each fold.
    '''
    coords, folds, *_ = data
    p1 = p2 = None
    for axis, n in folds:
        new_coords = set()
        for x, y in coords:
            if axis == 0 and y > n:
                new_coords.add((x, 2 * n - y))
            elif axis == 1 and x > n:
                new_coords.add((2 * n - x, y))
            else:
                new_coords.add((x, y))
        coords = new_coords
        if p1 is None:
            p1 = len(coords)
    p2 = visualise(coords, **kwargs)
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 13")
    data = get_input('input.txt')
    p1, p2 = Day13(data, vis=ocr)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
