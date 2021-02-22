from helper import aoc_timer
import itertools
from collections import deque


@aoc_timer
def get_input(path):

    def parse(rule):
        if rule.count('"') > 0:
            return rule.replace('"', '')
        return [tuple(map(int, x.split())) for x in rule.split(' | ')]

    rules, messages = [y.split('\n') for y in [x for x in open(path).read().split('\n\n')]]
    rules = {int(k): parse(v) for k, v in [line.split(': ') for line in rules]}
    return rules, messages


def cmb(rule):
    ans = []
    for x in itertools.product(*rule):
        ans.append(''.join(x))
    return ans


def reduce(rule, rules):
    if isinstance(rule, list):
        tmp = []
        for subrule in rule:
            tmp.append(reduce(subrule, rules))
        # Lists are "OR" so can join into one list
        if all(isinstance(x, list) for x in tmp):
            return list(itertools.chain.from_iterable(tmp))
        return tmp
    if isinstance(rule, tuple):
        tmp = []
        for idx in rule:
            tmp.append(reduce(rules[idx], rules))
        # All strings => join
        if all(isinstance(x, str) for x in tmp):
            out = ''
            for r in tmp:
                out += r
            return out
        # All lists => join product
        if all(isinstance(x, list) for x in tmp):
            return cmb(tmp)
        return tuple(tmp)
    if rule in rules:
        return rules[rule]
    return cmb(rule)


def chunk(msg, n):
    while len(msg) >= n:
        yield msg[:n]
        msg = msg[n:]


@aoc_timer
def Day19(data, part1=True):
    """This code works for the specific problem, i.e. [0: 8 11, 8: 42, 11: 42 31]
       This will not work in the general case as 31 and 42 are hard-coded here.
    """
    rules, messages = data
    # Rules of interest:
    R = {}
    for idx in [31, 42]:
        R[idx] = set(reduce(rules[idx], rules))
    # Part 1 message length
    chunk_len = len(next(iter(R[42])))
    msg_len = 3 * chunk_len
    # Check messages
    p1, p2 = 0, 0
    for msg in messages:
        if part1 and len(msg) > msg_len:
            continue
        cnt1, cnt2, flag = 0, 0, False
        Q = deque(chunk(msg, chunk_len))
        while Q:
            r = Q.pop()
            if r in R[31] and not flag:
                cnt1 += 1
            elif r in R[42]:
                flag = True
                cnt2 += 1
            else:
                cnt1 = cnt2 = 0
                break
        if cnt1 and cnt2 > cnt1 and flag:
            # Part 1
            if cnt2 - cnt1 == 1:
                p1 += 1
            # Part 2
            p2 += 1
    if part1:
        return p1
    return p2


# %% Output
def main():
    print("AoC 2020\nDay 19")
    data = get_input('input.txt')
    print("Part 1:", Day19(data, True))
    print("Part 2:", Day19(data, False))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 747 µs ± 2.66 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit Day19(data, True)
# 4.01 ms ± 30.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

# %timeit Day19(data, False)
# 4.68 ms ± 28 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
