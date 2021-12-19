from helper import aoc_timer
import itertools as it
import re


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f'({self.x},{self.y})'

    def __iter__(self):
        return iter((self.x, self.y))

    def drag(self):
        if self.x > 0:
            self.x -= 1
        elif self.x < 0:
            self.x += 1
        return self

    def gravity(self):
        self.y -= 1
        return self

    def inside(self, target):
        lo, hi = target
        return lo.x <= self.x <= hi.x and lo.y <= self.y <= hi.y

    def past(self, target):
        lo, hi = target
        return self.y < lo.y or self.x > hi.x

    def traj(self, vel):
        self += vel
        vel.drag()
        vel.gravity()
        return self


@aoc_timer
def get_input(path):
    return map(int, re.findall(r'-?\d+', open(path).read()))


def tri(n):
    '''Return the nth triangle number.'''
    return n * (n + 1) // 2


def inv_tri(n):
    '''Return the inverse triangular number of n.'''
    return int((2 * n) ** 0.5)


@aoc_timer
def Day17(data):
    p1 = p2 = 0
    x1, x2, y1, y2 = data
    target = (Point(x1, y1), Point(x2, y2))
    for x, y in it.product(range(inv_tri(x1), x2 + 1), range(y1, -y1)):
        pos = Point(0, 0)
        vel = Point(x, y)
        while not pos.past(target):
            if pos.inside(target):
                p2 += 1
                break
            pos.traj(vel)
            if pos.y > p1:
                p1 = pos.y
    assert p1 == tri(y1)
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 17")
    data = get_input('input.txt')
    p1, p2 = Day17(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
