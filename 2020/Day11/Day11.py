from helper import aoc_timer
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def disp(grid, R, C):
    """Display ASCII state in console"""
    for r in range(R):
        for c in range(C):
            if (r, c) not in grid:
                print('.', end='')
            elif grid[(r, c)] == 1:
                print('#', end='')
            elif grid[(r, c)] == 0:
                print('L', end='')
        print()
    print()


def plt_init(part, con):
    """Initialise matplotlib plot"""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.tick_params(axis='both', which='both', labelsize=0, length=0)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    plt.title('Part ' + str(part), loc='left')
    plt.title('Constraint: ' + str(con), loc='right')
    return fig, ax, [], 0


def plt_vis(grid, R, C, ims, fig, ax):
    """Visualise state as numpy array and add to image list"""
    state = np.zeros([R, C])
    for r in range(R):
        for c in range(C):
            if (r, c) not in grid:
                state[r, c] = -1
            else:
                state[r, c] = grid[(r, c)]
    label = ax.text(0.5, 1.02, 'Seated: ' + str(sum(grid.values())),
                    size=plt.rcParams["axes.titlesize"],
                    ha='center', transform=ax.transAxes,)
    ims.append([plt.imshow(state, cmap='RdBu'), label])
    return ims


def plt_ani(fig, ims, save, part, con, fr):
    """Display (and save if selected) animation"""
    im_ani = animation.ArtistAnimation(fig, ims, interval=500, repeat_delay=1000, blit=True)
    if save:
        fname = "\\Outputs\\Day11_" + str(part) + "_" + str(con) + ".gif"
        im_ani.save(fname, writer='imagemagick', fps=fr)
    return


@aoc_timer
def Day11(data, part=1, con=3, ani=False, save=False):
    # Process seats (S) and adjacency (A)
    R, C = len(data), len(data[0])
    S, A = {}, {}
    for r in range(R):
        for c in range(C):
            if data[r][c] == 'L':
                tmp = []
                Q = deque([])
                [Q.append([(dr, dc)])
                 for dr in (-1, 0, 1)
                 for dc in (-1, 0, 1)
                 if not (dr == dc == 0)]
                while Q:
                    [(dr, dc)] = Q.popleft()
                    if r + dr in (-1, R) or c + dc in (-1, C):
                        continue
                    if data[r + dr][c + dc] == 'L':
                        tmp.append((r + dr, c + dc))
                    elif part == 2:
                        ddr = dr and (1, -1)[dr < 0]
                        ddc = dc and (1, -1)[dc < 0]
                        Q.append([(dr + ddr, dc + ddc)])
                S[(r, c)] = 0
                A[(r, c)] = tmp

    # Matplotlib animation
    if ani == 'PLT':
        fig, ax, ims, t = plt_init(part, con)

    # Run the simulation until equilibrium
    N = S.copy()
    while True:
        # Visualisation
        if ani == 'ASCII':
            disp(S, R, C)
        if ani == 'PLT':
            if t > 0 and t % 2 == 0:
                ims = plt_vis(S, R, C, ims, fig, ax)
            t += 1
        # Generation
        for seat, occ in S.items():
            tot = 0
            for nei in A[seat]:
                tot += S[nei]
            if not occ and not tot:
                N[seat] = 1
            elif occ and tot > con:
                N[seat] = 0
        if S == N:
            # Equilibrium reached: animate and return
            if ani == 'PLT':
                plt_ani(fig, ims, save, part, con, fr=(t // 4))
            return sum(S.values())
        S = N.copy()
    return


# %% Output
def main():
    print("AoC 2020\nDay 11")
    data = get_input('input.txt')
    print("Part 1:", Day11(data))
    # print("Part 1:", Day11(data, part=1, con=3, ani='PLT', save=True))
    print("Part 2:", Day11(data, part=2, con=4))
    # print("Part 2:", Day11(data, part=2, con=4, ani='PLT', save=True))


if __name__ == '__main__':
    main()
