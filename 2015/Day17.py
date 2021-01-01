from time import time
from itertools import combinations

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day17.txt"

def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]

def Day17(data, target=150):
    p1 = [cmb for r in range(len(data),0,-1) for cmb in combinations(data, r) if sum(cmb) == target]
    p2 = [1 for cmb in p1 if len(cmb) == min(map(len,p1))]
    return len(p1), len(p2)


# %% Output
print("AoC 2015\nDay 16\n-----")
t0=time()
data = get_input(path)
print("Data:",time()-t0,"\n-----")
t0=time()
p1,p2 = Day17(data)
print("Part 1:",p1)
print("Part 2:",p2)
print("Time:",time()-t0,"\n-----")

del t0, path, data, p1, p2