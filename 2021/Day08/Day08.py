from helper import aoc_timer


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        signals, display = line.split(' | ')
        yield signals.split(), display.split()


@aoc_timer
def Day08(data):
    p1 = p2 = 0
    for signals, display in data:
        segments = {len(s): set(s) for s in signals}
        n = ''
        for out in map(set, display):
            match len(out), len(out & segments[4]), len(out & segments[2]):
                case 2, _, _: n += '1'; p1 += 1
                case 3, _, _: n += '7'; p1 += 1
                case 4, _, _: n += '4'; p1 += 1
                case 7, _, _: n += '8'; p1 += 1
                case 5, 2, _: n += '2'
                case 5, 3, 1: n += '5'
                case 5, 3, 2: n += '3'
                case 6, 4, _: n += '9'
                case 6, 3, 1: n += '6'
                case 6, 3, 2: n += '0'
        p2 += int(n)
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 08")
    data = get_input('input.txt')
    p1, p2 = Day08(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
