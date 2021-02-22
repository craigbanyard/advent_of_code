from helper import aoc_timer
import re
from collections import deque


@aoc_timer
def get_input(path):
    notes, me, nearby = [y.split('\n') for y in [x for x in open(path).read().split('\n\n')]]
    notes = {k: map(int, re.findall(r'\d+', v)) for k, v in [line.split(': ') for line in notes]}
    notes = {k: set(range(a, b + 1)) | set(range(c, d + 1)) for k, (a, b, c, d) in notes.items()}
    me = [int(x) for x in me[1].split(',')]
    nearby = [list(map(int, line)) for line in [line.split(',') for line in nearby[1:]]]
    return notes, me, nearby


@aoc_timer
def Day16(data, part1=True):
    # Split input data into variables
    notes, me, nearby = data

    # Set of all valid numbers
    valid = set()
    for note in notes.values():
        valid |= note

    # Count invalid for part 1, drop invalid for part 2
    rate, valid_tickets = 0, [me]
    for ticket in nearby:
        t = set(ticket)
        diff = sum(t - valid)
        if part1:
            rate += diff
            continue
        if not diff:
            valid_tickets.append(ticket)
    if part1:
        return rate

    # Cycle positions until each is narrowed down to one possibility
    fields = len(me)
    F = {k: list(notes.keys()) for k in range(fields)}
    Q = deque(notes.keys())
    while Q:
        for pos in range(fields):
            for ticket in valid_tickets:
                for attribute in Q:
                    if ticket[pos] not in notes[attribute]:
                        if attribute in F[pos]:
                            F[pos].remove(attribute)
                if len(F[pos]) == 1:
                    done = F[pos][0]
                    if done in Q:
                        Q.remove(done)
                    for k in range(fields):
                        if k != pos and done in F[k]:
                            F[k].remove(done)
                    break
    # Final answer
    ans = 1
    for idx, val in enumerate(me):
        if F[idx][0].startswith('departure'):
            ans *= val
    return ans


# %% Output
def main():
    print("AoC 2020\nDay 16")
    data = get_input('input.txt')
    print("Part 1:", Day16(data))
    print("Part 2:", Day16(data, part1=False))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 2.04 ms ± 13.9 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

# %timeit Day16(data)
# 816 µs ± 2.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit Day16(data, part1=False)
# 23.5 ms ± 126 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
