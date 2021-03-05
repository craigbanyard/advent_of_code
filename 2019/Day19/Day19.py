from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque
import numpy as np
import matplotlib.pyplot as plt


@aoc_timer
def Day19(program_file, part2=False, plot=False, mpl=True):

    # Constants
    P1_SEARCH = 50
    SHIP_SIZE = 99

    def get_input():
        """Used as input function to Intcode VM."""
        return Q.popleft()

    def tractor(x, y):
        """Check whether a coordinate (x, y) is affected by the tractor beam."""
        Q.append(x)
        Q.append(y)
        VM.reset()
        return VM.run()

    def draw_beam(plot, mpl, G):
        """Draw tractor beam in given style."""
        if plot:
            if mpl:
                plt.figure(figsize=(8, 8))
                plt.imshow(G.view(int), cmap='gray')
                plt.axis('off')
            else:
                for line in G:
                    for ch in line:
                        print(ch, end='')
                    print()

    # Search dimensions
    X0, Y0 = 0, 0
    X, Y = P1_SEARCH, P1_SEARCH
    if part2:
        X += SHIP_SIZE * 12    # Should be large enough
        Y += SHIP_SIZE * 12
        Y0 += 2 * SHIP_SIZE    # Ship has to be at least this far

    Q = deque()
    affected = 0
    G = np.full((Y, X), ".", dtype=str)
    VM = IntcodeComputer(program_file, input=get_input)

    for y in range(Y0, Y):
        found = False
        for x in range(X0, X):
            if tractor(x, y):
                # Coordinate affected by tractor beam
                affected += 1
                found = True
                if not X0:
                    X0 = x
                G[y][x] = "#"
            elif found:
                # Rest of row won't be affected
                G[y][x] = "."
                break
            else:
                # Keep searching
                X0 = 0
                G[y][x] = "."

            # Check if ship can fit for part 2
            if found and part2:
                # Up-right
                if not tractor(x + SHIP_SIZE, y - SHIP_SIZE):
                    break
                # Right
                if not tractor(x + SHIP_SIZE, y):
                    break
                # Up
                if tractor(x, y - SHIP_SIZE):
                    G[(y - SHIP_SIZE):y][x:(x + SHIP_SIZE)] = "O"
                    G = G[:(y + 5)][:(x + 5)]
                    draw_beam(plot, mpl, G)
                    return (x * 10000) + y - SHIP_SIZE

    draw_beam(plot, mpl, G)
    return affected


# %% Output
def main():
    print("AoC 2019\nDay 19")
    program_file = 'input.txt'
    print("Part 1:", Day19(program_file, plot=True, mpl=False))
    print("Part 2:", Day19(program_file, part2=True))


if __name__ == '__main__':
    main()
