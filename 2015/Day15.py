from time import time
import re
import numpy as np
from itertools import product, combinations_with_replacement

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day15.txt"

def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)

def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s

def get_input(path):
    delims = [': capacity ', ', durability ', ', flavor ', ', texture ', ', calories ']
    parse = lambda x: re_split(delims, x.strip())
    return {x.split(':')[0]: list(map(to_int,parse(x)[1:])) for x in open(path).readlines()}

def Day15(path,part):
    
    ing = get_input(path)
    cal = []
    
    # Put calories in separate list
    for k,v in ing.items():
        ing[k] = v[:-1]
        cal.append(v[-1])
    
    ans = 0
    tsp = 100
    kcal = 500
    
    # More general code here (need to figure out logic):
    # for recipe in combinations_with_replacement(ing.keys(),tsp):
    #     print('figure this part out')
    
    for a in range(tsp+1):
        for b in range(tsp+1-a):
            for c in range(tsp+1-a-b):
                d = tsp-a-b-c
                if part == 2:
                    cals = sum(x*y for x,y in zip([a,b,c,d],cal))
                    if cals != kcal:
                        continue
                temp = [max(0, a*p + b*q + c*r + d*s) for p,q,r,s in zip(*ing.values())]
                ans = max(ans, np.prod(temp))
    return ans


print("AoC 2015\nDay 15\n-----")
t0=time()
print("Part 1:",Day15(path,1))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",Day15(path,2))
print("Time:",time()-t0,"\n-----")

del t0, path