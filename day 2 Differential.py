def line_check(line_data):
    length = len(line_data)
    line_diff = [(b - a) for a, b in zip(line_data[0:length-1], line_data[1:length])]

    sign = 1
    if line_diff[0]<0:
        sign = -1
    line_diff_norm = [sign*x for x in line_diff]
    mark = 0
    
    if all(i <= 3 and i >= 1 for i in line_diff_norm):
        mark = 1
    
    return mark
    
file_path = "/Users/boxu/Dev/aoc 2024/day 2_input.txt"
colume_mark = []
with open(file_path, 'r') as file:
    for line in file:
        line_str = line.strip().split()
        line_data = [int(x) for x in line_str]

        mark2 = 0
        mark2 += line_check(line_data)

        for i in range (0,len(line_data)):
            data_pop = line_data[:]
            data_pop.pop(i)
            mark2 += line_check(data_pop)

        if mark2 >= 1:
            mark = 1
        else:
            mark = 0
        colume_mark.append(mark)

print(sum(colume_mark))