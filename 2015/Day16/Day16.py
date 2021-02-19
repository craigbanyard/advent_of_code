from helper import aoc_timer


@aoc_timer
def get_input(path):
    return {
        int(k.lstrip('Sue ')): {
            kk: int(vv) for kk, vv in
            (pair.split(': ') for pair in v.split(', '))
        }
        for k, v in (x.strip().split(': ', 1) for x in open(path).readlines())
    }


@aoc_timer
def Day16(data, part2=False):

    # MFCSAM results
    M = {'children': 3,
         'cats': 7,
         'samoyeds': 2,
         'pomeranians': 3,
         'akitas': 0,
         'vizslas': 0,
         'goldfish': 5,
         'trees': 3,
         'cars': 2,
         'perfumes': 1,
         }

    P = {k: lambda x, y: x == y for k in M}

    # Modify dictionary for part 2 conditions
    if part2:
        for k in M:
            if k in ['cats', 'trees']:
                P[k] = lambda x, y: x > y
            elif k in ['pomeranians', 'goldfish']:
                P[k] = lambda x, y: x < y

    for sue, comps in data.items():
        matches = 0
        for k, v in M.items():
            if k in comps:
                if P[k](comps[k], v):
                    matches += 1
            if matches == 3:
                return sue


# %% Output
def main():
    print("AoC 2015\nDay 16")
    data = get_input('input.txt')
    print("Part 1:", Day16(data))
    print("Part 2:", Day16(data, part2=True))


if __name__ == '__main__':
    main()
