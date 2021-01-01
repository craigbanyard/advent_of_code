from time import time
import re
import itertools
from os import getcwd


def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def parse_inst(line):
    return [int(x) for x in re.findall('\d+', line)]


def to_dec(b):
    ans = 0
    for i in b:
        ans = (ans << 1) | i
    return ans


def to_bin(d, bits=36):
    return [int(x) for x in format(d, '0' + str(bits) + 'b')]


def part1(data):
    mem = {}
    for line in data:
        # Process mask
        if line[:4] == 'mask':
            mask = line[7:]
            continue
        # Get memory address and value to write
        add, val = parse_inst(line)
        # Convert value to 36 bit binary
        val = to_bin(val, bits=36)
        # Apply mask to value
        for idx, d in enumerate(mask):
            if d == 'X':
                continue
            val[idx] = int(d)
        # Write decimal value to memory
        mem[add] = to_dec(val)
    return sum(mem.values())


# Idea: for n X's in mask, and value y, sum = y * 2**N - need to account for overlaps
def part2(data):
    mem = {}
    for line in data:
        # Process mask
        if line[:4] == 'mask':
            mask = line[7:]
            continue
        # Get memory address and value to write
        add, val = parse_inst(line)
        # Convert address to 36 bit binary
        add = to_bin(add, bits=36)
        # Apply mask to address
        for idx, d in enumerate(mask):
            if d == 'X':
                # Floating bit
                add[idx] = d
                continue
            add[idx] = add[idx] | int(d)
        # Process floating bits
        n = add.count('X')
        xs = [idx for idx, val in enumerate(add) if val == 'X']
        adds = []
        for x in itertools.product([0, 1], repeat=n):
            for idx, bit in zip(xs, x):
                add[idx] = bit
            adds.append(to_dec(add))
        # Write value to relevant addresses
        for add in adds:
            mem[add] = val
    return sum(mem.values())


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day14.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day14.txt"
    print("AoC 2020\nDay 14\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    print("Part 1:", part1(data))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", part2(data))
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()
