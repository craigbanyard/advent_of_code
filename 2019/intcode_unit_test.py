# %% Imports
import os
from Day02.Day02 import Day02
from Day05.Day05 import Day05
from Day07.Day07 import Day07
from Day09.Day09 import Day09
from Day11.Day11 import Day11
from Day13.Day13 import Day13
from Day15.Day15 import Day15
from Day17.Day17 import Day17
from Day19.Day19 import Day19


path = os.getcwd()


# %% Day 02
def unit02():
    print("\nDay 02")
    program_file = path + '\\Day02\\input.txt'
    p1 = Day02(program_file)
    p2 = Day02(program_file, part1=False, target=19690720)
    return p1, p2


# %% Day 05
def unit05():
    print("\nDay 05")
    program_file = path + '\\Day05\\input.txt'
    p1 = Day05(program_file, input=1)
    p2 = Day05(program_file, input=5)
    return p1, p2


# %% Day 07
def unit07():
    print("\nDay 07")
    program_file = path + '\\Day07\\input.txt'
    p1 = Day07(program_file, range(5))
    p2 = Day07(program_file, range(5, 10))
    return p1, p2


# %% Day 09
def unit09():
    print("\nDay 09")
    program_file = path + '\\Day09\\input.txt'
    p1 = Day09(program_file, input=1)
    p2 = Day09(program_file, input=2)
    return p1, p2


# %% Day 11
def unit11():
    print("\nDay 11")
    program_file = path + '\\Day11\\input.txt'
    p1 = Day11(program_file, (120, 120), part1=True, asc=False, mpl=False)
    p2 = Day11(program_file, (8, 45), part1=False, asc=True, mpl=False)
    return p1, p2


# %% Day 13
def unit13():
    print("\nDay 13")
    program_file = path + '\\Day13\\input.txt'
    p1 = Day13(program_file, (23, 43), part2=False, plot=False)
    p2 = Day13(program_file, (25, 43), part2=True, plot=False)
    return p1, p2


# %% Day 15
def unit15():
    print("\nDay 15")
    program_file = path + '\\Day15\\input.txt'
    grid_dimensions = (43, 43)
    p1 = Day15(program_file, grid_dimensions)
    p2 = Day15(program_file, grid_dimensions, part1=False)
    return p1, p2


# %% Day 17
def unit17():
    print("\nDay 17")
    program_file = path + '\\Day17\\input.txt'
    routine_file = path + '\\Day17\\routine.txt'
    p1 = Day17(program_file, routine_file=routine_file)
    p2 = Day17(program_file, part1=False, routine_file=routine_file)
    return p1, p2


# %% Day 19
def unit19():
    print("\nDay 19")
    program_file = path + '\\Day19\\input.txt'
    p1 = Day19(program_file)
    p2 = Day19(program_file, part2=True)
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
    17: unit17(),
    19: unit19()
}

# Display unit test results
print("\n" + "=" * 80)
for day in expected:
    exp = expected.get(day, 0)
    res = results.get(day, 0)
    print(f"Day {day}: Pass: {exp == res}, Expected: {exp}, Result: {res}")
