from helper import aoc_timer
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from scipy.ndimage import correlate


KERNEL = np.array([[0, 2j, 0],
                   [2, 0, 1],
                   [0, 1j, 0]], dtype=complex)


class Visualisation:

    def __init__(self, **kwargs) -> None:
        self.vis = kwargs.get('vis', False)
        if not self.vis:
            return
        # Initial figure
        self.fig, self.ax = plt.subplots(figsize=kwargs.get('figsize', (7, 7)))
        self.ax.tick_params(axis='both', which='both', labelsize=0, length=0)
        for axis in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[axis].set_linewidth(2)
        # Frames
        self.ims = []
        default_colours = mpl.colors.ListedColormap(
            ['darkgreen', 'midnightblue', 'seagreen']
        )
        self.colours = kwargs.get('colours', default_colours)
        # Animation
        self.save = kwargs.get('save', False)
        self.fr = kwargs.get('fr', 30)
        default_filename = f'{os.getcwd()}/Outputs/{self.fr}FPS/Day25.gif'
        self.fname = kwargs.get('filename', default_filename)
        self.interval = kwargs.get('interval', 10)
        self.repeat_delay = kwargs.get('repeat_delay', 1000)
        self.blit = kwargs.get('blit', True)

    def snapshot(self, grid, t, num_frames=1) -> None:
        '''Convert complex to int and add state to image list.'''
        if not self.vis:
            return
        newgrid = np.zeros_like(grid, dtype=int)
        newgrid[grid == 1] = 1
        newgrid[grid == 1j] = -1
        label = self.ax.text(
            0.5, 1.02, f'Steps: {t}',
            size=plt.rcParams["axes.titlesize"],
            ha='center', transform=self.ax.transAxes,
        )
        frames = [plt.imshow(newgrid, cmap=self.colours), label] * num_frames
        self.ims.append(frames)
        return

    def animate(self) -> None:
        '''Display or save animation.'''
        if not self.vis:
            return
        im_ani = animation.ArtistAnimation(
            self.fig,
            self.ims,
            interval=self.interval,
            repeat_delay=self.repeat_delay,
            blit=self.blit
        )
        if self.save:
            im_ani.save(self.fname, writer='imagemagick', fps=self.fr)
        else:
            plt.show()
        return

    def ascii_state(self, grid) -> None:
        '''Print ASCII-art representation of the grid.'''
        state = ''
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                match grid[r][c]:
                    case 0: state += '.'
                    case 1: state += '>'
                    case 1j: state += 'v'
                    case _: assert False, grid[r][c]
            state += '\n'
        print(state)
        return


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
    v = Visualisation(**kwargs)
    while True:
        P = G.copy()
        for herd in (1, 1j):
            G = step(G, herd)
        t += 1
        v.snapshot(G, t)
        if np.array_equal(P, G):
            v.animate()
            break
    return t


# %% Output
def main():
    print("AoC 2021\nDay 25")
    data = get_input('input.txt')
    print("Part 1:", Day25(data, vis=False, save=False))


if __name__ == '__main__':
    main()
