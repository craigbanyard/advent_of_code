from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque
import sys
import re


def get_routine(path):
    """
    Return a generator for all characters (as ASCII) in file at path.
    Routine generated via playing game manually in interactive shell.

    To auto-solve this, need to write a routing algorithm (e.g. BFS)
    to traverse the map, and then another algorithm to try different
    combinations of objects on the scale in the last room.
    """
    for x in open(path).read():
        yield ord(x)


def show_map(path):
    """
    Print the ASCII map in file at path.

    Want to develop this to highlight the map to show current position.
    Can also extend to highlight required/dangerous/decoy items.

    RegEx for finding room from output:
    r'== ([a-zA-Z -]+) =='
    The matched group above (or last matched group if multiple rooms visited)
    is the current room.

    Can use this information to find the room in the map and highlight:
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal

    Difficulty comes from text spanning multiple lines in the map...
    Possible RegEx:
    r'(Gift)[ \n#|]+(Wrapping)[ \n#|]+(Center)'
    e.g. split the result of the first RegEx giving ['Gift', 'Wrapping', 'Center'],
    then construct above RegEx by joining this list with '[ \n#|]+' as separator.
    """
    for line in open(path).read().split("\n"):
        print(line, flush=True)
    print("Command?")


@aoc_timer
def Day25(program_file, debug=True, routine_file=None, map_file='map.txt'):

    def get_input():
        """Function used as input to Intcode VM."""
        if not Q:
            queue_input(input())
        out = Q.popleft()
        if debug:
            print(chr(out), end='', flush=True)
        return out

    def queue_input(cmd):
        """Add user input to VM input queue."""
        if cmd.lower().startswith('q'):
            print("Exiting game...")
            sys.exit(0)
        elif cmd.lower().startswith('m'):
            show_map(map_file)
            queue_input(input())
        else:
            for ch in cmd:
                Q.append(ord(ch))
            Q.append(10)

    def queue_auto(routine):
        """Add auto-solved instructions to VM input queue."""
        for ch in routine:
            Q.append(ch)

    Q = deque()
    if routine_file is not None:
        queue_auto(get_routine(routine_file))

    encounter = ""
    VM = IntcodeComputer(program_file, input=get_input)
    while not VM.halted:
        out = VM.run()
        if out is not None:
            encounter += (out := chr(out))
            if debug:
                print(out, end='')
    password = re.findall(r'\d+', encounter)[-1]
    return int(password)


# %% Output
def main():
    print("AoC 2019\nDay 25")
    program_file = 'input.txt'
    routine_file = 'routine.txt'
    map_file = 'map.txt'
    print("Part 1:", Day25(program_file, True, routine_file, map_file))


if __name__ == '__main__':
    main()
