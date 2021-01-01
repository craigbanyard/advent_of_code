from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day08.txt"

def get_input(path):
    return [x.strip() for x in open(path).readlines()]

def Day08(path):
    file = get_input(path)
    p1 = sum(len(s)-len(eval(s)) for s in file)
    p2 = sum(2+s.count('\\')+s.count('"') for s in file)
    return p1, p2

print("AoC 2015\nDay 8\n-----")
t0=time()
p1,p2 = Day08(path)
print("Part 1:",p1)
print("Part 2:",p2,"\nTime:",time()-t0,"\n-----")

del path, t0, p1, p2