from helper import aoc_timer


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        signals, display = line.split(' | ')
        yield signals.split(), display.split()


@aoc_timer
def Day08(data):
    p1 = p2 = 0
    UNIQUE = set('1478')
    for signals, display in data:
        segments = {len(s): set(s) for s in signals}
        n = ''
        for out in map(set, display):
            match len(out), len(out & segments[4]), len(out & segments[2]):
                case 2, _, _: n += (d := '1')
                case 3, _, _: n += (d := '7')
                case 4, _, _: n += (d := '4')
                case 7, _, _: n += (d := '8')
                case 5, 2, _: n += (d := '2')
                case 5, 3, 1: n += (d := '5')
                case 5, 3, 2: n += (d := '3')
                case 6, 4, _: n += (d := '9')
                case 6, 3, 1: n += (d := '6')
                case 6, 3, 2: n += (d := '0')
            if d in UNIQUE:
                p1 += 1
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
