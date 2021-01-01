from time import time
from itertools import groupby

# BRUTE FORCE
def get_next(n):
    n = str(n)
    look, counter, say = n[0], 1, ''
    for d in n[1:]:
        if look == d:
            counter += 1
            continue
        say += str(counter) + look
        counter = 1
        look = d
    return say + str(counter) + look

# GROUP BY, SLOW ONE-LINER
def look_and_say(seed):
    return ''.join([(str(len([1 for _ in g]))+k) for k,g in groupby(seed)])

# DRIVING CODE
def Day10(seed,steps):
    for s in range(steps):
        # UGLY FAST
        seed = get_next(seed)
        # SEXY SLOW
        # seed = look_and_say(seed)
    return(len(seed))

seed = '1113122113'
print("AoC 2015\nDay 10\n-----")
t0=time()
print("Part 1:",Day10(seed,40))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",Day10(seed,50))
print("Time:",time()-t0,"\n-----")

del t0, seed