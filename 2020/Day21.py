from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return {tuple(k.split()): set(v.split(', ')) for k, v in
            [x .replace(')', '').strip().split(' (contains ')
             for x in open(path).readlines()]}


def filt_dict(d, search, domain='keys', result='keys'):
    res = []
    for k, v in d.items():
        lookup = {'keys': k, 'values': v}
        if search in lookup[domain]:
            res.append(lookup[result])
    return res


@aoc_timer
def Day21(data, part1=True, p1_data=None):

    if part1:
        # Unique allergens and ingredients
        allergens = set.union(*data.values())
        ingredients = set().union(*data)

        # Get ingredients that cannot be allergens (NOT)
        # Get possible allergens for ingredients that do contain an allergen (POSS)
        NOT = {k: set() for k in ingredients}
        POSS = {k: allergens for k in ingredients}
        for i in ingredients:
            for a in allergens:
                if any(i not in x for x in filt_dict(data, a, 'values', 'keys')):
                    NOT[i].add(a)
            if NOT[i] == allergens:
                del POSS[i]
                continue
            POSS[i] = POSS[i] - NOT[i]

        # Count number of instances of non-allergen ingredients in food list
        no_allerg = {i for i in NOT if NOT[i] == allergens}
        cnt = 0
        for ing in no_allerg:
            cnt += len(filt_dict(data, ing, 'keys', 'keys'))
        return cnt, (len(allergens), POSS)

    # Part 2 - construct canonical dangerous ingredient list
    allergens, POSS = p1_data
    ALGN = {}
    while len(ALGN) < allergens:
        for k in sorted(POSS, key=lambda k: len(POSS[k])):
            v = POSS[k] - set(ALGN.keys())
            if len(v) == 1:
                ALGN[v.pop()] = k
    return ','.join(ALGN[k] for k in sorted(ALGN))


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day21.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day21.txt"
    print("AoC 2020\nDay 21")
    data = get_input(path)
    p1, p1_data = Day21(data, True)
    print("Part 1:", p1)
    print("Part 2:", Day21(data, False, p1_data))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
494 µs ± 905 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day21(data, True)
24.4 ms ± 16.7 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit Day21(data, False, p1_data)
16.4 µs ± 19.8 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
'''
