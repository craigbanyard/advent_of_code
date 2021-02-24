from helper import aoc_timer
from intcode import IntcodeComputer


# %% Day 2 Solver
@aoc_timer
def Day02(program_file, part1=True, target=None):
    if part1:
        VM = IntcodeComputer(program_file)
        VM.override({1: 12, 2: 2})
        VM.run()
        return VM.P[0]

    for noun in range(100):
        for verb in range(100):
            VM = IntcodeComputer(program_file)
            VM.override({1: noun, 2: verb})
            VM.run()
            if VM.P[0] == target:
                return (100 * noun) + verb


# %% Output
def main():
    print("AoC 2019\nDay 02")
    program_file = 'input.txt'
    print("Part 1:", Day02(program_file))
    print("Part 2:", Day02(program_file, part1=False, target=19690720))


if __name__ == '__main__':
    main()
