from helper import aoc_timer
from itertools import groupby


def inc_pwd(pwd):
    if pwd == 'z':
        return 'aa'
    if pwd[-1] == 'z':
        return inc_pwd(pwd[:-1]) + 'a'
    return pwd[:-1] + chr(ord(pwd[-1]) + 1)


def eight_lower(pwd):
    return len(pwd) == 8 and pwd.islower()


def make_eight_lower(pwd):
    if eight_lower(pwd):
        return pwd
    return pwd.lower() + (8 - len(pwd)) * 'a'


def no_illegal(pwd):
    return sum(map(pwd.count, 'iol')) == 0


def make_legal(pwd):
    if no_illegal(pwd):
        return pwd
    return ''.join(chr(ord(x) + 1) if x in 'iol' else x for x in pwd)


def straight(pwd):
    return sum(ord(z) == ord(y) + 1 == ord(x) + 2
               for x, y, z in zip(pwd, pwd[1:], pwd[2:])) > 0


def two_pair(pwd):
    groups = [len([1 for _ in g]) for k, g in groupby(pwd)]
    return sum(1 for i in groups if i > 1) > 1


# Replace illegal characters, don't check eight lower (never bites in this problem)
@aoc_timer
def Day11(pwd):
    while True:
        pwd = make_legal(inc_pwd(pwd))
        if straight(pwd):
            if two_pair(pwd):
                return pwd


# %% Output
def main():
    print("AoC 2015\nDay 11")
    pwd = 'vzbxkghb'
    pwd = Day11(pwd)
    print("Part 1:", pwd)
    print("Part 2:", Day11(pwd))


if __name__ == '__main__':
    main()
