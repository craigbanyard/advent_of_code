from collections import deque, defaultdict, OrderedDict
import re
import random
from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines() if x != '\n']


def get_reactions(data, reverse=False):
    if not reverse:
        # Parse reactions into dictionary {IN: [*OUT]}
        R = defaultdict(list)
        for react in data:
            IN, OUT = react.split(' => ')
            R[IN].append(OUT)
    else:
        # Reactions in reverse
        R = {}
        for react in data:
            OUT, IN = react.split(' => ')
            R[IN] = OUT
        # Sort by length of RHS molecule
        R = OrderedDict(sorted(R.items(), key=lambda x: len(x[0]), reverse=True))
    return R


def shuffle_dict(d):
    items = list(d.items())
    random.shuffle(items)
    return OrderedDict(items)


def repl_all(s, mol, repl):
    """Replace each occurrence of mol in s with repl.
       Return set of all possible single replacements.
    """
    inds = [m.start() for m in re.finditer(f'(?={mol})', s)]
    if not inds:
        return {}
    out = set()
    chars = len(mol)
    for idx in inds:
        pre, post = s[:idx], s[idx+chars:]
        out.add(pre + repl + post)
    return out


def repl_greedy(s, mol, repl):
    """Replace all occurrences of mol in s with repl.
       Return reduced string and count of replacements.
    """
    cnt = 0
    while mol in s:
        s = s.replace(mol, repl, 1)
        cnt += 1
    return s, cnt


@aoc_timer
def part1(replacements, medicine):
    R = get_reactions(replacements)
    M = set()
    for k, v in R.items():
        for mol in v:
            M = M.union(repl_all(medicine, k, mol))
    return len(M)


@aoc_timer
def part2(replacements, medicine, output=False):
    # Reactions in reverse
    R = get_reactions(replacements, reverse=True)

    # BFS with greedy replacements, retry with random shuffle if residual remains
    while True:
        start, end = 'e', medicine
        bfs = deque([(end, 0, end)])
        visited = {medicine: 0}
        while bfs:
            mol, steps, route = bfs.popleft()
            for k, v in R.items():
                if k not in mol:
                    continue
                mol, _steps = repl_greedy(mol, k, v)
                steps += _steps
                if mol in visited and visited[mol] <= steps:
                    continue
                visited[mol] = steps
                bfs.append((mol, steps, route + ' =>\n' + mol))
                break  # Always retry from beginning after making successful reductions
        if start in visited:
            break  # Found solution
        if output:
            print(f'NOT FOUND!\nsteps: {steps}, residual: {mol}' +
                  '\nRetrying with shuffled reactions...\n')
        R = shuffle_dict(R)
    if output:
        print(f'route: {route}, steps: {visited[start]}')
    return visited[start]


# %% Output
def main():
    print("AoC 2015\nDay 19")
    replacements = get_input('input.txt')
    medicine = replacements.pop()
    print("Part 1:", part1(replacements, medicine))
    print("Part 2:", part2(replacements, medicine, False))


if __name__ == '__main__':
    main()
