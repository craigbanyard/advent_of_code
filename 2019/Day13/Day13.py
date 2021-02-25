from helper import aoc_timer
from intcode import IntcodeComputer
from matplotlib import pyplot as plt
import numpy as np


@aoc_timer
def Day13(program_file, grid_init, part2=False, plot=False):

    def get_joystick():
        """Simple AI tracking the ball position with the paddle."""
        return np.sign(ball - paddle)

    # Set up grid (determined from wall positions)
    R, C = grid_init
    G = [[0 for _ in range(C)] for _ in range(R)]

    # Initialise Intcode program
    if part2:
        VM = IntcodeComputer(program_file, input=get_joystick)
        VM.override({0: 2})
        # Buffer for score display at the top of screen
        row_buffer = 2
    else:
        VM = IntcodeComputer(program_file)
        row_buffer = 0

    # Carry on receiving output from program until it halts
    while True:
        c, r, tile = [VM.run() for _ in range(3)]
        if c == -1:
            score = tile
        if VM.halted:
            break
        elif tile == 3:
            paddle = c    # Save paddle x-position
        elif tile == 4:
            ball = c      # Save ball x-position
        G[r + row_buffer][c] = tile

    # Matplotlib plot
    if plot:
        plt.figure()
        plt.imshow(G, cmap='gist_stern')
        plt.axis('off')
        if part2:
            plt.text(
                42.2, 0.6, "Score: " + str(score), fontsize=9, family='Consolas',
                color='white', horizontalalignment='right'
            )

    if part2:
        return score
    return sum(x.count(2) for x in G)


# %% Output
def main():
    print("AoC 2019\nDay 13")
    program_file = 'input.txt'
    print("Part 1:", Day13(program_file, (23, 43), part2=False, plot=True))
    print("Part 2:", Day13(program_file, (25, 43), part2=True, plot=False))


if __name__ == '__main__':
    main()
