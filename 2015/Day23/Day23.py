from helper import aoc_timer


class Program:

    # Initialise computer
    def __init__(self, program_file, a):
        # Properties
        self.program_file = program_file
        self.P = self.load()
        self.ip = 0
        self.regs = {'a': a, 'b': 0}
        self.len = len(self.P)

    # Load the boot code
    def load(self):
        self.P = {}
        with open(self.program_file) as f:
            for i, x in enumerate(f.readlines()):
                line = x.replace(',', '').split()
                if len(line) == 3:
                    op, r, off = line
                    self.P[i] = (op, r, int(off))
                elif line[0] == 'jmp':
                    op, off = line
                    self.P[i] = (op, int(off))
                else:
                    op, r = line
                    self.P[i] = (op, r)
        return self.P

    # Run the program
    def run(self):
        while self.ip < self.len:
            op, *rest = self.P[self.ip]
            if op == 'hlf':
                self.regs[rest.pop()] //= 2
                self.ip += 1
            elif op == 'tpl':
                self.regs[rest.pop()] *= 3
                self.ip += 1
            elif op == 'inc':
                self.regs[rest.pop()] += 1
                self.ip += 1
            if op == 'jmp':
                self.ip += rest.pop()
            elif op == 'jie':
                r, off = rest
                if self.regs[r] % 2 == 0:
                    self.ip += off
                else:
                    self.ip += 1
            elif op == 'jio':
                r, off = rest
                if self.regs[r] == 1:
                    self.ip += off
                else:
                    self.ip += 1
        return self.regs


@aoc_timer
def Day23(path, a=0):
    P = Program(path, a)
    return P.run()


# %% Output
def main():
    print("AoC 2015\nDay 23")
    print("Part 1:", Day23('input.txt')['b'])
    print("Part 2:", Day23('input.txt', a=1)['b'])


if __name__ == '__main__':
    main()
