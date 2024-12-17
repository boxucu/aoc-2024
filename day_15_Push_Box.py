def parse_input(description):
    # Split the input description into the two parts using the empty line as the delimiter
    map_part, directions_part = description.strip().split("\n\n")

    # Parse the map into a list of strings
    char_map = map_part.splitlines()

    # Parse the directions into a list of individual characters
    directions = "".join(directions_part.split("\n"))
    # print(directions)

    return char_map, directions


def wide_map(map):
    map_wide = []
    for row in map:
        row_wide = []
        for char in row:
            if char == "#":
                row_wide.append("##")
            elif char == ".":
                row_wide.append("..")
            elif char == "@":
                row_wide.append("@.")
            elif char == "O":
                row_wide.append("[]")
        map_wide.append("".join(row_wide))

    map_view(map_wide)
    return map_wide


def map_view(map):
    for line in map:
        print(line)


def replace_char_at_index(map, i, j, new_char):
    line_new = map[i][:j] + new_char + map[i][j + 1 :]
    map_new = []
    for index in range(0, len(map)):
        if index == i:
            map_new.append(line_new)
        else:
            map_new.append(map[index])
    return map_new


# based the current diection and current map, create the next map
def one_step_map_change(direction_num, map):
    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]  # direction_num 0 - ">", 1 - "^", 2 - "<", 3 - "v"
    (di, dj) = didj[direction_num]

    # find the current location of robot
    for index, string in enumerate(map):
        if "@" in string:
            i = index
            j = string.index("@")

    # read the line of charaters in the current direction, start with @ stop at #
    index_i = i
    index_j = j
    line = []
    while True:
        char = map[index_i][index_j]
        line.append(char)
        index_i += di
        index_j += dj
        if char == "#":
            break
    # print("".join(line))

    # skip if hit the wall
    if line[1] == "#":
        pass
    # else: facing a box or empty spot
    else:
        # find the index of the first "." in the line
        if "." in line:
            N_empty = line.index(".")
            map = replace_char_at_index(map, i + di * N_empty, j + dj * N_empty, "O")
            map = replace_char_at_index(map, i + di, j + dj, "@")
            map = replace_char_at_index(map, i, j, ".")
        else:
            # no more space to move the box, pass
            pass

    return map


# PART II, based the current diection and current map, create the next map
def one_step_partII(direction_num, map):
    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]  # direction_num 0 - ">", 1 - "^", 2 - "<", 3 - "v"
    (di, dj) = didj[direction_num]

    # find the current location of robot
    for index, string in enumerate(map):
        if "@" in string:
            i = index
            j = string.index("@")

    # read the line of charaters in the current direction, start with @ stop at #
    index_i = i
    index_j = j
    # print(index_i, index_j)

    line = []
    while True:
        char = map[index_i][index_j]
        line.append(char)
        index_i += di
        index_j += dj
        if char == "#":
            break
    # print("".join(line))

    # it will be the same for all cases if facing the wall or empty
    # skip if hit the wall
    if line[1] == "#":
        pass
    # move if facing an empty space
    elif line[1] == ".":
        map = replace_char_at_index(map, i, j, ".")
        map = replace_char_at_index(map, i + di, j + dj, "@")
    # else meanings facing a box
    else:
        # for left and right movement, the logic should be the same as part I
        if direction_num % 2 == 0:
            if "." in line:
                N_empty = line.index(".")
                if line[1] == "[":
                    for k in range(2, N_empty, 2):
                        map = replace_char_at_index(map, i + di * k, j + dj * k, "[")
                    for m in range(3, N_empty + 1, 2):
                        map = replace_char_at_index(map, i + di * m, j + dj * m, "]")
                else:
                    for k in range(2, N_empty, 2):
                        map = replace_char_at_index(map, i + di * k, j + dj * k, "]")
                    for m in range(3, N_empty + 1, 2):
                        map = replace_char_at_index(map, i + di * m, j + dj * m, "[")
                map = replace_char_at_index(map, i, j, ".")
                map = replace_char_at_index(map, i + di, j + dj, "@")
            else:
                # no more space to move the box, pass
                pass

        # for up and down movement
        else:
            box_set = tree_search(i, j, di, map)
            # look through all edges in the way of the tree
            for boxi, boxj in box_set:
                if map[boxi + di][boxj] == "#":
                    return map
            # after the for loop, all edges are clear, then move all tree points up
            for boxi, boxj in box_set:
                map = replace_char_at_index(map, boxi, boxj, ".")
            for boxi, boxj in box_set:
                map = replace_char_at_index(map, boxi + di, boxj, box_set[(boxi, boxj)])
            # finally, move the robot
            map = replace_char_at_index(map, i, j, ".")
            map = replace_char_at_index(map, i + di, j + dj, "@")

    return map


def tree_search(i, j, di, map):
    char = map[i + di][j]
    box_set = {}
    if char == "[":
        box_set[(i + di, j)] = "["
    else:
        box_set[(i + di, j - 1)] = "["
    # find the set of locations of the left edge of boxes in the tree
    while True:
        box_set_add = {}
        for boxi, boxj in box_set:
            for dj in [-1, 0, 1]:
                if (
                    map[boxi + di][boxj + dj] == "["
                    and (boxi + di, boxj + dj) not in box_set
                ):
                    box_set_add[(boxi + di, boxj + dj)] = "["

        if len(box_set_add) == 0:
            break
        else:
            box_set.update(box_set_add)
    # add all right edges of boxes in the tree
    for boxi, boxj in box_set:
        box_set_add[(boxi, boxj + 1)] = "]"
    box_set.update(box_set_add)

    return box_set


def GPS_sum(map, mark):
    GPS_score = 0
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == mark:
                GPS_score += x + 100 * y

    return GPS_score


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_15_input.txt"
    with open(file_path, "r") as file:
        description = file.read()

    map, directions = parse_input(description)
    map_wide = wide_map(map)

    print(len(directions))
    step = 0

    for direction_string in directions:
        if direction_string == ">":
            direction_num = 0
        elif direction_string == "^":
            direction_num = 1
        elif direction_string == "<":
            direction_num = 2
        elif direction_string == "v":
            direction_num = 3
        else:
            pass

        map_wide = one_step_partII(direction_num, map_wide)
        # print(direction_string)
        # map_view(map_wide)
        step += 1

    print(step)
    map_view(map)
    GPS_score = GPS_sum(map_wide, "[")
    print(GPS_score)


if __name__ == "__main__":
    main()
