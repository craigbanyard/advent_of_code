from helper import aoc_timer
from collections import defaultdict
import math


@aoc_timer
def get_input(path):

    def parse_amt_chem(s):
        amt, chem = s.split()
        return int(amt), chem

    reactions = {}
    for line in open(path).read().split('\n'):
        inputs, ouput = line.split(' => ')
        n_ouput, ouput = parse_amt_chem(ouput)
        inputs = inputs.split(', ')
        inputs = [parse_amt_chem(s.strip()) for s in inputs]
        reactions[ouput] = (n_ouput, inputs)
    return reactions


def ore_cost(reactions, target, target_amount, surplus=None):
    if surplus is None:
        surplus = defaultdict(int)
    if target == 'ORE':
        return target_amount
    elif target_amount <= surplus[target]:
        surplus[target] -= target_amount
        return 0
    target_amount -= surplus[target]
    surplus[target] = 0
    ore = 0
    n_output, inputs = reactions[target]
    quantity = math.ceil(target_amount / n_output)
    for n_input, input in inputs:
        n_input *= quantity
        ore += ore_cost(reactions, input, n_input, surplus)
    surplus[target] += n_output * quantity - target_amount
    return ore


@aoc_timer
def Day14(data, req='FUEL', part1=True, fuel_cost=None):

    if part1:
        return ore_cost(data, req, 1)

    # Part 2 - binary search
    ore = int(1e12)
    lo, hi = 0, ore
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if (ore_cost(data, req, mid)) > ore:
            hi = mid - 1
        else:
            lo = mid
    return lo


# %% Output
def main():
    print("AoC 2019\nDay 14")
    data = get_input('input.txt')
    p1 = Day14(data)
    print("Part 1:", p1)
    print("Part 2:", Day14(data, part1=False, fuel_cost=p1))


if __name__ == '__main__':
    main()
