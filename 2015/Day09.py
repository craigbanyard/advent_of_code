from time import time
from itertools import permutations
from math import inf

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day09.txt"

def get_input(path):
    return [x.strip().split()[::2] for x in open(path).readlines()]

# Function used to discard routes that are the reverse of other routes
# This halves the number of permutations (iterations) required to find shortest/longest route
def get_unique_perms(locations):
    for p in permutations(locations):
        if p <= p[::-1]:
            yield p

def Day09(path):
    D = {}
    for a,b,d in get_input(path):
        # Add distances (both directions, saves check within loop) to dictionary
        D[(a,b)] = D[(b,a)] = int(d)
    L = set(v for k in D for v in k)
    shortest, longest = inf, 0
    for p in get_unique_perms(L):
        dist = sum(D[(a,b)] for a,b in zip(p,p[1:]))
        shortest = min(dist, shortest)
        longest = max(dist, longest)
    return shortest,longest

print("AoC 2015\nDay 9\n-----")
t0=time()
p1,p2 = Day09(path)
print("Part 1:",p1)
print("Part 2:",p2,"\nTime:",time()-t0,"\n-----")

del path, t0, p1, p2