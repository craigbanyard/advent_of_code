from helper import aoc_timer
from intcode import IntcodeComputer
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


@aoc_timer
def Day15(program_file, grid_init, part1=True, plot=None):

    # Constants
    WALL = 0
    TRAVERSED = 1
    OXYGEN = 2
    DROID = 3
    UNEXPLORED = 4
    CLOCKWISE = {
        1: 4,
        2: 3,
        3: 1,
        4: 2
    }
    ANTICLOCKWISE = {v: k for k, v in CLOCKWISE.items()}
    DR, DC = [None, -1, 1, 0, 0], [None, 0, 0, -1, 1]

    def get_command(movement_command, status_code):
        """Determine next input command, N (1), S (2), W (3), E (4)."""
        if movement_command is None:
            return 1
        if status_code == WALL:
            return ANTICLOCKWISE[movement_command]
        if status_code == TRAVERSED:
            return CLOCKWISE[movement_command]
        else:
            assert status_code == OXYGEN
            return 1

    def get_input():
        """Function used as input to Intcode VM."""
        return movement_command

    def draw_grid(G, style='ascii'):
        """
        Draw a representation of G in a given style.

        Arguments:
          G -- grid to draw
          style -- method of visualisation, two accepted string values:
            'ascii':  ASCII art
            'mpl':    Matplotlib plot
        """

        # ASCII art mapping
        ASCII = {
            WALL: "#",
            TRAVERSED: ".",
            OXYGEN: "O",
            DROID: "D",
            UNEXPLORED: " "
        }

        # Draw ASCII art
        if style.lower() == 'ascii':
            grid = "\n"
            for r in G:
                for c in r:
                    grid += ASCII[c]
                grid += "\n"
            print(grid)
            return None

        # Matplotlib plot
        assert style.lower() == 'mpl', f"Invalid plot style: {style}"
        plt.figure(figsize=(8, 8))
        cmap = ListedColormap([
            'xkcd:dark indigo',        # Walls
            'white',                   # Traversed
            'crimson',                 # Oxygen
            'xkcd:azure',              # Droid
            'black'                    # Unexplored
        ])
        plt.imshow(G, cmap=cmap)
        plt.axis('off')
        return None

    # Initialise grid
    R, C = grid_init
    r = r0 = R // 2 + 1
    c = c0 = (C // 2) + 1
    G = [[UNEXPLORED for _ in range(C)] for _ in range(R)]
    G[r][c] = DROID
    movement_command = None
    status_code = None
    commands = 0
    visited = {(r0, c0): commands}
    # Part 2
    longest = 0
    oxygen_found = False
    oxygen_path = {}

    # Initialise Intcode program
    VM = IntcodeComputer(program_file, input=get_input)

    while not VM.halted:
        movement_command = get_command(movement_command, status_code)
        dr, dc = DR[movement_command], DC[movement_command]
        status_code = VM.run()
        # Process output
        if status_code == WALL:
            # Hit a wall, droid cannot move in given direction
            G[r + dr][c + dc] = WALL
            continue
        # Droid successfully moved in the given direction
        if G[r][c] != OXYGEN:
            G[r][c] = TRAVERSED
        r += dr
        c += dc
        # Update visited
        if (r, c) not in visited:
            commands += 1
            visited[(r, c)] = commands
        else:
            # Backtracking after hitting dead-end
            commands -= 1
        # Update oxygen path
        if oxygen_found and (r, c) not in oxygen_path:
            longest += 1
            oxygen_path[(r, c)] = longest
        elif oxygen_found:
            longest -= 1
        # Successful movement status codes
        if status_code == OXYGEN:
            G[r][c] = OXYGEN
            if part1:
                if plot:
                    G[r0][c0] = DROID
                    draw_grid(G, style=plot)
                return commands
            oxygen_found = True
        else:
            assert status_code == TRAVERSED
            G[r][c] = DROID
        # Halt if we're back at the starting position
        if (r, c) == (r0, c0):
            break

    if plot:
        draw_grid(G, style=plot)
    return max(oxygen_path.values())


# %% Output
def main():
    print("AoC 2019\nDay 15")
    program_file = 'input.txt'
    grid_dimensions = (43, 43)
    print("Part 1:", Day15(program_file, grid_dimensions, plot='mpl'))
    print("Part 2:", Day15(program_file, grid_dimensions, part1=False, plot='mpl'))


if __name__ == '__main__':
    main()
