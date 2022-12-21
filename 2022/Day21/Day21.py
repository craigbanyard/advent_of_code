from helper import aoc_timer, sign
import operator as op


@aoc_timer
def get_input(path: str) -> dict[str: list[str]]:
    return {k: v.split() for k, v in
            [line.split(': ') for line in open(path).read().splitlines()]}


@aoc_timer
def solve(data: dict[str: list[str]], part1: bool = True) -> int:

    OP = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv
    }

    def yell(monkey):
        '''Cannott use DP since Part 2 invalidataes the cache.'''
        match data[monkey]:
            case [n]:
                return int(n)
            case a, op, b:
                return OP[op](yell(a), yell(b))
            case _:
                return None

    def depends(m1, m2):
        '''Determine whether m1 result depends on m2.'''
        match data[m1]:
            case [_]:
                return False
            case a, _, b:
                if a == m2 or b == m2:
                    return True
                return depends(a, m2) or depends(b, m2)

    if part1:
        return int(yell('root'))

    m1, _, m2 = data['root']
    # Some observations from an initial brute force attempt:
    # Let n = data['humn'], i.e., the number the human shouts.
    # Let yell(m1) = M1 and yell(m2) = M2
    # 1. M1 decreases as n increases
    # 2. M2 remains constant, i.e., is independent of n
    # 3. M2 > M1 when n = 0
    # 4. ⇔ R = M1 - M2 decreases as n increases
    # We could therefore fix the target as M2 and perform binary
    # search on M1 to find n.
    # These observations do not hold for the sample input, so it
    # is assumed that they do not necessarily hold for all inputs,
    # so they have been ignored for the final solution.

    # Determine how R moves with changes in n
    lo, hi = 0, 1e15
    data['humn'] = [lo]
    result_lo = yell(m1) - yell(m2)
    data['humn'] = [hi]
    result_hi = yell(m1) - yell(m2)
    traj = sign(result_lo - result_hi)

    # Binary search
    while hi - lo > 1:
        n = (hi + lo) // 2
        data['humn'] = [n]
        result = yell(m1) - yell(m2)
        if result == 0:
            return int(n)
        if sign(result) == traj:
            lo = n
        else:
            hi = n

    return None


# %% Output
def main() -> None:
    print("AoC 2022\nDay 21")
    data = get_input('input.txt')
    print("Part 1:", solve(data, part1=True))
    print("Part 2:", solve(data, part1=False))


if __name__ == '__main__':
    main()
