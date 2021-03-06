from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque


@aoc_timer
def Day21(program_file, part1=True, debug=False):

    def get_input():
        """Function used as input to Intcode VM."""
        out = Q.popleft()
        if debug:
            print(chr(out), end='', flush=True)
        return out

    # Springscripts deduced logically
    p1_ss = [
        "NOT C T",
        "OR D J",
        "AND T J",
        "NOT A T",
        "OR T J",
        "WALK"
    ]
    p2_ss = [
        "NOT H J",
        "OR C J",
        "AND B J",
        "AND A J",
        "NOT J J",
        "AND D J",
        "RUN"
    ]

    # Queue springscript instructions
    Q = deque()
    springscript = p1_ss if part1 else p2_ss
    for instr in springscript:
        [Q.append(ord(ch)) for ch in instr]
        Q.append(10)

    VM = IntcodeComputer(program_file, input=get_input)
    while not VM.halted:
        out = VM.run()
        if out not in range(128):
            return out
        if debug:
            print(chr(out), end='', flush=True)


# %% Output
def main():
    print("AoC 2019\nDay 21")
    program_file = 'input.txt'
    print("Part 1:", Day21(program_file))
    print("Part 2:", Day21(program_file, part1=False))


if __name__ == '__main__':
    main()
