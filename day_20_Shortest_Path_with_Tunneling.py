from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    i: int
    j: int
    score: int


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
            nextstep_set.add(Tile(i + di, j + dj, score + 1))

    return nextstep_set


# based on the current frontier set of tiles, expand to new frontier with the lowest increase in score
def update_frontier(frontier_set, visited_set, map):
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
        # if the next step lead us to a visited spot but now with a smaller score, add
        else:
            # find the visited score of (i, j)
            for visited_tile in visited_set:
                (visited_i, visited_j) = (visited_tile.i, visited_tile.j)
                if (visited_i, visited_j) == (i, j):
                    visited_score = visited_tile.score
            if score < visited_score:
                new_step_set.add(tile)

        for tile in new_step_set:
            frontier_set.add(tile)
            visited_set.add(tile)

    return frontier_set, visited_set


def shortest_path(map, i_start, j_start, i_end, j_end):
    visited_set = set()
    visited_set.add(Tile(i_start, j_start, 0))
    frontier_set = visited_set.copy()

    while True:
        frontier_set, visited_set = update_frontier(frontier_set, visited_set, map)
        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    # if (i_end, j_end) not in the visited_set, maze is not solvable
    solvable = False
    smallest_score = 10**10
    for tile in visited_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        if (i, j) == (i_end, j_end):
            solvable = True
            if tile.score <= smallest_score:
                smallest_score = score
            else:
                pass

    return smallest_score, solvable


# This time there's no end point, create a dict of all the possible (i, j) can be reached with the shortest path to it
def shortest_reach(map, i_start, j_start):
    visited_set = set()
    visited_set.add(Tile(i_start, j_start, 0))
    frontier_set = visited_set.copy()

    while True:
        frontier_set, visited_set = update_frontier(frontier_set, visited_set, map)
        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    reach_score = {}
    for tile in visited_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        if (i, j) in reach_score:
            if score < reach_score[(i,j)]:
                reach_score[(i,j)] = score
            else:
                pass
        else:
            reach_score[(i,j)] = score

    return reach_score


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_20_input.txt"
    with open(file_path, "r") as file:
        description = file.read()
    map = description.split("\n")
    # print("\n".join(map))

    # find the start spot
    for index, string in enumerate(map):
        if "S" in string:
            i_start = index
            j_start = string.index("S")
    # print(i_start, j_start)

    # find the end spot
    for index, string in enumerate(map):
        if "E" in string:
            i_end = index
            j_end = string.index("E")
    # print(i_end, j_end)

    # First find the shortest path/fastest_time
    fastest_time, solvable = shortest_path(map, i_start, j_start, i_end, j_end)
    if solvable:
        print("Fastest time through the race track is", fastest_time, "picoseconds.")
    else:
        print("Start and end of this race track are disconnected")

    # Find the fastest time to reach any tile on the map from the start point
    time_from_start = shortest_reach(map, i_start, j_start)

    # Find the fastest time to reach any tile on the map from the end point
    time_from_end = shortest_reach(map, i_end, j_end)

    # Cheat time gives the dx+dy between the two sets
    cheat_time = 20
    saved_time = {}
    for i_cheat_s, j_cheat_s in time_from_start:
        start_time = time_from_start[(i_cheat_s, j_cheat_s)]
        for i_cheat_e, j_cheat_e in time_from_end:
            end_time = time_from_end[(i_cheat_e, j_cheat_e)]
            tunnel_time = abs(i_cheat_s - i_cheat_e) + abs(j_cheat_s - j_cheat_e)
            if tunnel_time <= cheat_time:
                finish_time = start_time + end_time + tunnel_time
                if finish_time < fastest_time:
                    if fastest_time - finish_time in saved_time:
                        saved_time[fastest_time - finish_time] += 1
                    else:
                        saved_time[fastest_time - finish_time] = 1

    # Announce the result:
    counts = 0
    time_limit = 100
    for s_time in sorted(saved_time):
        print("There are", saved_time[s_time], "cheats that save", s_time, "picoseconds.")
        # Count for cheats that save you at least time_limit of picoseconds
        if s_time >= time_limit:
            counts += saved_time[s_time]

    print("There are", counts, "cheats that save at least", time_limit, "picoseconds.")


if __name__ == "__main__":
    main()
