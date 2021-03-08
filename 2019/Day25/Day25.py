from helper import aoc_timer
from intcode import IntcodeComputer
from collections import deque
import sys
import re


class Colours:
    """ANSI code class for terminal highlighting."""

    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    class fg:
        """Foreground colours."""

        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        ORANGE = '\033[33m'
        BLUE = '\033[34m'
        PURPLE = '\033[35m'
        CYAN = '\033[36m'
        LIGHTGREY = '\033[37m'
        DARKGREY = '\033[90m'
        LIGHTRED = '\033[91m'
        LIGHTGREEN = '\033[92m'
        YELLOW = '\033[93m'
        LIGHTBLUE = '\033[94m'
        PINK = '\033[95m'
        LIGHTCYAN = '\033[96m'

    class bg:
        """Background colours."""

        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        ORANGE = '\033[43m'
        BLUE = '\033[44m'
        PURPLE = '\033[45m'
        CYAN = '\033[46m'
        LIGHTGREY = '\033[47m'


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


def highlight_word(word, base_map, colour=Colours.fg.BLUE, bold=True):
    """Highlight a given word in base_map with given colour."""
    word = r"" + word
    repl = f"{colour}{word}{Colours.ENDC}"
    if bold:
        repl = f"{Colours.BOLD}{repl}"
    return re.sub(word, repl, base_map)


def show_map(path, current_room, colour=Colours.fg.BLUE, bold=True):
    """
    Print ASCII map saved in file at path.
    Use RegEx and MapColours class to highlight currently occupied room.
    Relies on the fact that no words are repeated in the map.
    """
    base_map = open(path).read()
    room_reg = r""
    room_sep = r'[ \n#|\w]+'
    for word in current_room.split():
        # Handle hyphenated line overspill
        if '-' in word:
            for w in word.split('-'):
                if word.startswith(w + '-'):
                    w += '-'
                room_reg += f"({w})"
                if current_room.endswith(w):
                    break
                room_reg += room_sep
            continue
        room_reg += f"({word})"
        if current_room.endswith(word):
            break
        room_reg += room_sep
    words = re.findall(room_reg, base_map).pop()
    if isinstance(words, str):
        words = [words]
    for word in words:
        base_map = highlight_word(word, base_map, colour, bold)
    print(base_map, flush=True)
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
            show_map(map_file, current_room)
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
    current_room = None
    room_search = r'== ([a-zA-Z -]+) =='
    VM = IntcodeComputer(program_file, input=get_input)
    while not VM.halted:
        out = VM.run()
        if out is not None:
            encounter += (out := chr(out))
            if debug:
                print(out, end='', flush=routine_file is None)
            if out == '?':
                current_room = re.findall(room_search, encounter).pop()
    password = re.findall(r'\d+', encounter).pop()
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
