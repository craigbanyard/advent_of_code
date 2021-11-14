from helper import aoc_timer
import re
from collections import Counter


@aoc_timer
def get_input(path):
    for line in open(path).readlines():
        yield line.strip()


def decrypt(s, n):
    a = ord('a')
    return ''.join(' ' if c == '-' else
                   chr((ord(c) - a + n) % 26 + a)
                   for c in s)


@aoc_timer
def Day04(data):
    pattern = re.compile(r'([a-z-]+)-(\d+)\[([a-z]+)\]')
    p1 = 0
    p2 = None
    for line in data:
        room, sector, checksum = pattern.search(line).groups()
        counts = Counter(sorted(room.replace('-', ''))).most_common(5)
        if ''.join(x[0] for x in counts) == checksum:
            p1 += int(sector)
            if p2 is None:
                decrypted_room = decrypt(room, int(sector))
                if decrypted_room == 'northpole object storage':
                    p2 = sector
    return p1, p2


# %% Output
def main():
    print("AoC 2016\nDay 04")
    data = get_input('input.txt')
    p1, p2 = Day04(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
