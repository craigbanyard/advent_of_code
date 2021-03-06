from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque


@aoc_timer
def Day23(program_file, part1=True, debug=False):

    # Constants
    N = 50

    def get_input(i):
        """Return next packet in queue for computer i, or -1 if empty."""
        if Q[i]:
            return Q[i].popleft()
        return -1

    network = {}
    Q = {}
    NAT = (None, None)
    for i in range(N):
        network[i] = IntcodeComputer(
            program_file,
            program_id=i,
            input=lambda: get_input(i)
        )
        Q[i] = deque([i])

    if not part1 and debug:
        print("\nNAT packets sent:")

    while True:
        for i in range(N):
            a = network[i].run(timeout=10)
            if a is None:
                continue
            x = network[i].run()
            y = network[i].run()
            if a == 255:
                if part1:
                    return y
                # Part 2 - NAT handling
                if all(not Q[j] for j in range(N)):
                    if NAT and NAT[1] == y:
                        return y
                    NAT = (x, y)
                    Q[0].append(x)
                    Q[0].append(y)
                    if debug:
                        print(y)
            else:
                Q[a].append(x)
                Q[a].append(y)


# %% Output
def main():
    print("AoC 2019\nDay 23")
    program_file = 'input.txt'
    print("Part 1:", Day23(program_file))
    print("Part 2:", Day23(program_file, part1=False, debug=True))


if __name__ == '__main__':
    main()
