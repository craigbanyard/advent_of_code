from helper import aoc_timer
import numpy as np


@aoc_timer
def get_input(path):
    return np.array(
        list(map(int, open(path).read())),
        dtype=int
    )


def fft(signal, base_pattern, offset):
    """Apply one phase of FFT manually."""
    signal_length = len(signal)
    output_signal = np.zeros((signal_length), dtype=int)
    for idx in range(signal_length):
        pattern = base_pattern.repeat(idx + 1)
        pattern = np.resize(pattern, signal_length + offset)[offset:]
        output_signal[idx] = abs(np.sum(pattern * signal)) % 10
    return output_signal


def np_to_int(arr, n):
    """Convert first n digits of arr into base 10 integer."""
    return sum(arr[:n] * 10**np.arange(n)[::-1])


@aoc_timer
def Day16(signal, phases=100, part1=True):
    if part1:
        base_pattern = np.array([0, 1, 0, -1], dtype=int)
        offset = 1
        for _ in range(phases):
            signal = fft(signal, base_pattern, offset)
        return np_to_int(signal, 8)

    # Part 2 - relies on offset being more than halfway through signal.
    # This way we are left with upper-triangular matrix (1 on and above
    # diagonal, 0 elsewhere). Problem then reduced to a cumulative sum.
    offset = np_to_int(signal, 7)
    nrep = 10000
    new_len = len(signal) * nrep
    assert new_len > offset > new_len // 2, "Method will not work!"

    # Trim and reverse signal
    signal = np.tile(signal, nrep)[offset:][::-1]
    for _ in range(phases):
        signal = np.cumsum(signal) % 10
    return np_to_int(signal[::-1], 8)


# %% Output
def main():
    print("AoC 2019\nDay 16")
    data = get_input('input.txt')
    print("Part 1:", Day16(data))
    print("Part 2:", Day16(data, part1=False))


if __name__ == '__main__':
    main()
