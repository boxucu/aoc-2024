def find_linked_pcs(pc, single_link_set, pc_name_list):
    connected_pcs = set()
    for pc1, pc2 in single_link_set:
        if pc1 == pc and pc2 in pc_name_list:
            connected_pcs.add(pc2)
        elif pc2 == pc and pc1 in pc_name_list:
            connected_pcs.add(pc1)
    return connected_pcs


def check_connection(pc1, pc2, single_link_set):
    if (pc1, pc2) in single_link_set:
        return True
    elif (pc2, pc1) in single_link_set:
        return True
    else:
        return False


def check_all_connections(next_pc, pc_list, single_link_set):
    result = True
    for pc in pc_list:
        result = result and check_connection(pc, next_pc, single_link_set)
    return result


def find_longest_chain(pc, single_link_set, pc_name_list):
    connected_pcs = find_linked_pcs(pc, single_link_set, pc_name_list)
    # this limits the possible pcs in this LAN party pool

    pc_chain_list = []
    pc_chain_list.append(pc)

    while True:
        new_pc_chain_list = []
        for pc_chain in pc_chain_list:
            # find all pcs that are already on this pc_chain
            pc_list = pc_chain.split(",")
            # search the next pc that can be connected to the chian, the next pc name must be "larger" than the last pc in the chain
            for next_pc in connected_pcs:
                if next_pc > pc_list[-1]:
                    # check if next_pc is connected to all previous pcs
                    if check_all_connections(next_pc, pc_list, single_link_set):
                        new_pc_chain_list.append(pc_chain + "," + next_pc)
        # print(new_pc_chain_list)
        if len(new_pc_chain_list) == 0:
            break
        else:
            pc_chain_list = new_pc_chain_list.copy()

    return pc_chain_list


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_23_input.txt"
    single_link_set = set()
    pc_name_set = set()
    with open(file_path, "r") as file:
        for line in file:
            pc1, pc2 = line.strip().split("-")
            single_link_set.add((pc1, pc2))
            pc_name_set.add(pc1)
            pc_name_set.add(pc2)
    pc_name_list = list(sorted(pc_name_set))  # sorted alphabetically

    # PART I
    # find the pc names starts with "t" in it
    pc_t_set = set()
    for pc_name in pc_name_set:
        if pc_name[0] == "t":
            pc_t_set.add(pc_name)
    # print(pc_t_set)

    interconnected_pcs = set()
    # for each "t?" pc, find the set of connected pcs
    for pc_t in pc_t_set:
        connected_pcs = find_linked_pcs(pc_t, single_link_set, pc_name_list)

        # find the inter-connected pairs
        for pc1, pc2 in single_link_set:
            if pc1 in connected_pcs and pc2 in connected_pcs:
                interconnected_pcs.add((pc_t, pc1, pc2))
                interconnected_pcs.add((pc_t, pc2, pc1))
                interconnected_pcs.add((pc1, pc2, pc_t))
                interconnected_pcs.add((pc1, pc_t, pc2))
                interconnected_pcs.add((pc2, pc1, pc_t))
                interconnected_pcs.add((pc2, pc_t, pc1))

    print(
        "There are",
        len(interconnected_pcs) // 6,
        "sets of three inter-connected computers with t# name",
    )

    # PART II
    longest_chain_len = 0
    while True:
        pc = pc_name_list[0]
        pc_chain_list = find_longest_chain(pc, single_link_set, pc_name_list)
        pc_chain = pc_chain_list[0]
        if len(pc_chain) > longest_chain_len:
            longest_chain_len = len(pc_chain)
            longest_chain = pc_chain

        if len(pc_name_list) == 1:
            break
        else:
            pc_name_list.pop(0)

    print(longest_chain)


if __name__ == "__main__":
    main()
