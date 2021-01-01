from time import time
import re

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day14.txt"

def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)

def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s

def get_input(path):
    delims = [' can fly ', ' km/s for ', ' seconds, but then must rest for ']
    parse = lambda x: re_split(delims, x.strip('seconds.\n'))
    return [list(map(to_int,parse(x))) for x in open(path).readlines()]

def get_pos(inp,t):
    R = {}
    for r, speed, dur, rest in inp:
        R[r] = (t//(dur+rest)*dur + 
        min(t%(dur+rest),dur)) * speed
    return [(k,v) for k, v in R.items() if v == max(R.values())]

def Day14(path,part):
    inp = get_input(path)
    t = 2503
    if part == 1:
        return get_pos(inp,t)
    
    # Part 2
    P = {}
    for t in range(2503):
        for r,p in get_pos(inp,t+1):
            if r not in P:
                P[r] = 1
                continue
            P[r] += 1
    
    return [(k,v) for k, v in P.items() if v == max(P.values())]

print("AoC 2015\nDay 14\n-----")
t0=time()
print("Part 1:",Day14(path,1))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",Day14(path,2))
print("Time:",time()-t0,"\n-----")

del t0, path