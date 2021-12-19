from helper import aoc_timer
from dataclasses import dataclass
from io import StringIO
from itertools import islice
from math import prod
from operator import gt, lt, eq


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        yield line


TYPE_ID = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    4: None,
    5: lambda args: gt(*args),
    6: lambda args: lt(*args),
    7: lambda args: eq(*args)
}


@dataclass
class Packet:

    version: int
    type_id: int
    value: int | list['Packet']

    def versions(self):
        yield self.version

        if TYPE_ID[self.type_id] is not None:
            for packet in self.value:
                yield from packet.versions()

    def parse(self):
        if TYPE_ID[self.type_id] is None:
            return self.value
        return TYPE_ID[self.type_id](packet.parse() for packet in self.value)


@aoc_timer
def Day16(data):

    def dec(bits: str) -> int:
        return int(bits, 2)

    def decode(stream: StringIO):
        version = dec(stream.read(3) or '0')
        type_id = dec(stream.read(3) or '0')

        if TYPE_ID[type_id] is None:
            value = ''
            while stream.read(1) == '1':
                value += stream.read(4)
            value += stream.read(4)
            yield Packet(
                version,
                type_id,
                dec(value)
            )
        else:
            match stream.read(1):
                case '':
                    return
                case '0':
                    bit_length = dec(stream.read(15))
                    sub_packet = StringIO(stream.read(bit_length))
                    yield Packet(
                        version,
                        type_id,
                        list(decode(sub_packet))
                    )
                case '1':
                    num_packets = dec(stream.read(11))
                    yield Packet(
                        version,
                        type_id,
                        list(islice(decode(stream), num_packets))
                    )

        yield from decode(stream)

    bits = StringIO(bin(int(data, 16))[2:].zfill(len(data) * 4))
    decoded = next(decode(bits))
    p1 = sum(decoded.versions())
    p2 = decoded.parse()

    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 16")
    data = next(get_input('input.txt'))
    p1, p2 = Day16(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
