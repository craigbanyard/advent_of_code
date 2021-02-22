from helper import aoc_timer
import numpy as np
from collections import deque


@aoc_timer
def get_input(path):
    return {int(k.strip('Tile ')): v.split('\n') for k, v in
            [x.strip().split(':\n') for x in open(path).read().split('\n\n')]}


def get_grid(tile):
    """Convert tile as list of strings (#.) into numpy array [1, 0]"""
    m, n = len(tile), len(tile[0])
    grid = np.zeros((m, n), dtype=int)
    for r, line in enumerate(tile):
        grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
    return grid


def rotate(tile, k=1):
    """Rotate a tile counter-clockwise 90 degress k times."""
    return np.rot90(tile, k)


def flip(tile, axis=None, diag=None):
    """
    Flip a tile along a given axis:
        axis=0       vertically
        axis=1       horizontally
        axis=None    diagonally twice = R2
    Single diagonal flips (group theory):
        d0 = (r1 o f0) = flip along y = -x
        d1 = (r1 o f1) = flip along y = x
    """
    if diag:
        tile = rotate(tile, 1)
    return np.flip(tile, axis)


def from_bin(arr):
    """Convert from binary to decimal using bitwise left shift."""
    ans = 0
    for n in arr:
        ans = (ans << 1) | n
    return ans


def extract_bin(tile, edge):
    """
    Extract given edge (edges numbered as in the diagram below) as a binary array.

          0
        3   1
          2

    Return a list of two decimal representations of the edge as read:
      1. forwards (left-to-right)
      2. backwards (right-to-left)

    """
    E = {
        0: lambda a: a[0],
        1: lambda a: a[:, -1],
        2: lambda a: a[-1],
        3: lambda a: a[:, 0]
    }
    bw = flip(fw := E[edge](tile))
    return list(map(from_bin, (fw, bw)))


def crop(tile, n=1):
    """Crop the outermost "pixels" of the tile."""
    return tile[n:-n, n:-n]


def translate(tile, op):
    """Apply a D8 translation (e.g. 'R2') to a whole tile."""
    o, n = op
    T = {
        'R': lambda tile, n: rotate(tile, n),
        'F': lambda tile, n: flip(tile, n),
        'D': lambda tile, n: flip(tile, n, True)
    }
    return T[o](tile, int(n))


def trans_edge(edge, op):
    """Apply a D8 translation (e.g. 'R2') to a given edge."""
    o, n = op
    # New direction of edge after op
    D = {
        'R': lambda e, n: (e - n) % 4,
        'F': lambda e, n: (e, (e - 2) % 4)[e % 2 == n],
        'D': lambda e, n: ((e + 1) % 4, (e - 1) % 4,)[e % 2 == n]
    }
    # Edge forwards/backwards after op
    evn = [0, 1, 1, 0]
    odd = [0, 0, 1, 1]
    F = {
        'R': lambda e, n: (odd[n], evn[n])[e % 2 == 0],
        'F': lambda e, n: (1 - n, n)[e % 2 == 0],
        'D': lambda e, n: n
    }
    return D[o](edge, int(n)), F[o](edge, int(n))


def scale_idx(idx, tlen, imlen):
    """
    For a tile at position idx in a tile-mapping array, return
    the slice that represents this position in the final image.
    """
    r, c = idx
    if r < 0:
        r = imlen + r
    if c < 0:
        c = imlen + c
    rr = slice(tlen * r, tlen * (r + 1))
    cc = slice(tlen * c, tlen * (c + 1))
    return (rr, cc)


@aoc_timer
def Day20(data, part1=True, p1_data=None):

    # Part 1
    if part1:

        # Full tiles
        G = {k: get_grid(v) for k, v in data.items()}

        # Forwards and backwards edges, integers from binary
        E = {}
        for n, tile in G.items():
            for edge in range(4):
                E[(n, edge)] = extract_bin(tile, edge)

        # Dictionaries for matching edges:
        #     M: Map of matches - used to form the image (part 2)
        #     N: Count of matches - if this equals 2, we have a corner (part 1)
        M, N = {}, {k: 0 for k in G.keys()}
        for (n, m), (fw, bw) in E.items():
            for (p, q), (e, _) in E.items():
                if p == n or ((n, m)) in M:
                    continue
                if fw == e:
                    M[(n, m)] = (p, q, 0)
                    N[n] += 1
                elif bw == e:
                    M[(n, m)] = (p, q, 1)
                    N[n] += 1

        # Find corners
        p1 = 1
        for tile, n in N.items():
            if n == 2:
                p1 *= tile

        return p1, (G, M, N)

    # Part 2
    G, M, N = p1_data

    # Monster pattern to find
    mnstr = get_grid([
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]).nonzero()

    # Centre sea monster tail on (0, 0)
    mrows = mnstr[0] - 1
    mcols = mnstr[1]
    NESSY = set(zip(mrows, mcols))

    # Remove borders from each tile
    G = {k: crop(v, 1) for k, v in G.items()}
    imlen = int((ntiles := len(G)) ** 0.5)
    tlen = len(G[next(iter(G))])
    shp = imlen * tlen

    # Arbitrarily pick a starting corner tile
    first = next(iter(sorted(N.items(), key=lambda item: item[1])))[0]
    fedges = tuple(sorted(n for (m, n), (p, q, f) in M.items() if m == first))

    orien = {
        (0, 1): (-1, 0),
        (1, 2): (0, 0),
        (2, 3): (0, -1),
        (0, 3): (-1, -1)
    }

    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    # Translations required to match two edges forwards (group theory)
    FW = {
        0: ['F0', 'D0', 'R0', 'R1'],
        1: ['D0', 'F1', 'R3', 'R0'],
        2: ['R0', 'R1', 'F0', 'D0'],
        3: ['R3', 'R0', 'D0', 'F1']
    }

    # Translations required to match two edges backwards (group theory)
    BW = {
        0: ['R2', 'R3', 'F1', 'D1'],
        1: ['R1', 'R2', 'D1', 'F0'],
        2: ['F1', 'D1', 'R2', 'R3'],
        3: ['D1', 'F0', 'R1', 'R2']
    }

    trans = (FW, BW)

    # Place arranged tile IDs in array
    image = np.empty((shp, shp))
    image[:] = np.NaN
    idx = orien[fedges]
    image[scale_idx(idx, tlen, imlen)] = G[first]

    Q = deque()
    for e in fedges:
        Q.append((first, e, e, 0, idx))
    placed = {first}
    while Q and len(placed) < ntiles:
        tile, edge, direc, bw, idx = Q.popleft()
        mtile, medge, mbw = M[(tile, edge)]
        if mtile in placed:
            continue
        nidx = tuple(sum(x) for x in zip(idx, (dr[direc], dc[direc])))
        placed.add(mtile)
        op = trans[bw ^ mbw][direc][medge]
        image[scale_idx(nidx, tlen, imlen)] = translate(G[mtile], op)
        for nedge in tuple(sorted(n for (m, n), (_, _, _) in M.items()
                                  if m == mtile and n != medge)):
            ndirec, mbw = trans_edge(nedge, op)
            Q.append((mtile, nedge, ndirec, mbw, nidx))

    # Search image for Nessy, if none, next orientation
    ops = ['R0', 'R1', 'R2', 'R3', 'F0', 'F1', 'D0', 'D1']
    for op in ops:
        newimage = translate(image, op)
        ONES = set(zip(*np.nonzero(newimage)))
        SM = set()
        for r, c in ONES:
            cnt = 0
            for dr, dc in NESSY:
                if (r + dr, c + dc) in ONES:
                    cnt += 1
                else:
                    break
            if cnt == len(NESSY):
                SM.add((r, c))
        if len(SM) > 0:
            return len(ONES) - len(SM) * len(NESSY)

    # If we get to this point, there's been a monumental fuck up
    return False


# %% Output
def main():
    """
    Solution makes use of the group of symmetries of the square:
    http://mathonline.wikidot.com/the-group-of-symmetries-of-the-square
    """
    print("AoC 2020\nDay 20")
    data = get_input('input.txt')
    p1, p1_data = Day20(data, True)
    print("Part 1:", p1)
    print("Part 2:", Day20(data, False, p1_data))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 362 µs ± 1.74 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit Day20(data, True)
# 94.2 ms ± 164 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

# %timeit Day20(data, False, p1_data)
# 28.6 ms ± 36.1 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
