from time import time

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day07.txt"

def get_input(path):
    return [list(map(to_int, x.strip().replace(' -> ',' ').split())) for x in open(path).readlines()]

def to_int(s):
    try:
        num = int(s)
    except ValueError:
        return s
    return num

def Day07(path,wire,override=False,oWire=False,oVal=False):
    # Gates
    G = {
        None: lambda x: x,
        'AND': lambda x, y: x & y,
        'OR': lambda x, y: x | y,
        'NOT': lambda x: ~ x & 0xFFFF,
        'LSHIFT': lambda x, y: x << y,
        'RSHIFT': lambda x, y: x >> y
        }
    
    instr = get_input(path)
    W = {}
    # Override a wire with a signal (for part 2)
    if override:
        W[oWire] = oVal
    # Main code
    while wire not in W:
        for line in instr:
            # A wire can receive only one signal
            dest = line[-1]
            if dest in W:
                continue
            # Signal given to a wire
            if len(line) == 2:
                signal, dest = line
                if isinstance(signal, int):
                    W[dest] = signal
                    continue
                if signal not in W:
                    continue
                W[dest] = W[signal]
                continue
            # 'NOT' gate
            if len(line) == 3:
                g, source, dest = line
                if isinstance(source, int):
                    W[dest] = G[g](source)
                    continue
                if source not in W:
                    continue
                W[dest] = G[g](W[source])
                continue
            # Other gate
            s1, g, s2, dest = line
            if s1 not in W:
                if isinstance(s1, int):
                    W[s1] = s1
                else:
                    continue
            if s2 not in W:
                if isinstance(s2, int):
                    W[s2] = s2
                else:
                    continue
            W[dest] = G[g](W[s1],W[s2])
    return W[wire]


print("AoC 2015\nDay 7\n-----")
t0=time()
part1=Day07(path,'a')
print("Part 1:",part1)
print("Time:",time()-t0,"\n-----")
t0=time()
part2=Day07(path,'a',True,'b',part1)
print("Part 1:",part2)
print("Time:",time()-t0,"\n-----")

del t0, part1, part2

# %% Prettier code but slower

def get_args(instr):
    instr = instr.split()
    G = ['AND', 'OR', 'NOT', 'LSHIFT', 'RSHIFT']
    gate = next((x for x in instr if x in G), None)
    args = [to_int(x) for x in instr if x != gate]
    return gate, args

def get_signal(path,wire,override=False,oWire=False,oVal=False):
    G = {
        None: lambda x: x[0],
        'AND': lambda x: x[0] & x[1],
        'OR': lambda x: x[0] | x[1],
        'NOT': lambda x: ~ x[0] & 0xFFFF,
        'LSHIFT': lambda x: x[0] << x[1],
        'RSHIFT': lambda x: x[0] >> x[1]
        }
    instr = [x.strip().split(' -> ') for x in open(path).readlines()]
    W = {}
    if override:
        W[oWire] = oVal
    while wire not in W:
        for line in instr:
            cmd, dest = line
            if dest in W:
                continue
            gate, args = get_args(cmd)
            for idx, x in enumerate(args):
                if isinstance(x, int):
                    continue
                try:
                    args[idx] = W[x]
                except KeyError:
                    args = None
                    break
            if args is not None:
                W[dest] = G[gate](args)
    return W[wire]

del path