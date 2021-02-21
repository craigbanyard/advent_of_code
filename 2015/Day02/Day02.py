from helper import aoc_timer
import math


@aoc_timer
def get_input(path):
    return [
        list(map(int, x.strip().split('x')))
        for x in open(path).readlines()
    ]


def wrapping(present):
    a, b, c = present
    faces = [
        a * b,
        b * c,
        a * c
    ]
    return 2 * sum(faces) + min(faces)


def ribbon(present):
    a, b, c = present
    perims = [
        a + b,
        b + c,
        a + c
    ]
    return 2 * min(perims) + math.prod(present)


@aoc_timer
def Day02(data, part2=False):
    if part2:
        return sum(map(ribbon, data))
    return sum(map(wrapping, data))


# %% Output
def main():
    print("AoC 2015\nDay 02")
    data = get_input('input.txt')
    print("Part 1:", Day02(data))
    print("Part 2:", Day02(data, part2=True))


if __name__ == '__main__':
    main()


# %% Class-based

class Present:
    def __init__(self, dims):
        self.dims = dims
        self.length = dims[0]
        self.width = dims[1]
        self.height = dims[2]

    def face_areas(self):
        return [
            self.length * self.width,
            self.width * self.height,
            self.height * self.length
        ]

    def face_perimeters(self):
        return [
            2 * (self.length + self.width),
            2 * (self.width + self.height),
            2 * (self.height + self.length)
        ]

    def surface_area(self):
        return 2 * sum(self.face_areas())

    def volume(self):
        return self.length * self.width * self.height

    def wrapping(self):
        return self.surface_area() + min(self.face_areas())

    def ribbon(self):
        return min(self.face_perimeters()) + self.volume()


@aoc_timer
def Day02_Class(data):
    p1, p2 = 0, 0
    for dims in data:
        p = Present(dims)
        p1 += p.wrapping()
        p2 += p.ribbon()
    return p1, p2
