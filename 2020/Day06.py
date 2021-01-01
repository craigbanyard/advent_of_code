from time import time
from os import getcwd


def get_input(path):
    return [x.replace('\n', ' ').split() for x in open(path).read().split('\n\n')]


def Day06(data):
    p1, p2 = 0, 0
    for group in data:
        yes = []
        for person in group:
            yes.append(set(person))
        p1 += len(set.union(*yes))
        p2 += len(set.intersection(*yes))
    return p1, p2


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day06.txt"
    print("AoC 2020\nDay 6\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    p1, p2 = Day06(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
519 µs ± 1.02 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day06(data)
2.25 ms ± 4.98 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
'''
