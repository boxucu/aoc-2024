from dataclasses import dataclass

@dataclass(frozen=True)
class Tile:
    i: int
    j: int
    direct: int
    score: int
    fromi: int
    fromj: int


# based on current tile (i, j, direct, score, fromi, fromj) give the set of possible next tiles
def find_next_tile(tile, map):
    (i, j) = (tile.i, tile.j)
    direct = tile.direct
    score = tile.score

    # direct 0: east, 1: north, 2: west, 3: south
    possible_next_direct_set = set()
    for dd in [-1, 0, 1]:
        possible_next_direct_set.add((direct + dd) % 4)
    # print(possible_next_direct_set)

    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]  # direct 0 - ">", 1 - "^", 2 - "<", 3 - "v"

    nextstep_set = set()
    for next_direct in possible_next_direct_set:
        (di, dj) = didj[next_direct]
        if map[i + di][j + dj] != "#":
            if next_direct == direct:
                nextstep_set.add(Tile(i + di, j + dj, next_direct, score + 1, i, j))
            else:
                nextstep_set.add(Tile(i + di, j + dj, next_direct, score + 1001, i, j))

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
        (i, j) = (tile.i, tile.j)
        (direct, score) = (tile.direct, tile.score)
        # if next step is not already visited, add
        if (i, j) not in visited_ij_set:
            new_step_set.add(tile)
        # if the next step lead us to a visited spot but now with a <= score, add
        else:
            # find the visited score of (i, j)
            for visited_tile in visited_set:
                (visited_i, visited_j) = (visited_tile.i, visited_tile.j)
                if (visited_i, visited_j) == (i, j):
                    (visited_direct, visited_score) = (
                        visited_tile.direct,
                        visited_tile.score,
                    )
            if direct == visited_direct and score < visited_score + 0:
                new_step_set.add(tile)
            elif direct != visited_direct and score <= visited_score + 1000:
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


# based on visited_set and current set of (i, j), find the previous (i, j) set
def trace_back_ij(current_ij_set, visited_set, path_set):
    previous_ij_set = set()
    for i, j in current_ij_set:
        for tile in visited_set:
            (v_i, v_j, v_fromi, v_fromj) = (tile.i, tile.j, tile.fromi, tile.fromj)
            if (v_i, v_j) == (i, j) and (v_fromi, v_fromj) not in path_set:
                previous_ij_set.add(tuple([v_fromi, v_fromj]))

    return previous_ij_set


# based on visited_set and current set of (tile), find the previous (tile) set
def trace_back(current_set, visited_set):
    previous_set = set()
    for current_tile in current_set:
        (fromi, fromj) = (current_tile.fromi, current_tile.fromj)
        for tile in visited_set:
            if (tile.i, tile.j) == (fromi, fromj) and tile.score < current_tile.score:
                previous_set.add(tile)

    return previous_set


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_16_input.txt"
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

    visited_set = set()
    visited_set.add(Tile(i_start, j_start, 0, 0, i_start, j_start))
    frontier_set = visited_set.copy()

    step = 0
    while True:
        step += 1
        frontier_set, visited_set = update_frontier(
            frontier_set, visited_set, i_end, j_end, map
        )

        # frontier_ij_set = set()
        # for tile in frontier_set:
        #     frontier_ij_set.add(tuple([tile.i, tile.j, tile.score, tile.fromi, tile.fromj]))
        # print(step, frontier_ij_set)
        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    # find end spot tile within the visited_set that has the smallest score
    smallest_score = 10**10
    for tile in visited_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        if (i, j) == (i_end, j_end):
            print(tile.i, tile.j, tile.direct, tile.score, tile.fromi, tile.fromj)
            if tile.score <= smallest_score:
                smallest_score = score
            else:
                pass

    current_set = set()
    for tile in visited_set:
        (i, j, score) = (tile.i, tile.j, tile.score)
        if (i, j, score) == (i_end, j_end, smallest_score):
            current_set.add(tile)

    # trace back the path
    path_set = set()
    step = 0
    while True:
        step += 1
        for tile in current_set:
            path_set.add(tuple([tile.i, tile.j]))
        current_set = trace_back(current_set, visited_set)
        # print(step, path_set)

        if len(current_set) == 0:
            break
        # elif step > 100:
        #     break

    print(len(path_set))


if __name__ == "__main__":
    main()
