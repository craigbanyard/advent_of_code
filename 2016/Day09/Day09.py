from helper import aoc_timer
import re


D = re.compile(r'(\((\d+)x(\d+)\))?(\w+)?')
N = re.compile(r'\d+')


@aoc_timer
def get_input(path):
    return open(path).read().strip()


def decompress(s: str) -> int:
    nums = re.findall(N, s)
    if not nums:
        return len(s)
    if s.startswith('('):
        chars, rep = map(int, nums[:2])
        idx1 = s.find(')') + 1
        idx2 = idx1 + chars
        return decompress(s[idx1:idx2]) * rep + decompress(s[idx2:])


@aoc_timer
def Day09(data):
    p1, p2 = 0, 0
    next_marker = 0
    for match in re.finditer(D, data):
        # Skip empty matches (final match due to ? RegEx token)
        if not match.group():
            continue
        len_seq = match.end(4) - match.start(4)
        chars, rep = map(int, match.group(2, 3))
        if match.start() == next_marker:
            p1 += chars * rep
            idx1 = match.end(1)
            idx2 = idx1 + chars
            p2 += decompress(data[idx1:idx2]) * rep
            next_marker = match.end() + chars - len_seq
    return p1, p2


# %% Output
def main():
    print("AoC 2016\nDay 09")
    data = get_input('input.txt')
    p1, p2 = Day09(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
