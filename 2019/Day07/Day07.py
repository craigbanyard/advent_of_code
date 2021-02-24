from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque
from itertools import permutations


# %% Day 7 Solver
@aoc_timer
def Day07(program_file, phase):

    def get_input(i):
        if Q[i]:
            return Q[i].popleft()
        return 0

    max_signal = 0
    for p in permutations(list(phase)):
        amps = []
        Q = []
        first_pass = True
        signal = 0
        while signal is not None:
            for i in range(5):
                if first_pass:
                    Q.append(deque([p[i]]))
                    amps.append(
                        IntcodeComputer(
                            program_file,
                            input=lambda: get_input(i),
                            program_id=i
                        )
                    )
                Q[i].append(signal)
                signal = amps[i].run()
            first_pass = False
            max_signal = max(signal if signal is not None else 0, max_signal)
    return max_signal


# %% Output
def main():
    print("AoC 2019\nDay 07")
    program_file = 'input.txt'
    print("Part 1:", Day07(program_file, range(5)))
    print("Part 2:", Day07(program_file, range(5, 10)))


if __name__ == '__main__':
    main()
