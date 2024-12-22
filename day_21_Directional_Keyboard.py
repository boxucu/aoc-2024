import re

from dataclasses import dataclass


@dataclass(frozen=True)
class Digit:
    char: str
    path: str


# based on the current digit, expand to new frontier with the lowest increase in score
def update_frontier(frontier_set, visited_set, directional_rule):
    # first, choose the digit within the frontier_set that has the smallest score
    lowest_score = 10**10
    for digit in frontier_set:
        score = len(digit.path)
        if score < lowest_score:
            lowest_score = score
            path = digit.path
            replaced_digit = digit

    # then remove the lowset score digit from frontier_set
    frontier_set.remove(replaced_digit)

    nextstep_set = set()
    # find the set of next step digits for this replaced tile
    for start, end in directional_rule:
        if start == replaced_digit.char:
            new_path = path + directional_rule[(start, end)]
            nextstep_set.add(Digit(end, new_path))

    new_step_set = set()
    visited_char_set = set()
    for digit in visited_set:
        visited_char_set.add(digit.char)

    for digit in nextstep_set:
        # if next step is not already visited, add
        if digit.char not in visited_char_set:
            new_step_set.add(digit)
        # if the next step lead us to a visited spot but now with a smaller score, add
        else:
            # find the visited score of (i, j)
            for visited_digit in visited_set:
                if visited_digit.char == digit.char:
                    visited_score = len(visited_digit.path)
            if score <= visited_score:
                new_step_set.add(digit)

    for digit in new_step_set:
        frontier_set.add(digit)
        visited_set.add(digit)

    return frontier_set, visited_set


# find the shortest path from a digit to the next digit based on the directional_rule dictionary
def shortest_path(current_char, next_char, directional_rule):
    visited_set = set()
    visited_set.add(Digit(current_char, ""))
    frontier_set = visited_set.copy()

    while True:
        frontier_set, visited_set = update_frontier(
            frontier_set, visited_set, directional_rule
        )
        # if no more frontier to explore, break
        if len(frontier_set) == 0:
            break

    # find the length of shortest path
    smallest_score = 10**10
    for visited_digit in visited_set:
        if visited_digit.char == next_char:
            score = len(visited_digit.path)
            if score <= smallest_score:
                smallest_score = score
            else:
                pass

    # find all the shortest paths
    shortest_paths = set()
    for visited_digit in visited_set:
        if visited_digit.char == next_char:
            score = len(visited_digit.path)
            if score == smallest_score:
                shortest_paths.add(visited_digit.path)
    # print(shortest_paths)

    return shortest_paths


# from num_pad character to directional keypad characters
def code_to_dk(code):
    num_pad = ["789", "456", "123", "X0A"]
    directional_rule = {}
    directions = [">", "^", "<", "v"]
    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]

    for i in range(0, len(num_pad)):
        for j in range(0, len(num_pad[0])):
            start = num_pad[i][j]
            for next_direct in range(0, 4):
                (di, dj) = didj[next_direct]
                if (
                    i + di < 0
                    or i + di >= len(num_pad)
                    or j + dj < 0
                    or j + dj >= len(num_pad[0])
                ):
                    pass
                elif start == "X" or num_pad[i + di][j + dj] == "X":
                    pass
                else:
                    directional_rule[(start, num_pad[i + di][j + dj])] = directions[
                        next_direct
                    ]

    # for (start, end) in directional_rule:
    #     print(start,"->",end,"uses a move of",directional_rule[(start,end)])

    current_char = "A"
    paths = {""}
    for next_char in code:
        shortest_paths = shortest_path(current_char, next_char, directional_rule)
        path_update = set()
        for path_now in paths:
            for path_add in shortest_paths:
                path_update.add(path_now + path_add + "A")
        paths = path_update.copy()
        current_char = next_char

    return paths


# from directional keypad character to directional keypad characters
def dk_to_dk(code):
    num_pad = ["X^A", "<v>"]
    directional_rule = {}
    directions = [">", "^", "<", "v"]
    didj = [
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0),
    ]

    for i in range(0, len(num_pad)):
        for j in range(0, len(num_pad[0])):
            start = num_pad[i][j]
            for next_direct in range(0, 4):
                (di, dj) = didj[next_direct]
                if (
                    i + di < 0
                    or i + di >= len(num_pad)
                    or j + dj < 0
                    or j + dj >= len(num_pad[0])
                ):
                    pass
                elif start == "X" or num_pad[i + di][j + dj] == "X":
                    pass
                else:
                    directional_rule[(start, num_pad[i + di][j + dj])] = directions[
                        next_direct
                    ]

    # for (start, end) in directional_rule:
    #     print(start,"->",end,"uses a move of",directional_rule[(start,end)])

    current_char = "A"
    paths = {""}
    for next_char in code:
        shortest_paths = shortest_path(current_char, next_char, directional_rule)
        path_update = set()
        for path_now in paths:
            for path_add in shortest_paths:
                path_update.add(path_now + path_add + "A")
        paths = path_update.copy()
        current_char = next_char

    return paths


def directional_keypads_layer(code_set):
    shortest_path_length = 10**10
    paths_set = set()
    for code in code_set:
        paths = dk_to_dk(code)
        paths_set = paths_set.union(paths)
        for path in paths:
            path_length = len(path)
            break
        if path_length < shortest_path_length:
            shortest_path_length = path_length

    new_code_set = set()
    for path in paths_set:
        if len(path) == shortest_path_length:
            new_code_set.add(path)

    return new_code_set, shortest_path_length


def encode_part1(code):
    code_set = code_to_dk(code)
    layer = 0
    while layer < 2:
        code_set, shortest_path_length = directional_keypads_layer(code_set)
        layer += 1
        # print(code_set)
        print(
            "After",
            layer,
            "layers of directional keypads, the shortest code length is",
            shortest_path_length,
        )

    # find a shortest translated code:
    shortest_length = 10**10
    for new_code in code_set:
        if len(new_code) < shortest_length:
            shortest_length = len(new_code)

    number_str = re.findall(r"\d+", code)
    number = int("".join(number_str))
    score = number * shortest_length

    return score


def encode_part2(code):
    code_set = code_to_dk(code)
    code_set, shortest_path_length = directional_keypads_layer(code_set)
    # print("At second robot, the shortest code length is",shortest_path_length,)

    # also return the value of the num_pad code
    number_str = re.findall(r"\d+", code)
    number = int("".join(number_str))

    return number, code_set


def create_trans_dict():
    # from direcitonal keyboard to direcitonal keyboard, the possible codes for one move is limited:
    move_2_next_move = {
    (">^>A", "vA<^Av>A^A"),
    (">>^A", "vAA<^A>A"),
    ("<vA", "v<<A>A^>A"),
    ("^<A", "<Av<A>>^A"),
    ("v<<A", "<vA<AA>>^A"),
    (">^A", "vA<^A>A"),
    ("vA", "<vA^>A"),
    (">>A", "vAA^A"),
    ("^>A", "<Av>A^A"),
    ("<A", "v<<A>>^A"),
    ("<v<A", "v<<A>A<A>>^A"),
    (">vA", "vA<A^>A"),
    ("<<A", "v<<AA>>^A"),
    ("v>A", "<vA>A^A"),
    ("^A", "<A>A"),
    ("A", "A"),
    (">A", "vA^A"),
    ("v<A", "<vA<A>>^A"),
    ("<^A", "v<<A>^A>A"),
    }

    next_layer_dict = {}
    for (move, next_move) in move_2_next_move:
        code_split = next_move.split("A")
        code_split.pop()
        for str_element in code_split:
            move2 = str_element + "A"
            if (move, move2) in next_layer_dict:
                next_layer_dict[(move, move2)] += 1
            else:
                next_layer_dict[(move, move2)] = 1

    return next_layer_dict


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_21_input.txt"
    with open(file_path, "r") as file:
        description = file.read()
    code_list = description.split("\n")

    score_total = 0
    # for code in code_list:
    #     score = encode_part1(code)
    #     score_total += score
    #     print(code, score)
    #     break

    next_layer_dict = create_trans_dict()
    for code in code_list:
        number, code_2_set = encode_part2(code)
        # number is what the num_pad code value is
        # code_2 are what the second robot from the num_pad is typing

        code_length_set = set()
        for code_2 in code_2_set:
            # decompose code 2:
            code_2_dict = {}
            code_2_split = code_2.split("A")
            code_2_split.pop()
            for str_element in code_2_split:
                code_move = str_element + "A"
                if code_move in code_2_dict:
                    code_2_dict[code_move] += 1
                else:
                    code_2_dict[code_move] = 1
            # print(code_2, code_2_dict)

            used_dk_layer = 2
            while used_dk_layer < 26:
                # calculate one layer
                code_3_dict = {}
                for code_move in code_2_dict:
                    for move, next_move in next_layer_dict:
                        if move == code_move:
                            if next_move in code_3_dict:
                                code_3_dict[next_move] += (
                                    code_2_dict[code_move]
                                    * next_layer_dict[(move, next_move)]
                                )
                            else:
                                code_3_dict[next_move] = (
                                    code_2_dict[code_move]
                                    * next_layer_dict[(move, next_move)]
                                )
                code_2_dict = code_3_dict.copy()
                used_dk_layer += 1

            # calculate code_3 length
            code_length = 0
            for code_move in code_3_dict:
                code_length += len(code_move) * code_3_dict[code_move]
            code_length_set.add(code_length)

        score = number * min(code_length_set)
        print("the complexities of code", code, "is", score)
        score_total += score

    print("The sum of the complexities of the five codes is", score_total)


if __name__ == "__main__":
    main()
