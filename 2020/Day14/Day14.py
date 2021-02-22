from helper import aoc_timer
import re
import itertools


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def parse_inst(line):
    return [int(x) for x in re.findall(r'\d+', line)]


def to_dec(b):
    ans = 0
    for i in b:
        ans = (ans << 1) | i
    return ans


def to_bin(d, bits=36):
    return [int(x) for x in format(d, '0' + str(bits) + 'b')]


@aoc_timer
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


@aoc_timer
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
    print("AoC 2020\nDay 14")
    data = get_input('input.txt')
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 246 µs ± 2.72 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit part1(data)
# 9.07 ms ± 159 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

# %timeit part2(data)
# 365 ms ± 11.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
