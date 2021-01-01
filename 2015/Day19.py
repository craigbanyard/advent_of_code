from time import time
from os import getcwd
from collections import deque

def get_input(path):
    return [x.strip() for x in open(path).readlines() if x != '\n']

def Day19(data):
    # Remove medicine from input data into new variable
    medicine = data.pop()
    
    # Parse reactions into dictionary {IN: [*OUT]}
    R = {}
    for react in data:
        IN, OUT = react.split(' => ')
        if IN not in R:
            R[IN] = [OUT]
            continue
        R[IN].append(OUT)
    
    # Process medicine replacements
    M = set()
    for idx, mol in enumerate(medicine):
        # Molecule with length 1
        if mol in R:
            for OUT in R[mol]:
                l, r = medicine[:idx], medicine[idx+1:]
                M.add(l + OUT + r)
        # Molecule with length 2
        mol = medicine[idx:idx+2]
        if mol in R:
            for OUT in R[mol]:
                l, r = medicine[:idx], medicine[idx+2:]
                M.add(l + OUT + r)
    
    return len(M)


def main():
    path = getcwd() + "\\Inputs\\Day19.txt"
    data = get_input(path)
    p1 = Day19(data)
    print(p1)
    
if __name__ == '__main__':
    main()


### Part 2 debugging ###
path = getcwd() + "\\Inputs\\test.txt"
data = get_input(path)

start, end = 'e', data.pop()

# # Parse reactions into dictionary {IN: [*OUT]}
# R = {}
# for react in data:
#     IN, OUT = react.split(' => ')
#     if IN not in R:
#         R[IN] = [OUT]
#         continue
#     R[IN].append(OUT)

# bfs = deque([(start,0,start)])
# visited = {}
# cnt = 0
# while bfs:
#     # DEBUG
#     cnt += 1
#     if cnt % 100000 == 0: print (cnt, OUT)
    
#     mol, steps, route = bfs.popleft()
#     if mol in visited:
#         continue
#     visited[mol] = steps
#     if mol == end:
#         print('Steps:', steps, '\nRoute:', route)
#         break
#     for idx, m in enumerate(mol):
#         # Molecule with length 1
#         if m in R:
#             for OUT in R[m]:
#                 l, r = mol[:idx], mol[idx+1:]
#                 OUT = l + OUT + r
#                 if OUT not in visited:
#                     bfs.append((OUT, steps+1, route + ' => ' + OUT))
#         # Molecule with length 2
#         m = mol[idx:idx+2]
#         if m in R:
#             for OUT in R[m]:
#                 l, r = mol[:idx], mol[idx+2:]
#                 OUT = l + OUT + r
#                 if OUT not in visited:
#                     bfs.append((OUT, steps+1, route + ' => ' + OUT))


# Idea - reverse the dictionary of reactions first
# Process BFS in reverse from that point
R = {}
for react in data:
    OUT, IN = react.split(' => ')
    R[IN] = OUT

bfs = deque([(end, 0, end)])
visited = {}
cnt = 0
while bfs:
    # DEBUG
    cnt += 1
    if cnt % 100000 == 0: print (cnt, m)
    
    mol, steps, route = bfs.popleft()
    if mol in visited:
        continue
    visited[mol] = steps
    if mol == start:
        print('Steps: ', steps, '\nRoute:', route)
        break
    for v in R.keys():
        if v in mol:
            idx = mol.find(v)
            l,r = mol[:idx], mol[idx+len(v):]
            if len(l+r)>0 and R[v] == start:
                continue
            m = l + R[v] + r
            bfs.append((m,steps+1,route + ' => ' + m))
    # for idx, m in enumerate(mol):
    #     if m in R:
    #         l, r = mol[:idx], mol[idx+1:]
    #         m = l + m + r
    #         if m not in visited:
    #             bfs.append((m, steps+1, route + ' => ' + m))
    #     # Molecule with length 2
    #     m = mol[idx:idx+2]
    #     if m in R:
    #         m = R[m]
    #         l, r = mol[:idx], mol[idx+2:]
    #         m = l + m + r
    #         bfs.append((m, steps+1, route + ' => ' + m))
