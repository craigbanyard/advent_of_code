from time import time
from collections import defaultdict

# %% Part 1 functions

# Get adjacent bugs for each position in grid
def adj_bugs(state):
    R,C = 5,5
    bugs = [[0 for _ in range (C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            for dr, dc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                if 0 <= dr < R and 0 <= dc < C:
                    # Inside grid
                    if state[dr][dc] == '#':
                        bugs[r][c] += 1
    return bugs

# Update the grid based on adjacency matrix
def update_state(state):
    R,C = 5,5
    bugs = adj_bugs(state)
    newstate = [[] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if state[r][c] == '#':
                if bugs[r][c] == 1:
                    newstate[r] += '#'
                else:
                    newstate[r] += '.'
            elif state[r][c] == '.':
                if 1 <= bugs[r][c] <= 2:
                    newstate[r] += '#'
                else:
                    newstate[r] += '.'
        newstate[r] = ''.join(newstate[r])
    return newstate

# Print states to screen
def print_states(init_state, minutes=0):
    # Print initial state
    for line in init_state:
        for ch in line:
            print(ch, end='')
        print()
    print("------")
    # Print subsequent states
    for i in range(minutes):
        init_state = update_state(init_state)
        for line in init_state:
            for ch in line:
                print(ch, end='')
            print()
        print("------")

# Convert a given raw state (# and .) to binary
def to_binary(state):
    tmp = ''.join([i[::-1] for i in state[::-1]])
    return ''.join(['1' if i == '#' else '0' for i in tmp])

# Convert raw state to biodiversity rating
def bio(state):
    return int(to_binary(state),2)


# %% Part 2 functions

#####################################
#  Example grid                     #
#####################################
#      |     |         |     |      #
#   1  |  2  |    3    |  4  |  5   #
#      |     |         |     |      #
# -----+-----+---------+-----+----- #
#      |     |         |     |      #
#   6  |  7  |    8    |  9  |  10  #
#      |     |         |     |      #
# -----+-----+---------+-----+----- #
#      |     |A|B|C|D|E|     |      #
#      |     |-+-+-+-+-|     |      #
#      |     |F|G|H|I|J|     |      #
#      |     |-+-+-+-+-|     |      #
#  11  | 12  |K|L|?|N|O|  14 |  15  #
#      |     |-+-+-+-+-|     |      #
#      |     |P|Q|R|S|T|     |      #
#      |     |-+-+-+-+-|     |      #
#      |     |U|V|W|X|Y|     |      #
# -----+-----+---------+-----+----- #
#      |     |         |     |      #
#  16  | 17  |    18   |  19 |  20  #
#      |     |         |     |      #
# -----+-----+---------+-----+----- #
#      |     |         |     |      #
#  21  | 22  |    23   |  24 |  25  #
#      |     |         |     |      #
#####################################

# Function to return all adjacent tiles at inner and outer depths
def get_adj_tiles(tile,depth):
    R,C = 5,5
    r,c = tile
    adj = defaultdict(list)
    # Centre tile - return empty
    if r == c == 2:
        return adj
    # Outer adjacencies
    if r == 0:
        adj[depth-1] += [(1,2)]  # Up
    if r == R-1:
        adj[depth-1] += [(3,2)]  # Down
    if c == 0:
        adj[depth-1] += [(2,1)]  # Left
    if c == C-1:
        adj[depth-1] += [(2,3)]  # Right
    # Inner adjacencies
    if tile == (1,2):  # Up
        for x in range(C):
            adj[depth+1] += [(0,x)]
    if tile == (3,2):  # Down
        for x in range(C):
            adj[depth+1] += [(C-1,x)]
    if tile == (2,1):  # Left
        for y in range(R):
            adj[depth+1] += [(y,0)]
    if tile == (2,3):  # Right
        for y in range(R):
            adj[depth+1] += [(y,R-1)]
    # Current depth adjacencies
    for dr, dc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= dr < R and 0 <= dc < C:
            if (dr,dc) != (2,2):
                adj[depth] += [(dr,dc)]
    return adj

# Cycle adjacent tiles and increment bug counts
def adj_bugs_rec(states):
    R,C = 5,5
    bugs = {}
    depths = sorted(states)
    # Only add a new outer depth if the current minimum depth is not empty
    if bio(states[min(states)]) > 0:
        states[min(states)-1] = ['.' * C for _ in range(R)]
    # Only add a new inner depth if the current maximum depth is not empty
    if bio(states[max(states)]) > 0:
        states[max(states)+1] = ['.' * C for _ in range(R)]
    # Iterate innermost depths, i.e. not including any newly added depths
    for depth in depths:
        # Create bugs for inner and outer depths if they don't already exist
        for d in [depth-1,depth,depth+1]:
            if d not in bugs:
                bugs[d] = [[0 for _ in range(C)] for _ in range(R)]
        # Cycle every tile in current depth, add adjacencies for surrounding depths
        for r in range(R):
            for c in range(C):
                adjs = get_adj_tiles((r,c),depth)
                for d in adjs:
                    if d == depth:
                        for rr,cc in adjs[d]:
                            bugs[depth][r][c] += 1 if states[d][rr][cc] == '#' else 0
                    elif d != depth:
                        for rr,cc in adjs[d]:
                            bugs[d][rr][cc] += 1 if states[depth][r][c] == '#' else 0
    return bugs

# Apply adjacency matrices to all recursion levels
def update_state_rec(states):
    R,C = 5,5
    bugs = adj_bugs_rec(states)
    depths = sorted(states)
    newstates = {}
    for d in depths:
        newstates[d] = [[] for _ in range(R)]
    for depth in depths:
        for r in range(R):
            for c in range(C):
                if states[depth][r][c] == '#':
                    if bugs[depth][r][c] == 1:
                        newstates[depth][r] += '#'
                    else:
                        newstates[depth][r] += '.'
                elif states[depth][r][c] == '.':
                    if bugs[depth][r][c] in [1,2]:
                        newstates[depth][r] += '#'
                    else:
                        newstates[depth][r] += '.'
            newstates[depth][r] = ''.join(newstates[depth][r])
    # If an outer state is empty, remove it
    if bio(newstates[min(depths)]) == 0:
        del newstates[min(depths)]
    if bio(newstates[max(depths)]) == 0:
        del newstates[max(depths)]
    return newstates


# %% Day 24
path = "F:\\Users\\Craig\\Documents\\Programming\\R\\Advent of Code\\Inputs\\Day24.txt"

def part1(path, verbose=False):
    # Get starting state
    grid = [line.strip() for line in open(path).readlines()]
    start_state = bio(grid)
    states = set()
    states.add(start_state)
    part1 = False
    if verbose: print_states(grid)
    # Increment time until repeated state
    while True:
        grid = update_state(grid)
        if verbose: print_states(grid)
        biodev = bio(grid)
        if biodev in states:
            print("Part 1:",biodev)
            part1 = True
            break
        states.add(biodev)
        if part1: break

def part2(path, verbose=False):
    # Get starting state
    grid = [line.strip() for line in open(path).readlines()] 
    s = {}
    s[0] = grid
    minutes = 200
    # Increment time
    for t in range(minutes):
        s = update_state_rec(s)
    # Verbose print of depths
    if verbose:
        for d in sorted(s):
            print("Depth",d,":")
            for r in range(5):
                for c in range(5):
                    print(s[d][r][c],end='')
                print()
            print()
    # Count all bugs over all recursion levels
    part2 = sum(1 for grid in s.values()
                for line in grid
                for ch in line if ch == '#')
    print("Part 2:",part2)


print("Day 24")
print("------")
t0=time()
part1(path)
print("Time:",time()-t0)
print("------")
t0=time()
part2(path)
print("Time:",time()-t0)
print("------")

del t0, path