from helper import aoc_timer


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        x, y = line.split()
        yield x[0], int(y)


def mag(z: complex) -> int:
    return int(z.real * z.imag)


@aoc_timer
def Day02(data):
    D = {
        'f': 1,
        'd': 1j,
        'u': -1j
    }
    p1, p2 = 0, 0
    aim = 0
    for d, n in data:
        p1 += D[d] * n
        aim = p1.imag * 1j
        if d == 'f':
            p2 += n * (1 + aim)
    return map(mag, (p1, p2))


# %% Output
def main():
    print("AoC 2021\nDay 02")
    data = get_input('input.txt')
    p1, p2 = Day02(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
