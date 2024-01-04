# %% Day 19
from helper import aoc_timer
from collections import deque
from math import prod


@aoc_timer
def get_input(path: str) -> tuple[dict, list[dict]]:
    workflows, parts = map(str.splitlines, open(path).read().split('\n\n'))
    W = {k: [x.split(':') for x in v.split(',')] for k, v in
         [w.strip('}').split('{') for w in workflows]}
    x, m, a, s = 'xmas'
    P = [eval(p.replace('=', ':')) for p in parts]
    return W, P


@aoc_timer
def solve(data: tuple[dict, list[dict]]) -> tuple[int]:
    W, P = data
    W['A'] = [1]
    W['R'] = [0]

    def process(valid: dict) -> int:
        '''
        Compare all unprocessed parts to the valid ratings and return the sum
        of the ratings for parts that are deemed valid.
        Mutates the parts list by removing parts that are accepted.
        '''
        result = 0
        accepted = []
        for idx, part in enumerate(P):
            if all(p in v for p, v in zip(part.values(), valid.values())):
                result += sum(part.values())
                accepted.append(idx)
        for idx in reversed(accepted):
            del P[idx]
        return result

    p1 = p2 = 0
    start, target = 'in', 'A'
    valid = {k: range(1, 4001) for k in 'xmas'}
    Q = deque([(start, valid)])
    while Q:
        w, valid = Q.popleft()
        if w == target:
            p1 += process(valid)
            p2 += prod(map(len, valid.values()))
            continue
        rules = W[w]
        for rule in rules:
            match rule:
                case str():
                    Q.append((rule, valid))
                case [k]:
                    Q.append((k, valid))
                case [cond, k]:
                    r, op, n = cond[0], cond[1], int(cond[2:])
                    v = valid.copy()
                    rng = v[r]
                    if op == '<':
                        v[r] = range(rng.start, min(rng.stop, n))
                        valid[r] = range(max(rng.start, n), rng.stop)
                    elif op == '>':
                        v[r] = range(max(rng.start, n + 1), rng.stop)
                        valid[r] = range(rng.start, min(rng.stop, n + 1))
                    Q.append((k, v))

    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 19")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
