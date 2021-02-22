from helper import aoc_timer
from collections import defaultdict


# %% Intcode computer class
class IntcodeProgram:
    """Intcode virtual machine class."""

    def __init__(self, program_file, input, output=False):
        # Load Intcode program
        self.P = defaultdict(int)
        with open(program_file) as f:
            for i, x in enumerate(f.read().split(',')):
                self.P[i] = int(x)
        # Additional properties
        self.input = input
        self.output = output
        self.ip = 0
        self.halted = False

    def get_index(self, i, m):
        """Get the index for the current instruction."""
        mode = (0 if i >= len(m) else m[i])
        idx = self.ip + 1 + i
        if mode == 0:
            # Position mode
            return self.P[idx]
        elif mode == 1:
            # Immediate mode
            return idx
        else:
            # Invalid parameter mode
            assert False, mode

    def run(self):
        """Run the program."""
        while not self.halted:
            cmd = str(self.P[self.ip])
            opcode = int(cmd[-2:])
            m = list(reversed([int(x) for x in cmd[:-2]]))
            if opcode == 1:
                # Add
                i1, i2, i3 = [self.get_index(i, m) for i in range(3)]
                self.P[i3] = self.P[i1] + self.P[i2]
                self.ip += 4
            elif opcode == 2:
                # Multiply
                i1, i2, i3 = [self.get_index(i, m) for i in range(3)]
                self.P[i3] = self.P[i1] * self.P[i2]
                self.ip += 4
            elif opcode == 3:
                # Input
                i1 = self.get_index(0, m)
                self.P[i1] = self.input
                self.ip += 2
            elif opcode == 4:
                # Output
                i1 = self.get_index(0, m)
                if self.output:
                    print(self.P[i1])
                self.ip += 2
            elif opcode == 5:
                # Jump-if-true
                i1, i2 = [self.get_index(i, m) for i in range(2)]
                if self.P[i1] != 0:
                    self.ip = self.P[i2]
                else:
                    self.ip += 3
            elif opcode == 6:
                # Jump-if-false
                i1, i2 = [self.get_index(i, m) for i in range(2)]
                if self.P[i1] == 0:
                    self.ip = self.P[i2]
                else:
                    self.ip += 3
            elif opcode == 7:
                # Less than
                i1, i2, i3 = [self.get_index(i, m) for i in range(3)]
                if self.P[i1] < self.P[i2]:
                    self.P[i3] = 1
                else:
                    self.P[i3] = 0
                self.ip += 4
            elif opcode == 8:
                # Equals
                i1, i2, i3 = [self.get_index(i, m) for i in range(3)]
                if self.P[i1] == self.P[i2]:
                    self.P[i3] = 1
                else:
                    self.P[i3] = 0
                self.ip += 4
            else:
                assert opcode == 99
                # End of program
                self.halted = True
                return self.P[i1]


# %% Day 5 Solver
@aoc_timer
def Day05(path, input, output=False):
    P = IntcodeProgram(path, input, output)
    return P.run()


# %% Output
def main():
    print("AoC 2019\nDay 05")
    path = 'input.txt'
    print("Part 1:", Day05(path, 1, False))
    print("Part 2:", Day05(path, 5, False))


if __name__ == '__main__':
    main()
