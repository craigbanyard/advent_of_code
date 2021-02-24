# %% Imports
from helper import aoc_timer
from intcode import IntcodeComputer
from itertools import permutations
from collections import deque
from matplotlib import pyplot as plt
import os


path = os.getcwd()


# %% Day 02
def Day02(program_file, part1=True, target=None):
    if part1:
        C = IntcodeComputer(program_file)
        C.override({1: 12, 2: 2})
        C.run()
        return C.P[0]

    for noun in range(100):
        for verb in range(100):
            C = IntcodeComputer(program_file)
            C.override({1: noun, 2: verb})
            C.run()
            if C.P[0] == target:
                return (100 * noun) + verb


def unit02():
    program_file = path + '\\Day02\\input.txt'
    p1 = Day02(program_file)
    p2 = Day02(program_file, part1=False, target=19690720)
    return p1, p2


# %% Day 05
def Day05(program_file, input):
    C = IntcodeComputer(program_file, input)
    while not C.halted:
        result = C.run()
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


def unit07():
    program_file = path + '\\Day07\\input.txt'
    p1 = Day07(program_file, range(5))
    p2 = Day07(program_file, range(5, 10))
    return p1, p2


# %% Day 09
def Day09(program_file, input):
    C = IntcodeComputer(program_file, input)
    return C.run()


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
    P = IntcodeComputer(program_file, input=get_input)

    if part1:
        # Start robot in centre of grid
        r, c = R // 2, C // 2
    else:
        # Start robot near top-left corner of grid on a white tile
        r, c = 1, 2
        G[r][c] = 1

    # Carry on receiving output from program until it halts
    while True:
        colour = P.run()
        if colour is None:
            break
        G[r][c] = colour
        painted.add((r, c))
        turn = P.run()
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
    11: unit11()
}

# Display unit test results
for day in expected:
    exp = expected.get(day, 0)
    res = results.get(day, 0)
    print(f"Day {day}: Pass: {exp == res}, Expected: {exp}, Result: {res}")
