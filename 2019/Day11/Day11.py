from helper import aoc_timer
from intcode import IntcodeComputer
import matplotlib.pyplot as plt


# %% Day 11 Solver
@aoc_timer
def Day11(program_file, grid_init, part1=True, asc=False, mpl=False):

    # Function to get current tile colour
    def get_input():
        return G[r][c]

    # Set up grid
    R, C = grid_init
    G = [[0 for _ in range(C)] for _ in range(R)]
    d = 0
    dR, dC = [-1, 0, 1, 0], [0, -1, 0, 1]
    painted = set()

    # Initialise Intcode computer
    VM = IntcodeComputer(program_file, input=get_input)

    if part1:
        # Start robot in centre of grid
        r, c = R // 2, C // 2
    else:
        # Start robot near top-left corner of grid on a white tile
        r, c = 1, 2
        G[r][c] = 1

    # Carry on receiving output from program until it halts
    while True:
        colour = VM.run()
        if colour is None:
            break
        G[r][c] = colour
        painted.add((r, c))
        turn = VM.run()
        if turn == 0:
            d = (d + 1) % 4
        else:
            d = (d + 3) % 4
        r += dR[d]
        c += dC[d]

    if mpl:
        # Matplotlib plot
        plt.figure()
        plt.imshow(G, cmap='gray')
        plt.axis('off')

    if asc:
        # Paint grid
        if part1:
            msg = str(len(painted)) + "\n"
        else:
            msg = "\n"
        for r in range(R):
            for c in range(C):
                if G[r][c] == 1:
                    msg += '#'
                else:
                    msg += " "
            msg += "\n"
        return msg

    if part1:
        return len(painted)
    return ""


# %% Output
def main():
    print("AoC 2019\nDay 09")
    program_file = 'input.txt'
    print("Part 1:", Day11(program_file, (120, 120), part1=True, asc=False, mpl=False))
    print("Part 2:", Day11(program_file, (8, 45), part1=False, asc=True, mpl=False))


if __name__ == '__main__':
    main()
