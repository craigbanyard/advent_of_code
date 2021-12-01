from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [*map(int, open(path))]


@aoc_timer
def Day01(data, offset):
    return sum([x < y for x, y in zip(data, data[offset:])])


# %% Output
def main():
    print("AoC 2021\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", Day01(data, offset=1))
    print("Part 2:", Day01(data, offset=3))


if __name__ == '__main__':
    main()
