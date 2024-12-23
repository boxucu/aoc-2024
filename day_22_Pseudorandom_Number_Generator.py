def mixing(secret, value):
    return secret ^ value


def pruning(secret):
    return secret % 16777216


def process_part1(secret):
    value = secret * 64
    secret = mixing(secret, value)
    secret = pruning(secret)

    value = secret // 32
    secret = mixing(secret, value)
    secret = pruning(secret)

    value = secret * 2048
    secret = mixing(secret, value)
    secret = pruning(secret)
    return secret


def price_list_gen(secret, finial_step):
    price_0 = secret % 10
    price_list = [price_0]
    change_list = []
    step = 0
    while step < finial_step:
        step += 1
        secret = process_part1(secret)
        price = secret % 10

        change_list.append(price - price_list[-1])
        price_list.append(price)
    return price_list, change_list


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_22_input.txt"
    initial_secret_list = []
    with open(file_path, "r") as file:
        for line in file:
            initial_secret_list.append(int(line.strip()))

    # PART I
    # finial_step = 2000
    # secret_sum = 0
    # for initial_secret in initial_secret_list:
    #     secret = initial_secret
    #     step = 0
    #     while step < finial_step:
    #         step += 1
    #         secret = process_part1(secret)
    #     print(initial_secret, ":", secret)
    #     secret_sum += secret
    # print("The sum of the 2000th secret number is", secret_sum)

    # PART II
    finial_step = 2000

    sequence_total_price = {}
    for initial_secret in initial_secret_list:
        price_list, change_list = price_list_gen(initial_secret, finial_step)
        sequence_visited = set()
        for i in range(0, len(price_list) - 4):
            sequence = tuple(change_list[i : i + 4])
            if sequence in sequence_visited:
                pass
            else:
                sequence_visited.add(sequence)
                if sequence not in sequence_total_price:
                    sequence_total_price[sequence] = price_list[i + 4]
                else:
                    sequence_total_price[sequence] += price_list[i + 4]

    max_sequence = max(sequence_total_price, key=sequence_total_price.__getitem__)
    print(max_sequence, sequence_total_price[max_sequence])


if __name__ == "__main__":
    main()
