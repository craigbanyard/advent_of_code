from time import time
from functools import reduce
from matplotlib import pyplot as plt

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day06.txt"

def get_input(path):
    # Dictionary for string replacement
    d = {
        'turn on': 'on',
        'turn off': 'off',
        'through': ' ',
        ',': ' '
        }
    
    return [list(map(to_int, reduce(lambda s, kv: s.strip().replace(*kv), d.items(), s).split()))
         for s in open(path).readlines()]

def to_int(s):
    try:
        num = int(s)
    except ValueError:
        return s
    return num

def part1(path, plot):
    instr = get_input(path)
    R,C = 1000,1000
    G = [[0 for _ in range(C)] for _ in range(R)]
    for op, x1, y1, x2, y2 in instr:
        cols = range(x1,x2+1)
        rows = range(y1,y2+1)
        # op on outside loop - fewer operations
        if op == 'on':
            for c in cols:
                for r in rows:
                    G[r][c] = 1
        elif op == 'off':
            for c in cols:
                for r in rows:
                    G[r][c] = 0
        elif op == 'toggle':
            for c in cols:
                for r in rows:
                    G[r][c] ^= 1

    on = sum(map(sum,G))
    print("Part 1:",on)
    
    # Matplotlib plot
    if plot:
        plt.figure("Part 1")
        plt.imshow(G, cmap='Greys')
        plt.axis('off')

def part2(path, plot):
    instr = get_input(path)
    R,C = 1000,1000
    G = [[0 for _ in range(C)] for _ in range(R)]
    for op, x1, y1, x2, y2 in instr:
        # 'off' op depends on current value, have to swap order of loop compared to part 1 - slower
        for c in range(x1,x2+1):
            for r in range(y1,y2+1):
                if op == 'on':
                    G[r][c] += 1
                elif op == 'off' and G[r][c] > 0:
                    G[r][c] -= 1
                elif op == 'toggle':
                    G[r][c] += 2
    
    brightness = sum(map(sum,G))
    print("Part 2:",brightness)
    
    # Matplotlib plot
    if plot:
        plt.figure("Part 2")
        plt.imshow(G, cmap='viridis')
        #plt.imshow(G, cmap='twilight')
        #plt.imshow(G, cmap='twilight_shifted')
        plt.axis('off')


print("AoC 2015\nDay 6\n-----")
t0=time()
part1(path,True)
print("Time:",time()-t0,"\n-----")
t0=time()
part2(path,True)
print("Time:",time()-t0,"\n-----")

del t0, path

# # %% Prettier but slower code
# path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day06.txt"

# def part1(path, plot):
#     # Light operations
#     ops = {
#         'on': lambda x: 1,
#         'off': lambda x: 0,
#         'toggle': lambda x: 1-x
#         }
    
#     instr = get_input(path)
#     R,C = 1000,1000
#     G = [[0 for _ in range(C)] for _ in range(R)]
#     for op, x1, y1, x2, y2 in instr:
#         for c in range(x1,x2+1):
#             for r in range(y1,y2+1):
#                 G[r][c] = ops[op](G[r][c])
    
#     on = sum(map(sum,G))
#     print("Part 1:",on)
    
#     # Matplotlib plot
#     if plot:
#         plt.figure("Part 1")
#         plt.imshow(G, cmap='gist_stern')
#         plt.axis('off')

# def part2(path, plot):
#     # Light operations
#     ops = {
#         'on': lambda x: x+1,
#         'off': lambda x: x-1 if x > 0 else 0,
#         'toggle': lambda x: x+2
#         }
    
#     instr = get_input(path)
#     R,C = 1000,1000
#     G = [[0 for _ in range(C)] for _ in range(R)]
#     for op, x1, y1, x2, y2 in instr:
#         for c in range(x1,x2+1):
#             for r in range(y1,y2+1):
#                 G[r][c] = ops[op](G[r][c])
    
#     on = sum(map(sum,G))
#     print("Part 1:",on)
    
#     # Matplotlib plot
#     if plot:
#         plt.figure("Part 1")
#         plt.imshow(G, cmap='gist_stern')
#         plt.axis('off')

# print("AoC 2015\nDay 6\n-----")
# t0=time()
# part1(path,False)
# print("Time:",time()-t0,"\n-----")
# t0=time()
# part2(path,False)
# print("Time:",time()-t0,"\n-----")

# del t0, path