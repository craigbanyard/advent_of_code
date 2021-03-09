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
    HIDE = '\033[8m'
    STRIKE = '\033[9m'

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


class Day25:
    """Solution encapsulated in class due to many arguments and methods."""

    # Constants
    ROOM_COLOUR = Colours.BOLD + Colours.fg.YELLOW
    ITEM_COLOURS = {
        'required': Colours.fg.GREEN,
        'decoy': Colours.fg.BLUE,
        'hazard': Colours.fg.RED
    }
    MAP_KEY = {
        0: 'Current Room',
        'required': 'Required Item',
        'decoy': 'Decoy Item',
        'hazard': 'Hazardous Item'
    }
    END_COLOUR = Colours.ENDC
    ROOM_SEARCH = r'== ([a-zA-Z -]+) =='

    def __init__(self,
                 program_file,
                 routine_file=None,
                 map_file='map.txt',
                 key_file='key.txt',
                 output=True
        ):
        # Initialisation arguments
        self.program_file = program_file
        self.routine_file = routine_file
        self.map_file = map_file
        self.key_file = key_file
        self.output = output
        # Game control
        self.routine = self.set_routine()
        self.Q = deque()
        self.cmd = None
        self.out = None
        self.encounter = ""
        # Mapping
        self.key = self.set_key()
        self.cheats = None
        self.current_room = None
        self.base_map = open(self.map_file).read()

    def set_routine(self):
        """
        Return a generator for all characters (as ASCII) in file at path.
        Routine generated via playing game manually in interactive shell.

        To auto-solve this, need to write a routing algorithm (e.g. BFS)
        to traverse the map, and then another algorithm to try different
        combinations of objects on the scale in the last room.
        """
        if self.routine_file is None:
            return None
        for x in open(self.routine_file).read():
            yield ord(x)

    def set_key(self):
        """Set the key for rooms and items."""
        return {
            k: v.split(", ") for k, v in [line.split(": ")
            for line in open(self.key_file).read().split('\n')]
        }

    def set_cheats(self):
        """Read last input command and set cheats if enabled."""
        if self.cmd is None:
            return None
        if self.cmd.lower().startswith('m'):
            _, *arg = self.cmd.split(' -')
            if not arg:
                return None
            if arg[0] == 'x':
                self.cheats = None
                return None
            assert arg[0] == 'c', f"Invalid cheat flag: -{arg[0]}"
            if len(arg) == 1:
                # All cheats enabled
                self.cheats = list(self.ITEM_COLOURS.keys())
            else:
                # Subset of cheats enabled
                self.cheats = []
                item_map = {it[0]: it for it in self.ITEM_COLOURS}
                for cheat in arg[1:]:
                    assert cheat in item_map, f"Invalid cheat flag: -{cheat}"
                    self.cheats.append(item_map[cheat])
            return self.cheats
        return None

    def make_words(self, words):
        """
        Return valid search patterns based on whether words span
        multiple lines or are hypenated.
        """
        if re.search(fr"{words}", self.base_map):
            # Pattern exists on single line - can search directly
            return [fr"{words}"]
        out = []
        for word in words.split():
            # Handle hyphenated line overspill
            if '-' in word:
                for w in word.split('-'):
                    if word.startswith(w + '-'):
                        w += '-'
                    out.append(fr"{w}")
                continue
            # No hyphenation
            out.append(fr"{word}")
        return out

    def highlight_word(self, word, colour, base_map):
        """Highlight a given word in base_map with given colour."""
        repl = f"{colour}{word}{self.END_COLOUR}"
        return re.sub(word, repl, base_map)

    def highlight_items(self):
        """Highlight items on base_map according to enabled cheats."""
        base_map = self.base_map
        if self.cheats is None:
            return base_map
        for cheat in self.cheats:
            for item in self.key[cheat]:
                colour = self.ITEM_COLOURS[cheat]
                key_label = self.MAP_KEY[cheat]
                for word in self.make_words(item):
                    base_map = self.highlight_word(word, colour, base_map)
                base_map = self.highlight_word(key_label, colour, base_map)
        return base_map

    def show_map(self):
        """
        Print ASCII map saved in file at self.map_file.
        Use RegEx and Colours class to highlight currently occupied room.
        Relies on the fact that no words are repeated in the map.
        """
        base_map = self.highlight_items()
        colour = self.ROOM_COLOUR
        label = self.MAP_KEY[0]
        for word in self.make_words(self.current_room):
            base_map = self.highlight_word(word, colour, base_map)
        base_map = self.highlight_word(label, colour, base_map)
        print(base_map, flush=True)
        print("Command?")

    def get_input(self):
        """Function used as input to Intcode VM."""
        if not self.Q:
            self.queue_input(input())
        out = self.Q.popleft()
        if self.output:
            print(chr(out), end='', flush=True)
        return out

    def queue_input(self, inp):
        """Add user input to VM input queue."""
        self.cmd = inp
        if self.cmd.lower().startswith('q'):
            print("Exiting game...")
            sys.exit(0)
        elif self.cmd.lower().startswith('m'):
            print(self.cmd, flush=True)
            self.set_cheats()
            self.show_map()
            self.queue_input(input())
        else:
            for ch in self.cmd:
                self.Q.append(ord(ch))
            self.Q.append(10)

    def queue_auto(self):
        """Add auto-solved instructions to VM input queue."""
        for ch in self.routine:
            self.Q.append(ch)

    @aoc_timer
    def solve(self):
        if self.routine is not None:
            self.queue_auto()

        VM = IntcodeComputer(self.program_file, input=self.get_input)
        while not VM.halted:
            out = VM.run()
            if out is not None:
                self.encounter += (out := chr(out))
                if self.output:
                    print(out, end='', flush=self.routine is None)
                if out == '?':
                    self.current_room = re.findall(
                        self.ROOM_SEARCH,
                        self.encounter
                    ).pop()
        password = re.findall(r'\d+', self.encounter).pop()
        return int(password)


# %% Output
def main():
    print("AoC 2019\nDay 25")
    program_file = 'input.txt'
    routine_file = 'routine.txt'
    map_file = 'map.txt'
    key_file = 'key.txt'
    droid = Day25(program_file, routine_file, map_file, key_file, output=True)
    print("Part 1:", droid.solve())


if __name__ == '__main__':
    main()
