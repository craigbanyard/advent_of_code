from helper import aoc_timer
from collections import defaultdict
import matplotlib.pyplot as plt


# %% Intcode computer class
class IntcodeProgram:
    """Intcode virtual machine class."""

    def __init__(self, program_file, input):
        # Load Intcode program
        self.P = defaultdict(int)
        with open(program_file) as f:
            for i, x in enumerate(f.read().split(',')):
                self.P[i] = int(x)
        # Additional properties
        self.input = input
        self.ip = 0
        self.rel_base = 0
        self.halted = False

    def read(self, i, m):
        """Get value from the current read instruction."""
        mode = (0 if i >= len(m) else m[i])
        idx = self.P[self.ip + 1 + i]
        if mode == 0:
            # Position mode
            return self.P[idx]
        elif mode == 1:
            # Immediate mode
            return idx
        elif mode == 2:
            # Relative mode
            return self.P[idx + self.rel_base]
        else:
            # Invalid parameter mode
            assert False, mode

    def write(self, i, m):
        """Get index for the current write instruction."""
        mode = (0 if i >= len(m) else m[i])
        idx = self.P[self.ip + 1 + i]
        if mode == 0:
            # Position mode
            return idx
        elif mode == 2:
            # Relative mode
            return idx + self.rel_base
        else:
            # Invalid parameter mode (write cannot be in immediate)
            assert False, mode

    # Run the Intcode program
    def run(self):
        while not self.halted:
            cmd = str(self.P[self.ip])
            opcode = int(cmd[-2:])
            m = list(reversed([int(x) for x in cmd[:-2]]))
            if opcode == 1:
                # Add
                self.P[self.write(2, m)] = self.read(0, m) + self.read(1, m)
                self.ip += 4
            elif opcode == 2:
                # Multiply
                self.P[self.write(2, m)] = self.read(0, m) * self.read(1, m)
                self.ip += 4
            elif opcode == 3:
                # Input
                self.P[self.write(0, m)] = self.input()
                self.ip += 2
            elif opcode == 4:
                # Output
                out = self.read(0, m)
                self.ip += 2
                return out
            elif opcode == 5:
                # Jump-if-true
                self.ip = self.read(1, m) if self.read(0, m) != 0 else self.ip + 3
            elif opcode == 6:
                # Jump-if-false
                self.ip = self.read(1, m) if self.read(0, m) == 0 else self.ip + 3
            elif opcode == 7:
                # Less than
                self.P[self.write(2, m)] = 1 if self.read(0, m) < self.read(1, m) else 0
                self.ip += 4
            elif opcode == 8:
                # Equals
                self.P[self.write(2, m)] = 1 if self.read(0, m) == self.read(1, m) else 0
                self.ip += 4
            elif opcode == 9:
                # Adjust relative base
                self.rel_base += self.read(0, m)
                self.ip += 2
            else:
                assert opcode == 99
                # End of program
                self.halted = True


# %% Day 11 Solver
@aoc_timer
def Day11(path, grid_init, part1=True, asc=False, mpl=False):

    # Function to get current tile colour
    def get_input():
        return G[r][c]

    # Set up grid
    R, C = grid_init
    G = [[0 for _ in range(C)] for _ in range(R)]
    d = 0
    dR, dC = [-1, 0, 1, 0], [0, -1, 0, 1]
    painted = set()

    # Initialise Intcode program
    P = IntcodeProgram(path, get_input)

    if part1:
        # Start robot in centre of grid
        r, c = R // 2, C // 2
    else:
        # Start robot near top-left corner of grid on a white tile
        r, c = 1, 2
        G[r][c] = 1

    # Carry on receiving output from program until it halts
    while True:
        colour = P.run()
        if colour is None:
            break
        G[r][c] = colour
        painted.add((r, c))
        turn = P.run()
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
    path = 'input.txt'
    print("Part 1:", Day11(path, (120, 120), part1=True, asc=False, mpl=False))
    print("Part 2:", Day11(path, (8, 45), part1=False, asc=True, mpl=False))


if __name__ == '__main__':
    main()
