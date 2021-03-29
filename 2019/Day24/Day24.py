from helper import aoc_timer
import numpy as np
import itertools
from collections import defaultdict
from scipy.ndimage import correlate


class Day24:
    """Class for Day 24 layout grids."""

    # Class constants (independent of initialisation args)
    DIRS = [
        (-1, 0),        # Up
        (0, 1),         # Right
        (1, 0),         # Down
        (0, -1)         # Left
    ]

    def __init__(self, path):
        # Construct initial layout
        self.path = path
        self.layout = self.get_grid()
        # Instance constants (dependent on initialisation args)
        self.DIMS = self.layout.shape
        self.MID = tuple(x//2 for x in self.DIMS)
        self.INNER = self.get_inner()
        self.OUTER = self.get_outer()
        # Part 1 instance variables
        self.seen = set()
        # Part 2 instance variables
        self.empty = np.zeros(self.DIMS, dtype=int)
        self.adjacency = self.get_adjacency()

    def get_input(self):
        """Read input file into list."""
        return [x.strip() for x in open(self.path).readlines()]

    def get_grid(self):
        """Convert ASCII list into numpy binary array."""
        data = self.get_input()
        # Dimensions: assume non-jagged but not necessarily square
        R, C = len(data), len(data[0])
        G = np.zeros((R, C), dtype=int)
        for r, line in enumerate(data):
            G[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
        return G

    def get_inner(self):
        """Get inner tiles based on layout size."""
        RM, CM = self.MID
        return {(RM + dr, CM + dc) for (dr, dc) in self.DIRS}

    def get_outer(self):
        """Get outer tiles based on layout size."""
        R, C = self.DIMS
        return {
            (r, c) for r, c in itertools.product(range(R), range(C))
            if r in (0, R - 1) or c in (0, C - 1)
        }

    def get_adjacency(self):
        """Get the full tile adjacency dictionary."""
        adj = defaultdict(set)
        RM, CM = self.MID
        R, C = self.DIMS
        # Get inter-depth adjacency
        for r, c in self.INNER:
            if r == RM - 1:
                # Top <-> Top
                for rr, cc in self.OUTER:
                    if not rr:
                        adj[(r, c)].add((1, rr, cc))
                        adj[(rr, cc)].add((-1, r, c))
            if r == RM + 1:
                # Bottom <-> Bottom
                for rr, cc in self.OUTER:
                    if rr == R - 1:
                        adj[(r, c)].add((1, rr, cc))
                        adj[(rr, cc)].add((-1, r, c))
            if c == CM - 1:
                # Left <-> Left
                for rr, cc in self.OUTER:
                    if not cc:
                        adj[(r, c)].add((1, rr, cc))
                        adj[(rr, cc)].add((-1, r, c))
            if c == CM + 1:
                # Right <-> Right
                for rr, cc in self.OUTER:
                    if cc == C - 1:
                        adj[(r, c)].add((1, rr, cc))
                        adj[(rr, cc)].add((-1, r, c))
        # Add intra-depth adjacency
        for r, c in itertools.product(range(R), range(C)):
            if (r, c) == self.MID:
                continue
            for dr, dc in self.DIRS:
                rr = r + dr
                cc = c + dc
                # Outer depth - already processed
                if rr not in range(R) or cc not in range(C):
                    continue
                # Inner depth - already processed
                if (rr, cc) == self.MID:
                    continue
                # Current depth
                adj[(r, c)].add((0, rr, cc))
        return adj

    def recursed(self):
        """Check whether the layout has recursed from depth zero."""
        return self.layout.shape != self.DIMS

    def bio(self, dim=None):
        """
        Calculate biodiversity rating of a single dimension (dim)
        of a possibly multi-dimensional layout grid.
        If the optional dim argument is omitted, it is assumed
        that the layout is already a single dimension.
        """
        if dim is None:
            G = self.layout
        else:
            G = self.layout[dim]
        return G.flatten().dot(1 << np.arange(G.size))

    def pad(self):
        """Add empty inner and outer depths if not already empty."""
        if not self.recursed():
            self.layout = np.stack([
                self.empty,
                self.layout,
                self.empty
            ])
            return None
        if self.bio(0):
            self.layout = np.concatenate([
                [self.empty],
                self.layout
            ])
        if self.bio(-1):
            self.layout = np.concatenate([
                self.layout,
                [self.empty]
            ])
        return None

    def get_bugs(self):
        """Return set of active bug tiles."""
        return {tuple(x) for x in 
                np.transpose(np.where(self.layout))}

    def evolve(self):
        """Perform one timestep grid evolution for part 1."""
        if self.recursed():
            raise ValueError("Layout has already recursed, " +
            "cannot evolve using this method.")
        G = self.layout
        kernel = np.array([
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ], dtype=int)
        nei = correlate(G, kernel, mode='constant', cval=0)
        nxt = G.copy()
        nxt[(G == 0) & ((nei == 1) | (nei == 2))] = 1
        nxt[(G == 1) & (nei != 1)] = 0
        self.layout = nxt
        return None

    def evolve_recurse(self):
        """Perform one timestep grid evolution for part 2."""
        self.pad()
        G = self.layout
        bugs = self.get_bugs()
        nei = np.zeros(G.shape, dtype=int)
        nxt = G.copy()
        for d, r, c in bugs:
            for dd, rr, cc in self.adjacency[(r, c)]:
                if (d + dd, rr, cc) in bugs:
                    nei[d][r][c] += 1
                else:
                    nei[d + dd][rr][cc] += 1
        nxt[(G == 0) & ((nei == 1) | (nei == 2))] = 1
        nxt[(G == 1) & (nei != 1)] = 0
        self.layout = nxt
        return None

    def __repr__(self):
        """ASCII representation of layout."""
        if self.recursed():
            G = self.layout
        else:
            G = np.expand_dims(self.layout, axis=0)
        out = ""
        I, J, K = G.shape
        for i in range(I):
            if not G[i].sum():
                continue
            if I > 1:
                # Works if layout extended symmetrically
                out += f'Depth {i - I//2}:\n'
            for j in range(J):
                for k in range(K):
                    if I > 1 and (j, k) == self.MID:
                        out += '?'
                    elif G[i][j][k]:
                        out += '#'
                    else:
                        out += '.'
                out += '\n'
            out += '\n'
        return out

    @aoc_timer
    def solve_p1(self):
        """Solve part 1."""
        while True:
            b = self.bio()
            if b in self.seen:
                return b
            self.seen.add(b)
            self.evolve()

    @aoc_timer
    def solve_p2(self, timesteps=200):
        """Solve part 2."""
        for _ in range(timesteps):
            self.evolve_recurse()
        return self.layout.sum()


# %% Output
def main():
    print("AoC 2019\nDay 24")
    eris = Day24('input.txt')
    print("Part 1:", eris.solve_p1())
    eris = Day24('input.txt')
    print("Part 2:", eris.solve_p2())


if __name__ == '__main__':
    main()
