def expand_one_step(region_set, border_set, character, map):
    Nx = len(map)
    Ny = len(map[0])

    # based on the border, expand index in every direction
    new_border_dict = {}
    for x, y in border_set:
        for dx in [-1, 1]:
            if (x + dx, y) in new_border_dict:
                new_border_dict[(x + dx, y)] += 1
            else:
                new_border_dict[(x + dx, y)] = 1
        for dy in [-1, 1]:
            if (x, y + dy) in new_border_dict:
                new_border_dict[(x, y + dy)] += 1
            else:
                new_border_dict[(x, y + dy)] = 1

    N_fence_add = 0
    new_border_set = set()
    # exclude the index that are out of boundary or already in the region
    for x, y in new_border_dict:
        if x < 0 or x >= Nx or y < 0 or y >= Ny:
            pass
        elif (x, y) in region_set:
            pass
        elif map[x][y] != character:
            pass
        else:
            new_border_set.add(tuple([x, y]))
            if new_border_dict[(x, y)] == 1:
                N_fence_add += 2
            elif new_border_dict[(x, y)] == 2:
                N_fence_add += 0
            elif new_border_dict[(x, y)] == 3:
                N_fence_add += -2
            elif new_border_dict[(x, y)] == 4:
                N_fence_add += -4
    # if the index is counted once N_fence add 2, twice add 0, three times add -2, four times add -4
    # print(new_border_set)
    return new_border_set, N_fence_add


# For a specific spot (x,y) on map, find the index of all its adjent same character
def find_region(x, y, map):
    region_set = set()
    border_set = {(x, y)}
    N_fence = 4
    N_side = 4
    character = map[x][y]

    while True:
        region_set = region_set.union(border_set)
        border_set, N_fence_add = expand_one_step(
            region_set, border_set, character, map
        )

        if len(border_set) == 0:
            break
        else:
            N_fence += N_fence_add
            # print(border_set)

    return region_set, N_fence


def search_corners(region_set, map):
    Nx = len(map)
    Ny = len(map[0])
    N_1_corner = 0
    N_2_corner = 0
    N_3_corner = 0
    D_x = [[0, -1], [0, -1], [0, 1], [0, 1]]
    D_y = [[0, -1], [0, 1], [0, -1], [0, 1]]

    for x, y in region_set:
        for Dx, Dy in zip(D_x, D_y):
            has_corner = []
            for dx in Dx:
                for dy in Dy:
                    if x + dx < 0 or x + dx >= Nx or y + dy < 0 or y + dy >= Ny:
                        has_corner.append(0)
                    elif (x + dx, y + dy) in region_set:
                        has_corner.append(1)
                    else:
                        has_corner.append(0)
            if sum(has_corner) == 1:
                N_1_corner += 1
                # 1/4 in region, contribute to 2*1/2 sides, will be count once during search
            elif sum(has_corner) == 3:
                N_3_corner += 1
                # 3/4 in region, contribute to 2*1/2 sides, will be count three-times during search
            elif has_corner == [0, 1, 1, 0] or has_corner == [1, 0, 0, 1]:
                N_2_corner += 1
                # 1/2 in region, but from "+" shaped corner, contribute to 4*1/2 sides, will be count twice during search
            N_side = N_1_corner + N_2_corner + int(N_3_corner / 3)
    print(len(region_set), N_side)

    return N_side


def search_map(map):
    Nx = len(map)
    Ny = len(map[0])
    searched_set = set()
    price_fence = 0
    price_side = 0

    for i in range(0, Nx):
        for j in range(0, Ny):
            if (i, j) not in searched_set:
                region_set, N_fence = find_region(i, j, map)
                searched_set = searched_set.union(region_set)

                price_fence += len(region_set) * N_fence
                N_side = search_corners(region_set, map)
                price_side += len(region_set) * N_side

    return price_fence, price_side


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day 12_input.txt"
    with open(file_path, "r") as file:
        maxtrix = file.read()
    map = maxtrix.split("\n")

    # print(map)
    price_fence, price_side = search_map(map)
    print(price_fence, price_side)


if __name__ == "__main__":
    main()
