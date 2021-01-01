from time import time
from os import getcwd


def get_input(path):
    # This is just binary, replace F,B,L,R with 0,1,0,1
    return [s.translate(s.maketrans('FBLR', '0101')) for s in open(path).readlines()]


def Day05(data):
    ID = set()
    # Part 1
    [ID.add(int(seat, 2)) for seat in data]
    # Part 2
    for x, y in zip(sorted(ID), sorted(ID)[1:]):
        if y - x == 2:
            return max(ID), x + 1


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day05.txt"
    print("AoC 2020\nDay 5\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    p1, p2 = Day05(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
800 µs ± 2.95 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day05(data)
335 µs ± 777 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
