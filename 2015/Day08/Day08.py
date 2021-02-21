from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


@aoc_timer
def Day08(data):
    p1 = sum(len(s) - len(eval(s)) for s in data)
    p2 = sum(2 + s.count('\\') + s.count('"') for s in data)
    return p1, p2


# %% Output
def main():
    print("AoC 2015\nDay 08")
    data = get_input('input.txt')
    p1, p2 = Day08(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
