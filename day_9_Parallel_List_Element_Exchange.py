# create a list of file ID and file length
# create a list of free space stating starting location and free space length
def decode_length(map):
    file_id_lst = []
    file_length_lst = []
    space_id_lst = []
    space_length_lst = []

    for index, number in enumerate(map):
        if index % 2 == 0:
            file_id_lst.append(int(index / 2))
            file_length_lst.append(number)
        else:
            space_id_lst.append(int((index - 1) / 2))
            space_length_lst.append(number)

    return file_id_lst, file_length_lst, space_id_lst, space_length_lst


# recontructing two lists, one with the file id, one with the location
def rearrange(file_id_lst, file_length_lst, space_id_lst, space_length_lst):
    file_total_length = sum(file_length_lst)
    print(file_total_length)
    map_id = []
    i = 0
    while i < file_total_length:
        for j in range(0, file_length_lst[0]):
            map_id.append(file_id_lst[0])
            i += 1
        file_id_lst.pop(0)
        file_length_lst.pop(0)
        # print(map_id)
        # print(file_id_lst,file_length_lst)

        if len(file_id_lst) != 0:
            k = 0
            while k < space_length_lst[0]:
                map_id.append(file_id_lst[-1])
                i += 1
                k += 1
                last_id_length = file_length_lst[-1] - 1
                if last_id_length == 0:
                    file_id_lst.pop()
                    file_length_lst.pop()
                else:
                    file_length_lst.pop()
                    file_length_lst.append(last_id_length)

            space_id_lst.pop(0)
            space_length_lst.pop(0)
            # print(map_id)
            # print(file_id_lst,file_length_lst)

    return map_id


# for part two, move one file at a time:
def move_block(file_id_lst, file_length_lst, space_id_lst, space_length_lst):
    if len(space_id_lst) < len(file_id_lst):
        space_id_lst.append(0)
        space_length_lst.append(0)

    print(sum(file_length_lst)+sum(space_length_lst))

    file_id = file_id_lst[-1]
    while file_id > 0:
        index = file_id_lst.index(file_id)
        file_length = file_length_lst[index]

        i_space = 0
        while i_space < index:
            space_length = space_length_lst[i_space]
            if space_length < file_length:
                i_space += 1
            else:
                file_id_lst.pop(index)
                file_length_lst.pop(index)
                file_id_lst.insert(i_space + 1, file_id)
                file_length_lst.insert(i_space + 1, file_length)

                space_length_lst[i_space] = 0
                space_length_lst.insert(i_space + 1, space_length - file_length)
                space_length_lst[index] = (
                    space_length_lst[index] + file_length + space_length_lst[index + 1]
                )
                space_length_lst.pop(index + 1)

                break
        file_id -= 1
    #print(sum(file_length_lst))

    # reconstruct map
    file_total_length = sum(file_length_lst) + sum(space_length_lst)
    print(file_total_length)
    map_id = []
    i = 0
    while i < file_total_length:
        for j in range(0, file_length_lst[0]):
            map_id.append(file_id_lst[0])
            i += 1
        file_id_lst.pop(0)
        file_length_lst.pop(0)

        for k in range(0, space_length_lst[0]):
            map_id.append(0)
            i += 1
        space_id_lst.pop(0)
        space_length_lst.pop(0)

        # print(map_id)

    return map_id


# find checksum
def checksum(map_id):
    check = 0
    for index, file_id in enumerate(map_id):
        check += index * file_id

    return check


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day 9_input.txt"
    with open(file_path, "r") as file:
        disk_map = file.read()
    map = [int(x) for x in disk_map]
    file_id_lst, file_length_lst, space_id_lst, space_length_lst = decode_length(map)
    # print(file_id_lst)
    # map_id = rearrange(file_id_lst, file_length_lst, space_id_lst, space_length_lst)
    map_id = move_block(file_id_lst, file_length_lst, space_id_lst, space_length_lst)
    check = checksum(map_id)
    print(check)


if __name__ == "__main__":
    main()
