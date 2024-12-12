# read map as 2D int matrix
def read_map_num(file_path):
    with open(file_path, "r") as file:
        maxtrix = file.read()
    map_str = maxtrix.split("\n")

    map = []
    for line in map_str:
        line_num = [int(x) for x in line]
        map.append(line_num)

    return map


# identify the location of all trailheads
def find_trailhead(map):
    trailhead_set = set()
    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            if map[i][j] == 0:
                index = [i, j]
                trailhead_set.add(tuple(index))

    return trailhead_set


# for a spot at (x, y) with value "h", in map find the set of next spot
def find_nextstep(x, y, map):
    h = map[x][y]
    nextstep_set = set()
    neighbor_set = set()
    Nx = len(map)
    Ny = len(map[0])
    neighbor_set.add(tuple([abs(x - 1), y]))
    neighbor_set.add(tuple([x, abs(y - 1)]))
    if y < Ny - 1:
        neighbor_set.add(tuple([x, y + 1]))
    if x < Nx - 1:
        neighbor_set.add(tuple([x + 1, y]))

    for a, b in neighbor_set:
        neighbor_h = map[a][b]
        if neighbor_h == h + 1:
            nextstep_set.add(tuple([a, b]))

    return nextstep_set


# for a trailhead at (x0,y0), find the set of "9" that it can reach
def find_trailend(x0, y0, map):
    nextstep_set = set()
    nextstep_set.add(tuple([x0, y0]))
    h = 0
    while h < 9:
        new_steps_set = set()
        for x, y in nextstep_set:
            new_steps = find_nextstep(x, y, map)
            new_steps_set = new_steps_set.union(new_steps)
        nextstep_set.clear()
        nextstep_set = nextstep_set.union(new_steps_set)
        if len(new_steps_set) == 0:
            trailend_set = set()
            break
        else:
            h += 1
    trailend_set = nextstep_set

    return trailend_set


# for a trailhead at (x0,y0), find the list of "9" that it can reach, along with the distinct trail number
def find_trail(x0, y0, map):
    nextstep_lst = []
    nextstep_lst.append([x0, y0])
    h = 0
    while h < 9:
        new_steps_lst = []
        for x, y in nextstep_lst:
            new_steps = find_nextstep(x, y, map)
            for a, b in new_steps:
                new_steps_lst.append([a, b])

        nextstep_lst.clear()
        nextstep_lst.extend(new_steps_lst)

        if len(nextstep_lst) == 0:
            trail_num = 0
            break
        else:
            h += 1
    trail_num = len(nextstep_lst)

    return trail_num


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day 10_input.txt"
    map = read_map_num(file_path)
    trailhead_set = find_trailhead(map)
    # print(trailhead_set)

    score = 0
    for x0, y0 in trailhead_set:
        # trailend_set = find_trailend(x0, y0, map)
        # score += len(trailend_set)
        trail_num = find_trail(x0, y0, map)
        score += trail_num

    print(score)


if __name__ == "__main__":
    main()
