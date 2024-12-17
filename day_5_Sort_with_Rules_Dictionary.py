rule_book = {}
manual_list = []

file_path = "/Users/boxu/Dev/aoc 2024/day_5_input.txt"
with open(file_path, 'r') as file:
    for line in file:
        if line != "\n":
            if "|" in line:
                a, b = line.split("|")
                rule_book.setdefault(int(a), set())
                rule_book[int(a)].add(int(b))
            else:
                line_str = line.strip().split(",")
                line_num = [int(x) for x in line_str]
                manual_list.append(line_num)

M_page_sum = 0
manual_inc = []
for manual in manual_list:
    score = 0
    N = len(manual)
    for i in range (0,N-1):
        for j in range (i+1, N):
            if manual[i] in rule_book.get(manual[j],set()):
                score += 1
            else:
                score += 0
    if score == 0:
        M_page_sum += manual[int((N-1)/2)]
    else:
        manual_inc.append(manual)
#print(M_page_sum)

print(manual_inc)
M_page_c_sum = 0
for manual in manual_inc:
    i = len(manual)-1
    while i > 0:
        if manual[i] in rule_book.keys():
            j = i - 1
            while j >= 0:
                if manual[j] in rule_book.get(manual[i], set()):
                    manual[i], manual[j] = manual[j], manual[i]
                else:
                    j -= 1
            i -= 1
        else:
            i -= 1
    print(manual)
    M_page_c_sum += manual[int((len(manual)-1)/2)]

print(M_page_c_sum)