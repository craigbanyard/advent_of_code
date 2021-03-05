from collections import defaultdict


class IntcodeComputer:
    """Intcode virtual machine class."""

    def __init__(self, program_file, input=None, program_id=None, timeout=None):
        # Load Intcode program
        self.P = defaultdict(int)
        with open(program_file) as f:
            for i, x in enumerate(f.read().split(',')):
                self.P[i] = int(x)
        # Additional properties
        self._P = self.P.copy()
        self.input = input
        self.ip = 0
        self.rel_base = 0
        self.program_id = program_id
        self.timeout = None
        self.halted = False

    def override(self, overrides):
        """Override one or many indices of the Intcode program according to dict."""
        for idx, val in overrides.items():
            self.P[idx] = val
    
    def reset(self):
        """Reset the Intcode VM to initial state."""
        self.P = self._P.copy()
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

    def run(self):
        """Run the program."""
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
                if callable(self.input):
                    self.P[self.write(0, m)] = self.input()
                else:
                    self.P[self.write(0, m)] = self.input
                self.ip += 2
            elif opcode == 4:
                # Output
                out = self.read(0, m)
                self.ip += 2
                return out
            elif opcode == 5:
                # Jump-if-true
                self.ip = self.read(1, m) if self.read(0, m) else self.ip + 3
            elif opcode == 6:
                # Jump-if-false
                self.ip = self.read(1, m) if not self.read(0, m) else self.ip + 3
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
