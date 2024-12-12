# identify the frequencies
def find_freqs(map):
    freq_set = set()
    freq_list = []
    freq_count = []

    map_str = "".join(map)
    for i in range(0, len(map_str)):
        freq_set.add(map_str[i])
    freq_set.remove(".")
    # print(freq_set)

    for freq in freq_set:
        freq_list.append(freq)
        freq_count.append(map_str.count(freq))
    # print(freq_list,freq_count)

    return freq_list, freq_count


# for each frequency, find the locations
def find_antenna(freq, map):
    freq_location = set()
    for i in range(0, len(map)):
        for j, char in enumerate(map[i]):
            if char == freq:
                index = [i, j]
                freq_location.add(tuple(index))
    # print(freq, freq_location)
    return freq_location


# for each pair of antenna, find antinodes
def find_antinodes(freq_location):
    node_location = set()
    for a, b in freq_location:
        for c, d in freq_location:
            if a != c or b != d:
                node1 = [2 * a - c, 2 * b - d]
                node2 = [2 * c - a, 2 * d - b]
                node_location.add(tuple(node1))
                node_location.add(tuple(node2))

    return node_location


# exclude out side of map ones
def clear_outsider(node_location, map):
    node_location_vaild = set()
    Nx = len(map[0])
    Ny = len(map)
    for a, b in node_location:
        if a >= 0 and a < Nx and b >= 0 and b < Ny:
            node_location_vaild.add(tuple([a, b]))

    return node_location_vaild


# for each pair of antenna, find rsonant antinodes in line
def find_res_nodes(freq_location, map):
    res_node_location = set()
    Nx = len(map[0])
    Ny = len(map)
    for a, b in freq_location:
        for c, d in freq_location:
            if a != c or b != d:
                res_node_location.add(tuple([a, b]))
                for x in range(0, Nx):
                    if x != a:
                        y = (x - a) * (d - b) / (c - a) + b
                        if y % 1 == 0:
                            res_node_location.add(tuple([x, y]))
    
    node_location_vaild = set()
    for a, b in res_node_location:
        if a >= 0 and a < Nx and b >= 0 and b < Ny:
            node_location_vaild.add(tuple([a, b]))

    return node_location_vaild


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day 8_input.txt"
    with open(file_path, "r") as file:
        maxtrix = file.read()
    map = maxtrix.split("\n")

    freq_list, freq_count = find_freqs(map)
    node_unique = set()
    for freq, count in zip(freq_list, freq_count):
        if count > 1:
            freq_location = find_antenna(freq, map)
            node_location = find_antinodes(freq_location)
            node_location = clear_outsider(node_location, map)
            # print(freq, node_location)
            # node_unique = node_unique.union(node_location)

            res_node_location = find_res_nodes(freq_location, map)
            node_unique = node_unique.union(res_node_location)
    print(len(node_unique))

if __name__ == "__main__":
    main()
