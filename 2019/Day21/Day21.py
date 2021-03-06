from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque


@aoc_timer
def Day21(program_file, part=1, debug=False):

    def get_input():
        """Return next queued ASCII value as input to VM."""
        ch = Q.popleft()
        if debug:
            print(ch, end='', flush=True)
        return ord(ch)

    # Springscripts deduced logically
    S = {
        1: [
            "NOT C T",
            "OR D J",
            "AND T J",
            "NOT A T",
            "OR T J",
            "WALK"
        ],
        2: [
            "NOT H J",
            "OR C J",
            "AND B J",
            "AND A J",
            "NOT J J",
            "AND D J",
            "RUN"
        ]
    }

    # Queue springscript instructions
    Q = deque()
    for instr in S[part]:
        [Q.append(ch) for ch in instr]
        Q.append("\n")

    # Neater output
    if debug:
        print()

    # Continuously run until non-ASCII output returned
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
    print("Part 1:", Day21(program_file, part=1))
    print("Part 2:", Day21(program_file, part=2))


if __name__ == '__main__':
    main()
