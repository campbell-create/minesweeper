import numpy as np
import random

BOMB = -1
UNREVEALED = -2
FLAG = -3

def make_grid(x=16, y=16, n_bombs=40):
    """makes a grid with dimensions x,y and with a number of randomly-located
    bombs (n_bombs)"""

    ra = np.zeros((x,y), dtype=int)
    options = [(a,b) for a in range(0, x) for b in range(0,y)]

    sample = random.sample(options, n_bombs)
    for item in sample:
        ra[item] = BOMB

    for a in range(x):
        for b in range(y):
            s = 0
            if ra[a, b] == BOMB:
                continue
            for aa in [-1, 0, 1]:
                for bb in [-1, 0, 1]:
                    if 0<=a-aa<x and 0<=b-bb<y:
                        if ra[a-aa, b-bb] == -1:
                            s += 1
            ra[a,b] = s

    return ra

def print_grid(grid):
    size = grid.shape
    s1 = "     "
    s2 = "    "
    for i in range(size[1]):
        s1 += f"{str(i).ljust(2, ' ')} "
        s2 += f"{'-'*2}-"
    print(s1)
    print(s2)
    for i in range(size[0]):
        s = f"{str(i).ljust(3, ' ')}| "
        for j in range(size[1]):
            if grid[i,j] == UNREVEALED:
                x = "╬"
            elif grid[i,j] == FLAG:
                x = "@"
            else:
                x = str(grid[i,j])
            x = x.ljust(2, " ")
            s += x + " "
        print(s)
    print()


def reveal_tile(x, y, grid, visible_grid):
    if grid[x,y] == 0:
        if visible_grid[x,y] == 0:
            return
        # reveal grid
        visible_grid[x,y] = grid[x,y]
        print_grid(visible_grid)

        # also recursively reveal all adjacent tiles
        for aa in [-1, 0, 1]:
            for bb in [-1, 0, 1]:
                if aa == 0 and bb == 0:
                    continue
                if 0 <= x-aa < grid.shape[0] and 0 <= y-bb < grid.shape[1]:
                    reveal_tile(x-aa, y-bb, grid, visible_grid)
    elif grid[x,y] == BOMB:
        # end game
        raise Exception("You revealed a bomb! DEATH")
    else:
        # reveal grid
        visible_grid[x,y] = grid[x,y]

def game_running(vis_grid, num_bombs):
    bombed = False
    revealed_count = 0
    flagged_count = 0
    for a in range(vis_grid.shape[0]):
        for b in range(vis_grid.shape[1]):
            if vis_grid[a,b] == BOMB:
                bombed = True
                break
            elif vis_grid[a,b] != UNREVEALED and vis_grid[a,b] != FLAG:
                revealed_count += 1
            elif vis_grid[a,b] == FLAG:
                flagged_count += 1
    if bombed:
        print("You died")
        return False
    else:
        clear = vis_grid.shape[0]*vis_grid.shape[1] - num_bombs
        print(f"revealed count: {revealed_count} vs total clear: {clear}")
        print(f"flag count: {flagged_count} vs total bombs: {num_bombs}")
        if revealed_count == clear or flagged_count == num_bombs:
            print("you won!")
            return False
    return True


### Solver functions ###

def is_full(vis, x, y):
    """if there are n bombs surrounding a tile, and n unrevealed/marked tiles,
    mark them all bombs"""
    count = 0
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if 0 <= x+a < vis.shape[0] and 0 <= y+b < vis.shape[1]:
                curr = vis[x+a, y+b]
                if curr == UNREVEALED or curr == FLAG:
                    count += 1
    if count == vis[x,y] and count > 0:
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if 0 <= x+a < vis.shape[0] and 0 <= y+b < vis.shape[1]:
                    if vis[x+a, y+b] == UNREVEALED:
                        vis[x+a, y+b] = FLAG


def if_full_then_clear(vis, x, y):
    if vis[x,y] < 0:
        return None
    flag_count = 0
    unrev_spot = None
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if 0 <= x+a < vis.shape[0] and 0 <= y+b < vis.shape[1]:
                if vis[x+a, y+b] == FLAG:
                    flag_count += 1
                if vis[x+a, y+b] == UNREVEALED:
                    unrev_spot = (x+a, y+b)
    print(f"Vis[{x}, {y}] = {vis[x,y]}, flag count = {flag_count}")
    if vis[x,y] == flag_count and vis[x,y] != 0 and unrev_spot is not None and vis[unrev_spot[0], unrev_spot[1]] == UNREVEALED:
        print(f"returning {unrev_spot}")
        return unrev_spot


def solve(vis):
    for x in range(vis.shape[0]):
        for y in range(vis.shape[1]):
            is_full(vis, x,y)
    print_grid(vis)
    for x in range(vis.shape[0]):
        for y in range(vis.shape[1]):
            next_move = if_full_then_clear(vis, x, y)
            if next_move:
                return next_move
    for x in range(vis.shape[0]):
        for y in range(vis.shape[1]):
            next_move = if_full_then_clear(vis, x, y)

### run the shit ###


n_bombs = 40
size = 16
grid = make_grid(size, size, n_bombs)
visible_grid = np.zeros(grid.shape, dtype=int) + UNREVEALED

while game_running(visible_grid, n_bombs):
    move = input("Provide next move:")
    move = move.split(",")

    reveal_tile(int(move[0]), int(move[1]), grid, visible_grid)
    print_grid(visible_grid)

    print("\n\nAutosolving...")

    next_move = solve(visible_grid)
    while next_move:
        reveal_tile(next_move[0], next_move[1], grid, visible_grid)
        print_grid(visible_grid)
        print("getting next move...")
        next_move = solve(visible_grid)
    print_grid(visible_grid)


