# change a number to a list
def change_num(num):
    new_lst = []
    num_str = str(num)
    digits = len(num_str)

    if num == 0:
        new_lst = [1]
    elif digits % 2 == 0:
        num_str1 = num_str[: digits // 2]
        num_str2 = num_str[digits // 2 :]
        new_lst.append(int(num_str1))
        new_lst.append(int(num_str2))
    else:
        new_lst.append(num * 2024)

    # print(new_lst)
    return new_lst


# change for the whole list
def change_lst(arrangement):
    new_arrangement = []
    for num in arrangement:
        new_lst = change_num(num)
        for new_num in new_lst:
            new_arrangement.append(new_num)

    return new_arrangement

# use dictionary to only store the counts of each unique numbers
def update_count(count):
    new_count = {}
    for num in count:
        num_counts = count[num]
        new_lst = change_num(num)
        for new_num in new_lst:
            if new_num in new_count:
                new_count[new_num] += num_counts
            else:
                new_count[new_num] = num_counts

    return new_count

def main():
    arrangement = [27, 10647, 103, 9, 0, 5524, 4594227, 902936]
    #arrangement = [125, 17]
    count = {}
    for num in arrangement:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    blinks = 75

    for i in range(0, blinks):
        count = update_count(count)
        total_counts = sum(count.values())
        print(i, total_counts)

if __name__ == "__main__":
    main()
