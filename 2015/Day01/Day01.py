from helper import aoc_timer


@aoc_timer
def get_input(path):
    return open(path).read()


@aoc_timer
def Day01(data, part1=True):
    if part1:
        return data.count('(') - data.count(')')
    floor = 0
    for idx, i in enumerate(data, start=1):
        if i == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return idx


# %% Output
def main():
    print("AoC 2015\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", Day01(data))
    print("Part 2:", Day01(data, part1=False))


if __name__ == '__main__':
    main()
