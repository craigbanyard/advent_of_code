from helper import aoc_timer
import numpy as np
import os
from scipy.ndimage import correlate
import matplotlib.pyplot as plt
import matplotlib.animation as animation


KERNEL = np.array([[0, 2j, 0],
                   [2, 0, 1],
                   [0, 1j, 0]], dtype=complex)


@aoc_timer
def get_input(path):
    G = []
    M = {
        '>': 1,
        'v': 1j,
        '.': 0
    }
    G = np.array([[M[c] for c in line] for line in
                  open(path).read().splitlines()], dtype=complex)
    return G


def ascii_state(G):
    '''Return ASCII-art representation of the grid.'''
    grid = ''
    for r in range(len(G)):
        for c in range(len(G[0])):
            match G[r][c]:
                case 0: grid += '.'
                case 1: grid += '>'
                case 1j: grid += 'v'
                case _: assert False, G[r][c]
        grid += '\n'
    return grid


def plt_init():
    '''Initialise matplotlib plot.'''
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.tick_params(axis='both', which='both', labelsize=0, length=0)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    return fig, ax, []


def plt_vis(grid, t, ims, ax):
    '''Convert complex to int and add state to image list.'''
    grid = grid.copy()
    grid[grid == 1j] = -1
    grid = grid.astype(int)
    label = ax.text(0.5, 1.02, f'Steps: {t}',
                    size=plt.rcParams["axes.titlesize"],
                    ha='center', transform=ax.transAxes,)
    ims.append([plt.imshow(grid, cmap='RdBu'), label])
    return ims


def plt_ani(fig, ims, **kwargs):
    '''Display or save animation, depending on kwargs.'''
    save = kwargs.get('save', False)
    fr = kwargs.get('fr', 30)
    im_ani = animation.ArtistAnimation(
        fig, ims, interval=10, repeat_delay=1000, blit=True)
    if save:
        fname = f'{os.getcwd()}/Outputs/Day25.gif'
        im_ani.save(fname, writer='imagemagick', fps=fr)
    else:
        plt.show()
    return


def step(G: np.ndarray, herd: complex):
    '''Perform one timestep for the given herd (east- or south-facing).'''
    G2 = G.copy()
    if herd == 1:
        nei = correlate(G, KERNEL.real, mode='wrap')
        G2[(G == 0) & (nei.real > 1)] = herd
    else:
        nei = correlate(G, KERNEL.imag, mode='wrap')
        G2[(G == 0) & (nei.imag > 1)] = herd
    G2[(G == herd) & (nei.imag % 2 == 0) & (nei.real % 2 == 0)] = 0
    return G2


@aoc_timer
def Day25(data, **kwargs):
    G = data
    t = 0
    vis = kwargs.pop('vis', False)
    if vis:
        fig, ax, ims = plt_init()
    while True:
        P = G.copy()
        for herd in (1, 1j):
            G = step(G, herd)
        t += 1
        if vis:
            ims = plt_vis(G, t, ims, ax)
        if np.array_equal(P, G):
            if vis:
                plt_ani(fig, ims, **kwargs)
            break
    return t


# %% Output
def main():
    print("AoC 2021\nDay 25")
    data = get_input('input.txt')
    print("Part 1:", Day25(data, vis=False, save=False))


if __name__ == '__main__':
    main()
