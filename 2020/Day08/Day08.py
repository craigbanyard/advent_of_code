from helper import aoc_timer
from collections import defaultdict


class Program:
    """Game console class"""

    def __init__(self, program_file, override=False):
        # Properties
        if override:
            self.P = override
        else:
            self.program_file = program_file
            self.P = self.load()
        self.ip = 0
        self.acc = 0
        self.len = len(self.P)
        self.seen = set([self.ip])
        self.halted = False

    def load(self):
        """Load the boot code"""
        self.P = defaultdict(tuple)
        with open(self.program_file) as f:
            for i, x in enumerate(f.readlines()):
                op, n = x.split()
                self.P[i] = (op, int(n))
        return self.P

    def run(self):
        """Run the program"""
        while not self.halted and self.ip < self.len:
            op, n = self.P[self.ip]
            if op == 'acc':
                self.acc += n
                self.ip += 1
            elif op == 'jmp':
                self.ip += n
            elif op == 'nop':
                self.ip += 1
            if self.ip in self.seen:
                self.halted = True
                return self.acc, self.halted, self.seen
            self.seen.add(self.ip)
        return self.acc, self.halted, self.seen


# %% Day 8
@aoc_timer
def get_input(path):
    P = Program(path)
    return P.load()


@aoc_timer
def part1(path, B):
    P = Program(path, B)
    return P.run()


@aoc_timer
def part2(path, B, S):
    P = Program(path)
    filtered = {k for k, v in B.items() if k in S and v[0] in 'jmpnop'}
    for idx in filtered:
        op, n = B[idx]
        Bmod = B.copy()
        if op == 'jmp':
            Bmod[idx] = ('nop', n)
        else:
            Bmod[idx] = ('jmp', n)
        P = Program(path, Bmod)
        acc, err, _ = P.run()
        if not err:
            return acc


# %% Output
def main():
    print("AoC 2020\nDay 08")
    path = 'input.txt'
    B = get_input(path)
    p1, _, S = part1(path, B)
    print('Part 1:', p1)
    p2 = part2(path, B, S)
    print('Part 2:', p2)


if __name__ == '__main__':
    main()


# %timeit get_input(path)
# 958 µs ± 2.01 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit part1(path, B)
# 160 µs ± 617 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

# %timeit part2(path, B, S)
# 8.03 ms ± 15.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
