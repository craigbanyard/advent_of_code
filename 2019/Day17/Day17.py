from helper import aoc_timer
from intcode import IntcodeComputer
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import itertools


def get_routine(path):
    """
    Return a generator for all integers in file at given path.
    Routine generated via trial and error in Excel.

    To auto-solve this, need to write a routing algorithm (e.g. BFS)
    to traverse the scaffold, then a compression algorithm to compress
    the path such that it meets the memory constraints.
    """
    for x in open(path).read().split(','):
        yield int(x)


@aoc_timer
def Day17(program_file, part1=True, debug=False, plot=None, routine_file=None):

    # Constants
    MAP = {
        '.': 0,
        '#': 1,
        '^': 2,
        'v': 2,
        '<': 2,
        '>': 2
    }
    if routine_file is None:
        ROUTINE = get_routine('routine.txt')
    else:
        ROUTINE = get_routine(routine_file)

    def get_input():
        """Function used as input to Intcode VM."""
        out = next(ROUTINE)
        if debug:
            print(chr(out), end='', flush=True)
        return out

    def scaffold_grid(scaffolds):
        """Convert scaffolds string into numeric grid."""
        return [[MAP[ch] for ch in line]
                for line in scaffolds.strip('\n').split('\n')]

    def get_intersections(scaffolds):
        """Return set of coordinates of all scaffold intersections."""
        G = scaffold_grid(scaffolds)
        R, C = len(G), len(G[0])
        intersections = set()
        dirs = [
            (-1, 0),        # Up
            (0, 1),         # Right
            (1, 0),         # Down
            (-1, 0)         # Left
        ]
        for r, c in itertools.product(range(1, R - 1), range(1, C - 1)):
            if G[r][c] == MAP['#']:
                if all(G[r + dr][c + dc] == MAP['#'] for (dr, dc) in dirs):
                    intersections.add((r, c))
        return intersections

    def plot_scaffolds(scaffolds, intersections=None):
        """Matplotlib plot of scaffolds from string representation."""
        G = scaffold_grid(scaffolds)
        colours = [
            'white',               # Space
            'midnightblue',        # Scaffold
            'dodgerblue',          # Robot
        ]
        if intersections is not None:
            # Append intersection colour to colour map
            colours.append('lightsteelblue')
            intersection = max(MAP.values()) + 1
            # Amend intersection values
            for r, c in intersections:
                G[r][c] = intersection
        # Show plot
        plt.figure(figsize=(8, 8))
        plt.imshow(G, cmap=ListedColormap(colours))
        plt.axis('off')
        return None

    # Initialise Intcode program
    VM = IntcodeComputer(program_file, input=get_input)
    if not part1:
        VM.override({0: 2})
    scaffolds = debug_out = "\n"

    while not VM.halted:
        out = VM.run()
        if out not in range(128):
            break
        scaffolds += chr(out)
        # Full debug output
        if debug:
            debug_out += chr(out)
            if out == 10:
                print(debug_out, end='')
                debug_out = ""

    if part1:
        intersections = get_intersections(scaffolds)
        # Plot
        if plot:
            plot_scaffolds(scaffolds, intersections)
        return sum(r * c for r, c in intersections)
    return out


# %% Output
def main():
    print("AoC 2019\nDay 17")
    program_file = 'input.txt'
    print("Part 1:", Day17(program_file, debug=False, plot=True))
    print("Part 2:", Day17(program_file, debug=False, part1=False))
    print()


if __name__ == '__main__':
    main()
