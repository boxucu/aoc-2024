file_path = "/Users/boxu/Dev/aoc 2024/day_1_input.txt"
colume_1 = []
colume_2 = []
with open(file_path, 'r') as file:
    for line in file:
        line_data = line.strip().split()
        colume_1.append(int(line_data[0]))
        colume_2.append(int(line_data[1]))

sorted_c1 = sorted(colume_1)
sorted_c2 = sorted(colume_2)

distance_list = [abs(a - b) for a, b in zip(sorted_c1, sorted_c2)]
distance_total = sum(distance_list)

#print(distance_total)

count_list = [sorted_c2.count(a) for a in sorted_c1]
score_list = [a*b for a, b in zip(sorted_c1, count_list)]
score_total = sum(score_list)

print(score_list)
print(score_total)