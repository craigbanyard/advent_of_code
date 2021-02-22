from helper import aoc_timer
from collections import defaultdict, deque
from itertools import permutations


# %% Intcode computer class
class IntcodeProgram:
    """Intcode virtual machine class."""

    def __init__(self, program_id, program_file, input):
        # Load Intcode program
        self.P = defaultdict(int)
        with open(program_file) as f:
            for i, x in enumerate(f.read().split(',')):
                self.P[i] = int(x)
        # Additional properties
        self.program_id = program_id
        self.input = input
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

    # Run the Intcode program
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
                self.P[i1] = self.input()
                self.ip += 2
            elif opcode == 4:
                # Output
                i1 = self.get_index(0, m)
                out = self.P[i1]
                self.ip += 2
                return out
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
                return None


# %% Day 7 Solver
@aoc_timer
def Day07(path, phase):

    def get_input(i):
        if Q[i]:
            return Q[i].popleft()
        return 0

    max_signal = 0
    for p in permutations(list(phase)):
        amps = []
        Q = []
        first_pass = True
        signal = 0
        while signal is not None:
            for i in range(5):
                if first_pass:
                    Q.append(deque([p[i]]))
                    amps.append(IntcodeProgram(i, path, lambda: get_input(i)))
                Q[i].append(signal)
                signal = amps[i].run()
            first_pass = False
            max_signal = max(signal if signal is not None else 0, max_signal)
    return max_signal


# %% Output
def main():
    print("AoC 2019\nDay 07")
    path = 'input.txt'
    print("Part 1:", Day07(path, range(5)))
    print("Part 2:", Day07(path, range(5, 10)))


if __name__ == '__main__':
    main()
