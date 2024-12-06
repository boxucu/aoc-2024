import re
def xmas_search(map):
    xmas_count = 0
    for line in map:
        matches1 = re.findall("XMAS",line)
        xmas_count += len(matches1)
        matches2 = re.findall("SAMX",line)
        xmas_count += len(matches2)
    return xmas_count

file_path = "/Users/boxu/Dev/aoc 2024/day 4_input.txt"
with open(file_path, 'r') as file:
    maxtrix = file.read()

map_east = maxtrix.split("\n")
N = len(map_east[0])

map_south = []
for i in range (0,N):
    newline_c = [x[i] for x in map_east]
    newline = "".join(newline_c)
    map_south.append(newline)

map_sw = []
map_sw_shift = []
for i in range (0,N):
    newline = "#"*i + map_east[i] + "#"*(N-i)
    map_sw_shift.append(newline)
for i in range (0,2*N):
    newline_c = [x[i] for x in map_sw_shift]
    newline = "".join(newline_c)
    map_sw.append(newline)

map_se = []
map_se_shift = []
for i in range (0,N):
    newline = "#"*(N-i) + map_east[i] + "#"*i
    map_se_shift.append(newline)
for i in range (0,2*N):
    newline_c = [x[i] for x in map_se_shift]
    newline = "".join(newline_c)
    map_se.append(newline)

xmas_count = 0
xmas_count += xmas_search(map_east)
xmas_count += xmas_search(map_south)
xmas_count += xmas_search(map_sw)
xmas_count += xmas_search(map_se)
print(xmas_count)

###
cross_mas_count = 0
map = maxtrix.split("\n")
N = len(map[0])
for i in range (1,N-1):
    for j in range (1,N-1):
        if map[i][j] == "A":
            cross = map[i-1][j-1] + map[i+1][j+1] + map[i-1][j+1] + map[i+1][j-1]
            if cross == "MSMS" or cross == "MSSM" or cross == "SMMS" or cross == "SMSM":
                cross_mas_count += 1
print(cross_mas_count)