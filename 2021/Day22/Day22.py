from helper import aoc_timer
from collections import defaultdict
import re


class Cuboid:

    def __init__(self, state, coords) -> None:
        self.state = state
        self.coords = coords
        self.small = all(-50 <= c <= 50 for c in coords)

    def __repr__(self):
        x1, x2, y1, y2, z1, z2 = self.coords
        return f'{self.state}: x={x1}..{x2},y={y1}..{y2},z={z1}..{z2}'

    def volume(self) -> int:
        x1, x2, y1, y2, z1, z2 = self.coords
        return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1) * self.state

    def intersect(self, other: type['Cuboid']) -> type['Cuboid'] | None:
        x1, x2, y1, y2, z1, z2 = self.coords
        p1, p2, q1, q2, r1, r2 = other.coords
        x1 = x1 if x1 >= p1 else p1
        x2 = x2 if x2 <= p2 else p2
        y1 = y1 if y1 >= q1 else q1
        y2 = y2 if y2 <= q2 else q2
        z1 = z1 if z1 >= r1 else r1
        z2 = z2 if z2 <= r2 else r2
        if x1 <= x2 and y1 <= y2 and z1 <= z2:
            return Cuboid(-other.state, (x1, x2, y1, y2, z1, z2))
        return False


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        op, *coords = re.findall(r'on|off|-?\d+', line)
        yield op == 'on', tuple(map(int, coords))


@aoc_timer
def Day22(data):
    cuboids: dict[Cuboid, list[Cuboid]] = defaultdict(list)
    for op, coords in data:
        new = Cuboid(op, coords)
        for prev in cuboids:
            new_intersections: list[Cuboid] = []
            if (i := new.intersect(prev)):
                new_intersections.append(i)
                for inner in cuboids[prev]:
                    if (i := new.intersect(inner)):
                        new_intersections.append(i)
            cuboids[prev] += new_intersections
        cuboids[new] = []
    p1 = p2 = 0
    for parent, children in cuboids.items():
        on = parent.volume() + sum(c.volume() for c in children)
        if parent.small:
            p1 += on
        p2 += on
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 22")
    data = get_input('input.txt')
    p1, p2 = Day22(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
