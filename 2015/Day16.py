from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day16.txt"

def get_input(path):
    return {int(k.lstrip('Sue ')): {kk: int(vv) for kk,vv in (pair.split(': ') for pair in v.split(', '))}
            for k,v in (x.strip().split(': ',1) for x in open(path).readlines())}


def Day16(data,part=1):
    
    # MFCSAM results
    M = {'children': 3,
         'cats': 7,
         'samoyeds': 2,
         'pomeranians': 3,
         'akitas': 0,
         'vizslas': 0,
         'goldfish': 5,
         'trees': 3,
         'cars': 2,
         'perfumes': 1,
         }

    # Part 1: search for three matching attributes    
    def part1():
        for sue,comps in data.items():
            matches = 0
            for k,v in M.items():
                if k in comps:
                    if comps[k] == v:
                        matches += 1
                if matches == 3:
                    return sue

    # Part 2: search for three matching attributes
    def part2():
        
        # Part 2 comparison
        P = {}
        for k in M.keys():
            if k in ['cats','trees']:
                P[k] = lambda x,y : x > y
            elif k in ['pomeranians', 'goldfish']:
                P[k] = lambda x,y : x < y
            else:
                P[k] = lambda x,y : x == y
        
        for sue,comps in data.items():
            matches = 0
            for k,v in M.items():
                if k in comps:
                    if P[k](comps[k],v):
                        matches += 1
                if matches == 3:
                    return sue
     
    return part1() if part == 1 else part2()
        

# %% Output
print("AoC 2015\nDay 16\n-----")
t0=time()
data = get_input(path)
print("Data:",time()-t0,"\n-----")
t0=time()
print("Part 1:",Day16(data))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",Day16(data,2))
print("Time:",time()-t0,"\n-----")

del t0, path, data