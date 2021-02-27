# %% Imports
from helper import aoc_timer
from intcode import IntcodeComputer
import itertools
from collections import deque
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os


path = os.getcwd()


# %% Day 02
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


def unit02():
    program_file = path + '\\Day02\\input.txt'
    p1 = Day02(program_file)
    p2 = Day02(program_file, part1=False, target=19690720)
    return p1, p2


# %% Day 05
def Day05(program_file, input):
    VM = IntcodeComputer(program_file, input)
    while not VM.halted:
        result = VM.run()
        if result is not None:
            diagnostic_code = result
    return diagnostic_code


def unit05():
    program_file = path + '\\Day05\\input.txt'
    p1 = Day05(program_file, input=1)
    p2 = Day05(program_file, input=5)
    return p1, p2


# %% Day 07
def Day07(program_file, phase):

    def get_input(i):
        if Q[i]:
            return Q[i].popleft()
        return 0

    max_signal = 0
    for p in itertools.permutations(list(phase)):
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


def unit07():
    program_file = path + '\\Day07\\input.txt'
    p1 = Day07(program_file, range(5))
    p2 = Day07(program_file, range(5, 10))
    return p1, p2


# %% Day 09
def Day09(program_file, input):
    VM = IntcodeComputer(program_file, input)
    return VM.run()


def unit09():
    program_file = path + '\\Day09\\input.txt'
    p1 = Day09(program_file, input=1)
    p2 = Day09(program_file, input=2)
    return p1, p2


# %% Day 11
def Day11(program_file, grid_init, part1=True, asc=False, mpl=False):

    # Function to get current tile colour
    def get_input():
        return G[r][c]

    # Set up grid
    R, C = grid_init
    G = [[0 for _ in range(C)] for _ in range(R)]
    d = 0
    dR, dC = [-1, 0, 1, 0], [0, -1, 0, 1]
    painted = set()

    # Initialise Intcode computer
    VM = IntcodeComputer(program_file, input=get_input)

    if part1:
        # Start robot in centre of grid
        r, c = R // 2, C // 2
    else:
        # Start robot near top-left corner of grid on a white tile
        r, c = 1, 2
        G[r][c] = 1

    # Carry on receiving output from program until it halts
    while True:
        colour = VM.run()
        if colour is None:
            break
        G[r][c] = colour
        painted.add((r, c))
        turn = VM.run()
        if turn == 0:
            d = (d + 1) % 4
        else:
            d = (d + 3) % 4
        r += dR[d]
        c += dC[d]

    if mpl:
        # Matplotlib plot
        plt.figure()
        plt.imshow(G, cmap='gray')
        plt.axis('off')

    if asc:
        # Paint grid
        if part1:
            msg = str(len(painted)) + "\n"
        else:
            msg = "\n"
        for r in range(R):
            for c in range(C):
                if G[r][c] == 1:
                    msg += '#'
                else:
                    msg += " "
            msg += "\n"
        return msg

    if part1:
        return len(painted)
    return ""


def unit11():
    program_file = path + '\\Day11\\input.txt'
    p1 = Day11(program_file, (120, 120), part1=True, asc=False, mpl=False)
    p2 = Day11(program_file, (8, 45), part1=False, asc=True, mpl=False)
    return p1, p2


# %% Day 13
def Day13(program_file, grid_init, part2=False, plot=False):

    def get_joystick():
        """Simple AI tracking the ball position with the paddle."""
        return np.sign(ball - paddle)

    # Set up grid (determined from wall positions)
    R, C = grid_init
    G = [[0 for _ in range(C)] for _ in range(R)]

    # Initialise Intcode program
    if part2:
        VM = IntcodeComputer(program_file, input=get_joystick)
        VM.override({0: 2})
        # Buffer for score display at the top of screen
        row_buffer = 2
    else:
        VM = IntcodeComputer(program_file)
        row_buffer = 0

    # Carry on receiving output from program until it halts
    while True:
        c, r, tile = [VM.run() for _ in range(3)]
        if c == -1:
            score = tile
        if VM.halted:
            break
        elif tile == 3:
            paddle = c    # Save paddle x-position
        elif tile == 4:
            ball = c      # Save ball x-position
        G[r + row_buffer][c] = tile

    # Matplotlib plot
    if plot:
        plt.figure()
        plt.imshow(G, cmap='gist_stern')
        plt.axis('off')
        if part2:
            plt.text(
                42.2, 0.6, "Score: " + str(score), fontsize=9, family='Consolas',
                color='white', horizontalalignment='right'
            )

    if part2:
        return score
    return sum(x.count(2) for x in G)


def unit13():
    program_file = path + '\\Day13\\input.txt'
    p1 = Day13(program_file, (23, 43), part2=False, plot=False)
    p2 = Day13(program_file, (25, 43), part2=True, plot=False)
    return p1, p2


# %% Day 15
def Day15(program_file, grid_init, part1=True, plot=None):

    # Constants
    WALL = 0
    TRAVERSED = 1
    OXYGEN = 2
    DROID = 3
    UNEXPLORED = 4
    CLOCKWISE = {
        1: 4,
        2: 3,
        3: 1,
        4: 2
    }
    ANTICLOCKWISE = {v: k for k, v in CLOCKWISE.items()}
    DR, DC = [None, -1, 1, 0, 0], [None, 0, 0, -1, 1]

    def get_command(movement_command, status_code):
        """Determine next input command, N (1), S (2), W (3), E (4)."""
        if movement_command is None:
            return 1
        if status_code == WALL:
            return ANTICLOCKWISE[movement_command]
        if status_code == TRAVERSED:
            return CLOCKWISE[movement_command]
        else:
            assert status_code == OXYGEN
            return 1

    def get_input():
        """Function used as input to Intcode VM."""
        return movement_command

    def draw_grid(G, style='ascii'):
        """
        Draw a representation of G in a given style.

        Arguments:
          G -- grid to draw
          style -- method of visualisation, two accepted string values:
            'ascii':  ASCII art
            'mpl':    Matplotlib plot
        """

        # ASCII art mapping
        ASCII = {
            WALL: "#",
            TRAVERSED: ".",
            OXYGEN: "O",
            DROID: "D",
            UNEXPLORED: " "
        }

        # Draw ASCII art
        if style.lower() == 'ascii':
            grid = "\n"
            for r in G:
                for c in r:
                    grid += ASCII[c]
                grid += "\n"
            print(grid)
            return None

        # Matplotlib plot
        assert style.lower() == 'mpl', f"Invalid plot style: {style}"
        plt.figure(figsize=(8, 8))
        cmap = ListedColormap([
            'xkcd:dark indigo',        # Walls
            'white',                   # Traversed
            'crimson',                 # Oxygen
            'xkcd:azure',              # Droid
            'black'                    # Unexplored
        ])
        plt.imshow(G, cmap=cmap)
        plt.axis('off')
        return None

    # Initialise grid
    R, C = grid_init
    r = r0 = R // 2 + 1
    c = c0 = (C // 2) + 1
    G = [[UNEXPLORED for _ in range(C)] for _ in range(R)]
    G[r][c] = DROID
    movement_command = None
    status_code = None
    commands = 0
    visited = {(r0, c0): commands}
    # Part 2
    longest = 0
    oxygen_found = False
    oxygen_path = {}

    # Initialise Intcode program
    VM = IntcodeComputer(program_file, input=get_input)

    while not VM.halted:
        movement_command = get_command(movement_command, status_code)
        dr, dc = DR[movement_command], DC[movement_command]
        status_code = VM.run()
        # Process output
        if status_code == WALL:
            # Hit a wall, droid cannot move in given direction
            G[r + dr][c + dc] = WALL
            continue
        # Droid successfully moved in the given direction
        if G[r][c] != OXYGEN:
            G[r][c] = TRAVERSED
        r += dr
        c += dc
        # Update visited
        if (r, c) not in visited:
            commands += 1
            visited[(r, c)] = commands
        else:
            # Backtracking after hitting dead-end
            commands -= 1
        # Update oxygen path
        if oxygen_found and (r, c) not in oxygen_path:
            longest += 1
            oxygen_path[(r, c)] = longest
        elif oxygen_found:
            longest -= 1
        # Successful movement status codes
        if status_code == OXYGEN:
            G[r][c] = OXYGEN
            if part1:
                if plot:
                    G[r0][c0] = DROID
                    draw_grid(G, style=plot)
                return commands
            oxygen_found = True
        else:
            assert status_code == TRAVERSED
            G[r][c] = DROID
        # Halt if we're back at the starting position
        if (r, c) == (r0, c0):
            break

    if plot:
        draw_grid(G, style=plot)
    return max(oxygen_path.values())


def unit15():
    program_file = path + '\\Day15\\input.txt'
    grid_dimensions = (43, 43)
    p1 = Day15(program_file, grid_dimensions)
    p2 = Day15(program_file, grid_dimensions, part1=False)
    return p1, p2


# %% Day 17
def Day17(program_file, part1=True, debug=False, plot=None):

    def get_routine(path):
        """
        Return a generator for all integers in file at given path.
        Routine generated via trial and error in Excel.

        To auto-solve this, need to write a routing algorithm (e.g. BFS)
        to traverse the scaffold, then a compression algorithm to compress
        the path such that it meets the memory constraints.
        """
        for x in open(path).read().split(','):
            yield int(x)

    # Constants
    MAP = {
        '.': 0,
        '#': 1,
        '^': 2,
        'v': 2,
        '<': 2,
        '>': 2
    }
    ROUTINE = get_routine(path + '\\Day17\\routine.txt')

    def get_input():
        """Function used as input to Intcode VM."""
        out = next(ROUTINE)
        if debug:
            print(chr(out), end='', flush=True)
        return out

    def scaffold_grid(scaffolds):
        """Convert scaffolds string into numeric grid."""
        return [[MAP[ch] for ch in line]
                for line in scaffolds.strip('\n').split('\n')]

    def get_intersections(scaffolds):
        """Return set of coordinates of all scaffold intersections."""
        G = scaffold_grid(scaffolds)
        R, C = len(G), len(G[0])
        intersections = set()
        dirs = [
            (-1, 0),        # Up
            (0, 1),         # Right
            (1, 0),         # Down
            (-1, 0)         # Left
        ]
        for r, c in itertools.product(range(1, R - 1), range(1, C - 1)):
            if G[r][c] == MAP['#']:
                if all(G[r + dr][c + dc] == MAP['#'] for (dr, dc) in dirs):
                    intersections.add((r, c))
        return intersections

    def plot_scaffolds(scaffolds, intersections=None):
        """Matplotlib plot of scaffolds from string representation."""
        G = scaffold_grid(scaffolds)
        colours = [
            'white',               # Space
            'midnightblue',        # Scaffold
            'dodgerblue',          # Robot
        ]
        if intersections is not None:
            # Append intersection colour to colour map
            colours.append('lightsteelblue')
            intersection = max(MAP.values()) + 1
            # Amend intersection values
            for r, c in intersections:
                G[r][c] = intersection
        # Show plot
        plt.figure(figsize=(8, 8))
        plt.imshow(G, cmap=ListedColormap(colours))
        plt.axis('off')
        return None

    # Initialise Intcode program
    VM = IntcodeComputer(program_file, input=get_input)
    if not part1:
        VM.override({0: 2})
    scaffolds = debug_out = "\n"

    while not VM.halted:
        out = VM.run()
        if out not in range(128):
            break
        scaffolds += chr(out)
        # Full debug output
        if debug:
            debug_out += chr(out)
            if out == 10:
                print(debug_out, end='')
                debug_out = ""

    if part1:
        intersections = get_intersections(scaffolds)
        # Plot
        if plot:
            plot_scaffolds(scaffolds, intersections)
        return sum(r * c for r, c in intersections)
    return out


def unit17():
    program_file = path + '\\Day17\\input.txt'
    p1 = Day17(program_file)
    p2 = Day17(program_file, part1=False)
    return p1, p2


# %% Unit tests

day11_2_exp = '\n' + \
    '                                             \n' + \
    '    ##  #### ###  #  # ####   ##  ##  ###    \n' + \
    '   #  # #    #  # # #     #    # #  # #  #   \n' + \
    '   #    ###  #  # ##     #     # #    #  #   \n' + \
    '   #    #    ###  # #   #      # #    ###    \n' + \
    '   #  # #    #    # #  #    #  # #  # # #    \n' + \
    '    ##  #### #    #  # ####  ##   ##  #  #   \n' + \
    '                                             \n'

# Expected results
expected = {
    2: (3166704, 8018),
    5: (13547311, 236453),
    7: (17790, 19384820),
    9: (3507134798, 84513),
    11: (2268, day11_2_exp),
    13: (361, 17590),
    15: (318, 390),
    17: (4112, 578918),
    19: (189, 7621042),
    21: (19350938, 1142986901),
    23: (18604, 11880),
    25: (2147485856, None)
}

# Run solvers
results = {
    2: unit02(),
    5: unit05(),
    7: unit07(),
    9: unit09(),
    11: unit11(),
    13: unit13(),
    15: unit15(),
    17: unit17()
}

# Display unit test results
for day in expected:
    exp = expected.get(day, 0)
    res = results.get(day, 0)
    print(f"Day {day}: Pass: {exp == res}, Expected: {exp}, Result: {res}")
