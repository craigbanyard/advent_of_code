from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day03.txt"

def get_input(path):
    return open(path).read()

def move(d):
    dirs = {
        '^': (0,1),
        'v': (0,-1),
        '>': (1,0),
        '<': (-1,0)
    }
    return(dirs[d])

def part1(path):
    dirs = get_input(path)
    # Starting point
    x,y = 0,0
    # Visited houses
    visited = {(x,y)}
    for d in dirs:
        dx,dy = move(d)
        x+=dx
        y+=dy
        visited.add((x,y))
    print("Part 1:",len(visited))

def part2(path):
    dirs = get_input(path)
    # Starting points
    xS,xR,yS,yR = 0,0,0,0
    # Visited houses
    visited = {(xS,yS)}
    # Take pairwise directions
    for S,R in zip(dirs[0::2], dirs[1::2]):
        # Santa
        dxS,dyS = move(S)
        xS+=dxS
        yS+=dyS
        visited.add((xS,yS))
        # Robo-Santa
        dxR,dyR = move(R)
        xR+=dxR
        yR+=dyR
        visited.add((xR,yR))
    print("Part 2:",len(visited))

print("AoC 2015\nDay 3\n-----")
t0=time()
part1(path)
print("Time:",time()-t0,"\n-----")
t0=time()
part2(path)
print("Time:",time()-t0,"\n-----")

del t0, path