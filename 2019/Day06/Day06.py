from helper import aoc_timer


@aoc_timer
def get_input(path):
    return dict(reversed(y) for y in list(x.strip().split(")") for x in open(path)))


@aoc_timer
def Day06(orbits, part1=True):
    count = 0
    for i in orbits:
        x = i
        while x in orbits:
            x = orbits[x]
            count += 1
    if part1:
        return count

    def transfer(orbits, origin):
        path = []
        while origin in orbits:
            origin = orbits[origin]
            path.append(origin)
        return path

    p1 = transfer(orbits, "SAN")
    p2 = transfer(orbits, "YOU")

    return len(set(p1) ^ set(p2))


# %% Output
def main():
    print("AoC 2019\nDay 06")
    data = get_input('input.txt')
    print("Part 1:", Day06(data))
    print("Part 2:", Day06(data, part1=False))


if __name__ == '__main__':
    main()
