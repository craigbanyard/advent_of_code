from helper import aoc_timer
import numpy as np
import matplotlib.pyplot as plt


@aoc_timer
def get_input(path):
    return open(path).read()


@aoc_timer
def Day08(data, part1=True, plot_ascii=True):
    # Parse input into numpy array
    x, y = 25, 6
    z = len(data) // (x * y)
    img = np.zeros([z, y, x], dtype=int)
    i = 0
    for layer in range(z):
        for r in range(y):
            for c in range(x):
                img[layer, r, c] = data[i]
                i += 1

    # Calculate checksum
    if part1:
        zeros = np.sum(img == 0, axis=(1, 2))
        check_layer = img[np.where(zeros == min(zeros))]
        return np.sum(check_layer == 1) * np.sum(check_layer == 2)

    # Decode image
    msg = "\n"
    final_img = np.full((y, x), 2)
    for r in range(y):
        for c in range(x):
            for layer in range(z):
                if img[layer, r, c] != 2:
                    final_img[r, c] = img[layer, r, c]
                    if final_img[r, c] == 0:
                        msg += ' '
                    else:
                        msg += '#'
                    break
        msg += '\n'

    if plot_ascii:
        return msg

    # Matplotlib plot
    plt.figure("Part 2")
    plt.imshow(final_img, cmap='gray')
    plt.axis('off')
    return ""


# %% Output
def main():
    print("AoC 2019\nDay 08")
    data = get_input('input.txt')
    print("Part 1:", Day08(data))
    print("Part 2:", Day08(data, part1=False, plot_ascii=True))


if __name__ == '__main__':
    main()
