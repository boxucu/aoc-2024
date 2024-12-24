def calc_output(output, output_inputs, wire_value):
    (input1, operation, input2) = output_inputs[output]
    if operation == "AND":
        wire_value[output] = wire_value[input1] and wire_value[input2]
    elif operation == "OR":
        wire_value[output] = wire_value[input1] or wire_value[input2]
    elif operation == "XOR":
        wire_value[output] = wire_value[input1] ^ wire_value[input2]
    else:
        print("Undefined Gate")
    return wire_value[output]


def find_output(inputa, operationt, inputb, output_inputs):
    correct_output = "not found"
    for output in output_inputs:
        (input1, operation, input2) = output_inputs[output]
        if inputa == input1 and inputb == input2 and operationt == operation:
            correct_output = output
        elif inputa == input2 and inputb == input1 and operationt == operation:
            correct_output = output
    if correct_output == "not found":
        print("Cannot find output for", inputa, operationt, inputb)
    return correct_output


def decimal_value(wire_value):
    binary_str_list = []
    for wire in sorted(wire_value, reverse=True):
        binary_str_list.append(str(int(wire_value[wire])))
    binary_str = "".join(binary_str_list)
    decimal_value = int(binary_str, 2)
    return decimal_value, binary_str


def main():
    wire_value = {}
    output_inputs = {}
    file_path = "/Users/boxu/Dev/aoc 2024/day_24_input.txt"
    with open(file_path, "r") as file:
        for line in file:
            if ":" in line:
                try:
                    wire, value = line.strip().split(": ")
                    wire_value[wire] = bool(int(value))
                except ValueError:
                    print(f"Error: Invalid format in line: '{line}'")
            elif "->" in line:
                try:
                    inputs, output = line.strip().split(" -> ")
                    input1, operation, input2 = inputs.split(" ")
                    output_inputs[output] = (input1, operation, input2)
                except ValueError:
                    print(f"Error: Invalid format in line: '{line}'")

    # for wire in wire_value:
    #     print(wire, wire_value[wire])
    # for output in output_inputs:
    #     print(output, output_inputs[output])

    x_wire_value = {}
    y_wire_value = {}
    for wire in wire_value:
        if wire[0] == "x":
            x_wire_value[wire] = wire_value[wire]
        elif wire[0] == "y":
            y_wire_value[wire] = wire_value[wire]
    x_decimal, x_binary = decimal_value(x_wire_value)
    y_decimal, y_binary = decimal_value(y_wire_value)
    except_z_decimal = x_decimal + y_decimal
    print("x wires input is", x_decimal, ", y wires input is", y_decimal)
    print("expected z wires output is", except_z_decimal)

    # PART I
    z_wire_value = {}
    while True:
        calc_count = 0
        for output in output_inputs:
            (input1, operation, input2) = output_inputs[output]
            if (
                input1 in wire_value
                and input2 in wire_value
                and output not in wire_value
            ):
                value = calc_output(output, output_inputs, wire_value)
                calc_count += 1
                if output[0] == "z":
                    z_wire_value[output] = value
            else:
                pass  # wait until the values came
        if calc_count == 0:
            break

    z_decimal, z_binary = decimal_value(z_wire_value)
    print("z wires output is", z_decimal)

    # PART II
    # target_output = {"z03"}
    # while len(target_output) > 0:
    #     new_target_output = set()
    #     for output in target_output:
    #         if output in output_inputs:
    #             (input1, operation, input2) = output_inputs[output]
    #             print(output, "<-", output_inputs[output])
    #             new_target_output.add(input1)
    #             new_target_output.add(input2)
    #     target_output = new_target_output.copy()

    carry_on = "ntr"
    digit = 2
    while digit < 45:
        x_wire = "x" + f"{digit:02d}"
        y_wire = "y" + f"{digit:02d}"
        z_wire = "z" + f"{digit:02d}"

        xy_xor = find_output(x_wire, "XOR", y_wire, output_inputs)
        xy_and = find_output(x_wire, "AND", y_wire, output_inputs)
        z_output = find_output(xy_xor, "XOR", carry_on, output_inputs)
        intermedia = find_output(xy_xor, "AND", carry_on, output_inputs)
        carry_on = find_output(
            xy_and, "OR", intermedia, output_inputs
        )  # new carry on for the next digit calculation

        if z_output == z_wire:
            print("Checked", z_wire, "carry_on:", carry_on)
            digit += 1
        elif intermedia == "not found":
            print("xy_xor:", xy_xor, "xy_and:", xy_and, "z_output:", z_output)
            break
        elif carry_on == "not found":
            print(z_output, "should be swapped with", z_wire)
            print(
                "xy_xor:",
                xy_xor,
                "xy_and:",
                xy_and,
                "z_output:",
                z_output,
                "intermedia:",
                intermedia,
            )
            break
        else:
            print(z_output, "should be swapped with", z_wire)
            break

    swapped = set()
    swapped.add("z05")
    swapped.add("dkr")

    swapped.add("z15")
    swapped.add("htp")

    swapped.add("z20")
    swapped.add("hhh")

    swapped.add("ggk")
    swapped.add("rhv")

    # print(sorted(swapped))


if __name__ == "__main__":
    main()
