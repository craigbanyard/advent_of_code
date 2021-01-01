from time import time
import re
from os import getcwd


def get_input(path):
    return [x.replace('\n', ' ').split() for x in open(path).read().split('\n\n')]


def Day04(data):

    # Passport validation - Part 1
    req = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    # Passport validation - Part 2
    reqval = {'byr': lambda x: '1920' <= x <= '2002',
              'iyr': lambda x: '2010' <= x <= '2020',
              'eyr': lambda x: '2020' <= x <= '2030',
              'hgt': lambda x: ('150' <= x[:-2] <= '193' and x.endswith('cm')) or
                               ('59' <= x[:-2] <= '76' and x.endswith('in')),
              'hcl': lambda x: re.search('^#[0-9a-f]{6}$', x),
              'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
              'pid': lambda x: re.search('^[0-9]{9}$', x),
              'cid': lambda x: True
              }

    # Check passports
    p1, p2 = 0, 0
    for passport in data:
        passport = {k: v for k, v in [crit.split(':') for crit in passport]}
        if all(x in passport.keys() for x in req):
            p1 += 1
            if all(reqval[k](v) for k, v in passport.items()):
                p2 += 1
    return p1, p2


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day04.txt"
    print("AoC 2020\nDay 4\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0)
    t0 = time()
    p1, p2 = Day04(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
433 µs ± 2.88 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day04(data)
2.06 ms ± 6.17 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
'''


# %% Original code


def get_input_orig(path):
    return [x.strip() for x in open(path).readlines()]


def Day04_orig(data):

    # Number of passports for input parsing (+1 for first passport, i.e. before a blank newline)
    ppts = sum(1 for l in data if l == '') + 1

    # Parse input - jeez this is bad
    P=[{} for _ in range(ppts)]
    counter = 0
    for line in data:
        if line == '':
            counter += 1
            continue
        for pair in line.split(' '):
            k,v = pair.split(':')
            P[counter][k] = v

    # Passport validation
    req = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    reqval = {'byr': lambda x: '1920' <= x <= '2002',
              'iyr': lambda x: '2010' <= x <= '2020',
              'eyr': lambda x: '2020' <= x <= '2030',
              'hgt': lambda x: ('150' <= x[:-2] <= '193' and x[-2:] == 'cm') or
                               ('59' <= x[:-2] <= '76' and x[-2:] == 'in'),
              'hcl': lambda x: re.search('^#[0-9a-f]{6}$', x),
              'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
              'pid': lambda x: re.search('^[0-9]{9}$', x),
              'cid': lambda x: True
              }

    # Check passports
    p1, p2 = 0, 0
    for passport in P:
        if all(x in passport.keys() for x in req):
            p1 += 1
            if all(reqval[k](v) for k, v in passport.items()):
                p2 += 1
    
    return p1, p2

# # Output
# path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2020\\Inputs\\Day04.txt"
# print("AoC 2020\nDay 4\n-----")
# t0=time()
# data = get_input_orig(path)
# print("Data:",time()-t0)
# t0=time()
# p1,p2 = Day04_orig(data)
# print("Part 1:",p1)
# print("Part 2:",p2)
# print("Time:",time()-t0)

# del t0, path, data, p1, p2
