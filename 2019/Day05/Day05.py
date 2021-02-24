from helper import aoc_timer
from intcode import IntcodeComputer


# %% Day 5 Solver
@aoc_timer
def Day05(program_file, input, output=False):
    VM = IntcodeComputer(program_file, input)
    while not VM.halted:
        result = VM.run()
        if result is not None:
            diagnostic_code = result
    return diagnostic_code


# %% Output
def main():
    print("AoC 2019\nDay 05")
    program_file = 'input.txt'
    print("Part 1:", Day05(program_file, input=1))
    print("Part 2:", Day05(program_file, input=5))


if __name__ == '__main__':
    main()
