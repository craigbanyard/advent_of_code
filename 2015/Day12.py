from time import time
import re

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day12.txt"

def get_input(path):
    return open(path).read()

# Regex on string input
def sum_json(j):
    return sum(map(int, re.findall('-?\d+', j)))

# Recursive sum on JSON input where property != item
def filter_json(j, item):
    if isinstance(j, int):
        return j
    if isinstance(j, list):
        return sum([filter_json(i, item) for i in j])
    if not isinstance(j, dict):
        return 0
    if item in j.values():
        return 0
    return filter_json(list(j.values()),item)

def part1(path):
    return sum_json(get_input(path))

def part2(path):
    j = eval(get_input(path))
    return filter_json(j,'red')

print("AoC 2015\nDay 12\n-----")
t0=time()
print("Part 1:",part1(path))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",part2(path))
print("Time:",time()-t0,"\n-----")

del t0, path


# %% Original thinking:

# Recursive sum on JSON input where property == item
def find_json(j, item):
    if isinstance(j, dict):
        if item in j.values():
            yield sum_json(str(j))
        else:
            yield from find_json(list(j.values()), item)
    elif isinstance(j, list):
        for line in j:
            yield from find_json(line, item)

# Original idea
def Day12(path):
    jstr = get_input(path)
    p1 = sum_json(jstr)
    p2 = p1 - sum(find_json(eval(jstr),'red'))
    return p1,p2