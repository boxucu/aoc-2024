# function to do calculation
def calculation(nums, operators):
    result = nums[0]
    for i in range(0, len(operators)):
        if operators[i] == 1:
            result += nums[i + 1]
        if operators[i] == 0:
            result *= nums[i + 1]
    return result


# function to sweep the possible operators
def sweep_operator(nums):
    result_list = []
    N = len(nums) - 1
    for i in range(0, 2**N):
        operators = []
        for j in range(0, N):
            op_bit, i = divmod(i, (2 ** (N - j - 1)))
            operators.append(op_bit)
        # print(operators)
        result = calculation(nums, operators)
        result_list.append(result)
    return result_list


# function to do calculation
def calculation_v2(nums, operators):
    result = nums[0]
    for i in range(0, len(operators)):
        if operators[i] == 1:
            result += nums[i + 1]
        if operators[i] == 0:
            result *= nums[i + 1]
        if operators[i] == 2:
            new_str = str(result) + str(nums[i + 1])
            result = int(new_str)
    return result


# function to sweep the possible operators
def sweep_operator_v2(nums):
    result_list = []
    N = len(nums) - 1
    for i in range(0, 3**N):
        operators = []
        for j in range(0, N):
            op_bit, i = divmod(i, (3 ** (N - j - 1)))
            operators.append(op_bit)
        # print(operators)
        result = calculation_v2(nums, operators)
        result_list.append(result)
    return result_list


def main():
    test_value = []
    num_equation = []

    file_path = "/Users/boxu/Dev/aoc 2024/day 7_input.txt"
    with open(file_path, "r") as file:
        for line in file:
            a, b = line.split(":")
            test_value.append(int(a.strip()))
            b_str = b.strip().split()
            b_num = [int(x) for x in b_str]
            num_equation.append(b_num)

    good_value = []
    for i in range(0, len(test_value)):
        value = test_value[i]
        nums = num_equation[i]
        result_list = sweep_operator(nums)
        if value in result_list:
            good_value.append(value)

    print(sum(good_value))


if __name__ == "__main__":
    main()
