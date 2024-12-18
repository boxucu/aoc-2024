from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    i: int
    j: int
    score: int
    fromi: int
    fromj: int


# based on current tile (i, j, score, fromi, fromj) give the set of possible next tiles
def find_next_tile(tile, map):
    (i, j, score) = (tile.i, tile.j, tile.score)

    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]  # direct 0 - ">", 1 - "^", 2 - "<", 3 - "v"

    nextstep_set = set()
    for next_direct in range(0, 4):
        (di, dj) = didj[next_direct]
        if i + di < 0 or i + di >= len(map) or j + dj < 0 or j + dj >= len(map[0]):
            pass
        elif map[i + di][j + dj] != "#":
            nextstep_set.add(Tile(i + di, j + dj, score + 1, i, j))

    return nextstep_set


# based on the current frontier set of tiles, expand to new frontier with the lowest increase in score
def update_frontier(frontier_set, visited_set, i_end, j_end, map):
    # first, choose the tile within the frontier_set that has the smallest score
    lowest_score = 10**10
    for tile in frontier_set:
        score = tile.score
        if score < lowest_score:
            lowest_score = score
            replaced_tile = tile

    # then remove the lowset score tile from frontier_set
    frontier_set.remove(replaced_tile)

    # find the set of next step tiles for this replaced tile
    nextstep_set = find_next_tile(replaced_tile, map)

    # visited (i,j) spots
    visited_ij_set = set()
    for visited_tile in visited_set:
        visited_ij_set.add(tuple([visited_tile.i, visited_tile.j]))

    new_step_set = set()
    for tile in nextstep_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        # if next step is not already visited, add
        if (i, j) not in visited_ij_set:
            new_step_set.add(tile)
        # if the next step lead us to a visited spot but now with a <= score, add
        else:
            # find the visited score of (i, j)
            for visited_tile in visited_set:
                (visited_i, visited_j) = (visited_tile.i, visited_tile.j)
                if (visited_i, visited_j) == (i, j):
                    visited_score = visited_tile.score
            if score < visited_score:
                new_step_set.add(tile)

    # if there's not more new steps from this tile, remove this tile is the end of update
    if len(new_step_set) == 0:
        return frontier_set, visited_set
    else:
        for tile in new_step_set:
            (i, j) = (tile.i, tile.j)
            # if this step is the end of the maze, don't add to frontier
            if (i, j) == (i_end, j_end):
                visited_set.add(tile)
            # else, add to frontier
            else:
                frontier_set.add(tile)
                visited_set.add(tile)
        return frontier_set, visited_set


def maze_solvable(map):
    (i_start, j_start) = (0, 0)
    (i_end, j_end) = (len(map) - 1, len(map[0]) - 1)

    visited_set = set()
    visited_set.add(Tile(i_start, j_start, 0, i_start, j_start))
    frontier_set = visited_set.copy()

    step = 0
    while True:
        step += 1
        frontier_set, visited_set = update_frontier(
            frontier_set, visited_set, i_end, j_end, map
        )

        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    # if (i_end, j_end) not in the visited_set, maze is not solvable
    solvable = False
    for tile in visited_set:
        (i, j) = (tile.i, tile.j)
        if (i, j) == (i_end, j_end):
            solvable = True

    return solvable


def map_view(map):
    for line in map:
        print(line)


def corrupted_map(Nx, Ny, corrupted_bytes):
    map = []
    for y in range(0, Ny):
        line = []
        for x in range(0, Nx):
            if (x, y) in corrupted_bytes:
                line.append("#")
            else:
                line.append(".")
        map.append("".join(line))

    return map


def main_part1():
    corrupted_bytes = set()
    N_cb = 1024
    N_line = 0

    file_path = "/Users/boxu/Dev/aoc 2024/day_18_input.txt"
    with open(file_path, "r") as file:
        for line in file:
            if "," in line:
                x, y = line.strip().split(",")
                corrupted_bytes.add(tuple([int(x), int(y)]))
                N_line += 1
                if N_line >= N_cb:
                    break
    # print(corrupted_bytes)

    Nx = 70 + 1
    Ny = 70 + 1
    map = corrupted_map(Nx, Ny, corrupted_bytes)
    map_view(map)

    (i_start, j_start) = (0, 0)
    (i_end, j_end) = (Ny - 1, Nx - 1)

    visited_set = set()
    visited_set.add(Tile(i_start, j_start, 0, i_start, j_start))
    frontier_set = visited_set.copy()

    step = 0
    while True:
        step += 1
        frontier_set, visited_set = update_frontier(
            frontier_set, visited_set, i_end, j_end, map
        )

        # frontier_ij_set = set()
        # for tile in frontier_set:
        #     frontier_ij_set.add(
        #         tuple([tile.i, tile.j, tile.score, tile.fromi, tile.fromj])
        #     )
        # print(step, frontier_ij_set)

        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    # find end spot tile within the visited_set that has the smallest score
    smallest_score = 10**10
    for tile in visited_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        if (i, j) == (i_end, j_end):
            print(tile.i, tile.j, tile.score, tile.fromi, tile.fromj)
            if tile.score <= smallest_score:
                smallest_score = score
            else:
                pass
    print(smallest_score)


def main():
    corrupted_bytes = []
    file_path = "/Users/boxu/Dev/aoc 2024/day_18_input.txt"
    with open(file_path, "r") as file:
        for line in file:
            if "," in line:
                x, y = line.strip().split(",")
                corrupted_bytes.append(tuple([int(x), int(y)]))
    # print(len(corrupted_bytes))

    Nx = 70 + 1
    Ny = 70 + 1

    Ncb = 2500
    while True:
        Ncb += 1
        print(Ncb)
        map = corrupted_map(Nx, Ny, corrupted_bytes[:Ncb])
        # map_view(map)
        solvable = maze_solvable(map)

        if not solvable:
            print([Ncb], corrupted_bytes[Ncb - 1])
            break


if __name__ == "__main__":
    main()
