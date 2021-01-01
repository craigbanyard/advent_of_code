from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day02.txt"

def get_input(path):
    return [list(map(int,x.strip().split('x'))) for x in open(path).readlines()]

def wrapping(present):
    a,b,c = present
    return 2*(a*b+b*c+a*c) + min(a*b,b*c,a*c)

def ribbon(present):
    a,b,c = present
    return 2*min(a+b,b+c,a+c) + a*b*c

def day2(path):
    t0 = time()
    dims = get_input(path)
    part1 = sum([wrapping(p) for p in dims])
    print("Part 1:",part1,"\nTime:",time()-t0,"\n-----")
    t0 = time()
    part2 = sum([ribbon(p) for p in dims])
    print("Part 2:",part2,"\nTime:",time()-t0,"\n-----")
    
print("AoC 2015\nDay 2\n-----")
day2(path)

del path