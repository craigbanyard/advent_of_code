from helper import aoc_timer
from intcode import IntcodeComputer


# %% Day 9 Solver
@aoc_timer
def Day09(program_file, input):
    VM = IntcodeComputer(program_file, input)
    return VM.run()


# %% Output
def main():
    print("AoC 2019\nDay 09")
    program_file = 'input.txt'
    print("Part 1:", Day09(program_file, input=1))
    print("Part 2:", Day09(program_file, input=2))


if __name__ == '__main__':
    main()
