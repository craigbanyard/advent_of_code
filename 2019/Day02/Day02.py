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
        # Day 2 replacement
        noun, verb = input
        self.P[1] = noun
        self.P[2] = verb
        # Additional properties
        self.ip = 0
        self.halted = False

    def run(self):
        """Run the program."""
        while not self.halted:
            opcode = self.P[self.ip]
            i1, i2, i3 = self.P[self.ip + 1], self.P[self.ip + 2], self.P[self.ip + 3]
            if opcode == 1:
                # Addition
                self.P[i3] = self.P[i1] + self.P[i2]
            elif opcode == 2:
                # Multiplication
                self.P[i3] = self.P[i1] * self.P[i2]
            else:
                assert opcode == 99
                self.halted = True
                return self.P[0]
            self.ip += 4


# %% Day 2 Solver
@aoc_timer
def Day02(path, part1=True, target=None):
    if part1:
        P = IntcodeProgram(path, [12, 2])
        return P.run()

    # Part 2
    for i in range(100):
        for j in range(100):
            P = IntcodeProgram(path, [i, j])
            if P.run() == target:
                return (i * 100) + j
    return None


# %% Output
def main():
    print("AoC 2019\nDay 02")
    path = 'input.txt'
    print("Part 1:", Day02(path))
    print("Part 2:", Day02(path, part1=False, target=19690720))


if __name__ == '__main__':
    main()
