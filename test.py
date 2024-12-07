def replace_char_at_index(map, i, j, new_char):
    line_new = map[i][:j] + new_char + map[i][j + 1:]
    map_new = []
    for index in range (0, len(map)):
        if index == i:
            map_new.append(line_new)
        else:
            map_new.append(map[index])
    return map_new

def final_step_check(index,direct):
    mark = False
    if direct == 1 and index[0] == 0:
        mark = True
    if direct == 2 and index[1] == width_WE-1:
        mark = True
    if direct == 3 and index[0] == width_NS-1:
        mark = True
    if direct == 4 and index[1] == 0:
        mark = True
    return mark

def find_direct(index,direct,map):
    #directions: 1:^, 2:>, 3:v,4:<
    direct_dict = {1:2,2:3,3:4,4:1}
    i = index[0]
    j = index[1]
    while True:
        if direct == 1 and map[i-1][j] == "#":
            direct = direct_dict[direct]
        if direct == 2 and map[i][j+1] == "#":
            direct = direct_dict[direct]
        if direct == 3 and map[i+1][j] == "#":
            direct = direct_dict[direct]
        if direct == 4 and map[i][j-1] == "#":
            direct = direct_dict[direct]
        else:
            break
    return direct

def move_a_step(index,direct,map):
    i = index[0]
    j = index[1]
    end_move = False
    if final_step_check(index,direct):
        map_new = replace_char_at_index(map, i, j, "X")
        end_move = True
        direct_new = direct
        index_new = index
    else:
        direct_new = find_direct(index,direct,map)
        if direct_new == 1:
            index_new = [i-1, j]
        if direct_new == 2:
            index_new = [i, j+1]
        if direct_new == 3:
            index_new = [i+1, j]
        if direct_new == 4:
            index_new = [i, j-1]
        map_new = replace_char_at_index(map, i, j, "X")
    return index_new, direct_new, map_new, end_move

def add_obstacle(map,i,j,index_start):
    ob_added = False
    if map[i][j] != "#" and [i,j] != index_start:
        map_new = replace_char_at_index(map, i, j, "#")
        ob_added = True
    else:
        map_new = map[:][:]
    return map_new, ob_added

file_path = "/Users/boxu/Dev/aoc 2024/example.txt"
with open(file_path, 'r') as file:
    maxtrix = file.read()
map = maxtrix.split("\n")

width_NS = len(map)
width_WE = len(map[0])

for i, string in enumerate(map):
    if "^" in string:
        index_start = [i,string.index("^")]
        direct_start = 1

success_spot = 0
for i in range (0,width_NS):
    for j in range (0, width_WE):
        map_new, ob_added = add_obstacle(map,i,j,index_start)
        if ob_added:
            index = index_start[:]
            direct = 1
            end_move = False
            step_count = 0
            while end_move == False:
                index, direct, map_new, end_move = move_a_step(index,direct,map_new)
                step_count += 1
                if step_count > 50:
                    end_move = True
                    success_spot += 1

print(success_spot)