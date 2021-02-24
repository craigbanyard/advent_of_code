from helper import aoc_timer
from collections import defaultdict


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
                self.P[self.write(0, m)] = self.input
                self.ip += 2
            elif opcode == 4:
                # Output
                yield self.read(0, m)
                self.ip += 2
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


# %% Day 9 Solver
@aoc_timer
def Day09(path, input):
    P = IntcodeProgram(path, input)
    return next(P.run())


# %% Output
def main():
    print("AoC 2019\nDay 09")
    path = 'input.txt'
    print("Part 1:", Day09(path, 1))
    print("Part 2:", Day09(path, 2))


if __name__ == '__main__':
    main()
