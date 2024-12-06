cross_mas_count = 0
map = ["MAS","MAS","MAS"]
N = len(map[0])
for i in range (1,N-1):
    for j in range (1,N-1):
        if map[i][j] == "A":
            cross = map[i-1][j-1] + map[i+1][j+1] + map[i-1][j+1] + map[i+1][j-1]
            if cross == "MSMS" or cross == "MSSM" or cross == "SMMS" or cross == "SMSM":
                cross_mas_count += 1
print(cross_mas_count)
