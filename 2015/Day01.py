from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day01.txt"

def get_input(path):
    return open(path).read()

def part1(path):
    instr = get_input(path)
    part1 = sum(map(lambda f: 1 if f == '(' else -1, instr))
    print("Part 1:",part1)

def part2(path):
    instr = get_input(path)
    pos = 1
    floor = 0
    for i in instr:
        if i == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            break
        pos += 1
    print("Part 2:",pos)

print("AoC 2015\nDay 1\n-----")
t0=time()
part1(path)
print("Time:",time()-t0,"\n-----")
t0=time()
part2(path)
print("Time:",time()-t0,"\n-----")

del t0, path