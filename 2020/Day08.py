# %% Computer class

from time import time
from os import getcwd
from collections import defaultdict


class Program:

    # Initialise computer
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

    # Load the boot program
    def load(self):
        self.P = defaultdict(tuple)
        with open(self.program_file) as f:
            for i, x in enumerate(f.readlines()):
                op, n = x.split()
                self.P[i] = (op, int(n))
        return self.P

    # Run the program
    def run(self):
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

# Split out the load and parse for timing, as with prior days
def data_load(path):
    P = Program(path)
    return P.load()


def part1(path, B):
    P = Program(path, B)
    return P.run()


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


def main():
    path = getcwd() + "\\Inputs\\Day08.txt"
    print("AoC 2020\nDay 8\n-----")
    t0 = time()
    B = data_load(path)
    print("Data:", time() - t0, '\n-----')
    t0 = time()
    p1, _, S = part1(path, B)
    print('Part 1:',  p1)
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    p2 = part2(path, B, S)
    print('Part 2:', p2)
    print("Time:", time() - t0, '\n-----')


if __name__ == '__main__':
    main()


'''
%timeit data_load(path)
1.12 ms ± 6.46 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit part1(path, B)
164 µs ± 1.06 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit part2(path, B, S)
8.42 ms ± 29.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
'''


# %% Initial attempt


def get_input(path):
    return [x.strip().split() for x in open(path).readlines()]


def p2(path):

    # Load for like-for-like timings
    data = get_input(path)

    # RIP - brute force replace one at a time and add to list of new programs
    def hack(data):
        REP = []
        new = data.copy()
        for ip, (op, n) in enumerate(data):
            if op == 'jmp':
                new[ip] = ['nop', n]
                REP.append(new)
                new = data.copy()
                continue
            if op == 'nop':
                new[ip]  = ['jmp', n]
                REP.append(new)
                new = data.copy()
                continue
        return REP

    # Return accumulator (acc), next instruction pointer (ip) and current ip
    R = {'acc': lambda x, acc, ip: (acc + x, ip + 1),
         'jmp': lambda x, acc, ip: (acc, ip + x),
         'nop': lambda x, acc, ip: (acc, ip + 1)
         }

    ins = len(data)
    newdata = hack(data)
    aborted, finished = False, False

    while not finished:
        for data in newdata:
            ip = 0
            acc = 0
            SEEN = set()
            aborted = False
            while not (aborted or finished):
                SEEN.add(ip)
                op, n = data[ip]
                acc, ip = R[op](int(n), acc, ip)
                if ip in SEEN:
                    # print('Aborted:', acc)
                    aborted = True
                if ip >= ins:
                    return acc
                    finished = True
