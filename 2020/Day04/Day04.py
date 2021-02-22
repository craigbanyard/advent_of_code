from helper import aoc_timer
import re


@aoc_timer
def get_input(path):
    for line in open(path).read().split('\n\n'):
        line = line.replace('\n', ' ').split()
        yield {k: v for k, v in [crit.split(':') for crit in line]}


@aoc_timer
def Day04(path):

    # Passport validation - Part 1
    req = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    def hgt_val(x):
        cm_val = '150' <= x[:-2] <= '193' and x.endswith('cm')
        in_val = '59' <= x[:-2] <= '76' and x.endswith('in')
        return cm_val or in_val

    # Passport validation - Part 2
    reqval = {
        'byr': lambda x: '1920' <= x <= '2002',
        'iyr': lambda x: '2010' <= x <= '2020',
        'eyr': lambda x: '2020' <= x <= '2030',
        'hgt': lambda x: hgt_val(x),
        'hcl': lambda x: re.search('^#[0-9a-f]{6}$', x),
        'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda x: re.search('^[0-9]{9}$', x),
        'cid': lambda x: True
    }

    # Check passports
    p1, p2 = 0, 0
    for passport in get_input(path):
        if all(x in passport.keys() for x in req):
            p1 += 1
            if all(reqval[k](v) for k, v in passport.items()):
                p2 += 1
    return p1, p2


# %% Output
def main():
    print("AoC 2020\nDay 04")
    p1, p2 = Day04('input.txt')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 277 ns ± 0.832 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# %timeit Day04(data)
# 2.06 ms ± 6.17 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
