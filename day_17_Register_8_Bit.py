def combo_operand(operand, A, B, C):
    # Combo operands 0 through 3 represent literal values 0 through 3.
    if operand in [0, 1, 2, 3]:
        return operand
    # Combo operand 4 represents the value of register A.
    elif operand == 4:
        return A
    # Combo operand 5 represents the value of register B.
    elif operand == 5:
        return B
    # Combo operand 6 represents the value of register C.
    elif operand == 6:
        return C
    # Combo operand 7 is reserved and will not appear in valid programs.
    else:
        return "False"


def instructions(ip, opcode, operand, A, B, C):
    # A, B, C are any integer
    output = []
    ip += 2

    # The adv instruction (opcode 0)
    if opcode == 0:
        numerator = A
        denominator = 2 ** combo_operand(operand, A, B, C)
        new_A = numerator // denominator
        return new_A, B, C, output, ip

    # The bxl instruction (opcode 1)
    elif opcode == 1:
        new_B = B ^ operand
        return A, new_B, C, output, ip

    # The bst instruction (opcode 2)
    elif opcode == 2:
        new_B = combo_operand(operand, A, B, C) % 8
        return A, new_B, C, output, ip

    # The jnz instruction (opcode 3)
    elif opcode == 3:
        if A == 0:
            return A, B, C, output, ip
        else:
            ip = operand
            # print("jumped to ip", ip)
            return A, B, C, output, ip

    # The bxc instruction (opcode 4)
    elif opcode == 4:
        new_B = B ^ C
        return A, new_B, C, output, ip

    # The out instruction (opcode 5)
    elif opcode == 5:
        output = [combo_operand(operand, A, B, C) % 8]
        return A, B, C, output, ip

    # The bdv instruction (opcode 6)
    elif opcode == 6:
        numerator = A
        denominator = 2 ** combo_operand(operand, A, B, C)
        new_B = numerator // denominator
        return A, new_B, C, output, ip

    # The cdv instruction (opcode 7)
    elif opcode == 7:
        numerator = A
        denominator = 2 ** combo_operand(operand, A, B, C)
        new_C = numerator // denominator
        return A, B, new_C, output, ip

    else:
        print("opcode out of range")
        return A, B, C, output, ip


def num_8bit(digit_list):
    power = 0
    number = 0
    for i in range(len(digit_list) - 1, -1, -1):
        number += digit_list[i] * (8**power)
        power += 1
    return number


def convert_8bit(number):
    digit_list = []
    while True:
        digit = number % 8
        digit_list.insert(0, digit)
        number = number // 8
        if number == 0:
            break
    return digit_list


def main():
    A = 164542125272765  # my_input
    B = 0
    C = 0
    program = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]  # my_input
    ip = 0
    ip_end = len(program)

    step = 0
    output_list = []
    while True:
        step += 1
        A, B, C, output, ip = instructions(ip, program[ip], program[ip + 1], A, B, C)
        if len(output) != 0:
            output_list.extend(output)
            print(output, A, B, C)
        if ip > ip_end - 2:
            break

    out_str = [str(x) for x in output_list]
    print("Output is:", ",".join(out_str))

    # PART II
    result_list = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]
    A_set = {0}

    for i in range(len(result_list) - 1, -1, -1):
        output_digit = result_list[i]
        # print(output_digit)

        new_A_set = set()
        for current_A in A_set:
            A_list = convert_8bit(current_A)

            if i == len(result_list) - 1:
                A_list_last_digit = 1  # the first digit can't be zero
            else:
                A_list_last_digit = 0

            while A_list_last_digit < 8:
                A_list_temp = A_list.copy()
                A_list_temp.append(A_list_last_digit)
                A_temp = num_8bit(A_list_temp)

                A = A_temp
                B = 0
                C = 0
                for ip in range(0, len(program) - 2, 2):
                    A, B, C, output, ip = instructions(
                        ip, program[ip], program[ip + 1], A, B, C
                    )
                    if len(output) != 0 and output[0] == output_digit:
                        print(output, A, B, C)
                        new_A_set.add(A_temp)
                        break  # out of the for loop

                A_list_last_digit += 1

        A_set = set()
        A_set = new_A_set.copy()

    print(A_set)
    print(min(A_set))


if __name__ == "__main__":
    main()
