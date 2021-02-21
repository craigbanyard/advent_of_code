from helper import aoc_timer
from hashlib import md5


def check_hash(s, N):
    return md5(s.encode()).hexdigest()[0:N] == '0' * N


@aoc_timer
def Day04(key, N):
    n = 1
    while True:
        s = key + str(n)
        if check_hash(s, N):
            break
        n += 1
    return n


# %% Output
def main():
    print("AoC 2015\nDay 04")
    key = 'bgvyzdsv'
    print("Part 1:", Day04(key, 5))
    print("Part 2:", Day04(key, 6))


if __name__ == '__main__':
    main()
