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
    mark_turn = False
    while True:
        if direct == 1 and map[i-1][j] == "#":
            direct = direct_dict[direct]
            mark_turn = True
        if direct == 2 and map[i][j+1] == "#":
            direct = direct_dict[direct]
            mark_turn = True
        if direct == 3 and map[i+1][j] == "#":
            direct = direct_dict[direct]
            mark_turn = True
        if direct == 4 and map[i][j-1] == "#":
            direct = direct_dict[direct]
            mark_turn = True
        else:
            break
    return direct, mark_turn

def move_a_step(index,direct,map):
    i = index[0]
    j = index[1]
    end_move = False
    if final_step_check(index,direct):
        end_move = True
        direct_new = direct
        index_new = index
        index_old = index
        mark_turn = False
    else:
        direct_new, mark_turn = find_direct(index,direct,map)
        index_old = index
        if direct_new == 1:
            index_new = [i-1, j]
        if direct_new == 2:
            index_new = [i, j+1]
        if direct_new == 3:
            index_new = [i+1, j]
        if direct_new == 4:
            index_new = [i, j-1]
    return index_new, direct_new, end_move, mark_turn, index_old

def add_obstacle(map,i,j):
    map_new = replace_char_at_index(map, i, j, "#")
    return map_new

def check_list_in_set(list_name, set_name):
    for sublist in set_name:
        if list_name == sublist:
            return True
    return False

file_path = "/Users/boxu/Dev/aoc 2024/day_6_input.txt"
with open(file_path, 'r') as file:
    maxtrix = file.read()
map = maxtrix.split("\n")

width_NS = len(map)
width_WE = len(map[0])

for i, string in enumerate(map):
    if "^" in string:
        index_start = [i,string.index("^")]

path = set()
turn = set()

end_move = False
index = index_start[:]
direct = 1
while end_move == False:
    index, direct, end_move, mark_turn, index_old = move_a_step(index,direct,map)
    path.add(tuple(index))
    if mark_turn:
        turn.add(tuple(index_old))

#print(path)
#print(turn)
#print(len(path))

for index in path:
    i = index[0]
    j = index[1]
    map = replace_char_at_index(map, i, j, "X")
map_view = "\n".join(map)
#print(map_view)

success_spot = 0
for ob_index in path:
    i = ob_index[0]
    j = ob_index[1]
    if ob_index != index_start:
        map_new = add_obstacle(map,i,j)

        turn = set()
        end_move = False
        index = index_start[:]
        direct = 1
        step_count = 0
        while end_move == False:
            index, direct, end_move, mark_turn,index_old = move_a_step(index,direct,map_new)
            step_count += 1
            index_str = ','.join(str(num) for num in index_old)
            if mark_turn:
                if index_str in turn:
                    success_spot += 1
                    end_move = True
                else:
                    turn.add(index_str)
        print(ob_index,success_spot,step_count)
