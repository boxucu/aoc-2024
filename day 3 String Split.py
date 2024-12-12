def mul_2_num(nums_input):
    nums_str = nums_input.split(",")
    if len(nums_str) == 2:
        if nums_str[0].isnumeric():
            num1 = int(nums_str[0])
        else:
            num1 = 0
        if nums_str[1].isnumeric():
            num2 = int(nums_str[1])
        else:
            num2 = 0

        if num1 > 0 and num1 < 1000 and num2 > 0 and num2 < 1000:
            mul = num1 * num2
        else:
            mul = 0
    else:
        mul = 0
    
    return mul

file_path = "/Users/boxu/Dev/aoc 2024/day 3_input.txt"
with open(file_path, 'r') as file:
    memory = file.read()

lines_new = []
do_lines = memory.split("do()")
for do_line in do_lines:
    if do_line.__contains__("don't()"):
        do_line_new = do_line[ 0 : do_line.index("don't()")]
        lines_new.append(do_line_new)
    else:
        lines_new.append(do_line)
memory_new = "".join(lines_new)

print(lines_new[2])

lines = memory_new.split("mul(")
colume_mul = []
for line in lines:
    if line.__contains__(")"):
        nums_input = line[ 0 : line.index(")")]
        colume_mul.append(mul_2_num(nums_input))

print(sum(colume_mul))

