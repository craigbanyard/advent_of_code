from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]


@aoc_timer
def Day01(data, part1=True):
    if part1:
        return sum(map(lambda m: (m // 3) - 2, data))
    part2 = 0
    for m in data:
        while m > 0:
            m = max((m // 3) - 2, 0)
            part2 += m
    return part2


# %% Output
def main():
    print("AoC 2019\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", Day01(data))
    print("Part 2:", Day01(data, part1=False))


if __name__ == '__main__':
    main()
