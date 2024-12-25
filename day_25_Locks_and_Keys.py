def extract_lock_key(lines):
    lock_set = set()
    key_set = set()
    translation_table = str.maketrans({"#": "1", ".": "0"})
    for i in range(0, len(lines), 8):
        if i + 6 < len(lines):
            total = 0
            # identify lock
            if lines[i][0] == "#":
                for index in range(i + 1, i + 7):
                    line = lines[index].strip()
                    row = line.translate(translation_table)
                    total += int(row)
                lock = f"{total:05d}"
                lock_set.add(lock)
            # identify key
            elif lines[i][0] == ".":
                for index in range(i, i + 6):
                    line = lines[index].strip()
                    row = line.translate(translation_table)
                    total += int(row)
                key = f"{total:05d}"
                key_set.add(key)
        else:
            pass  # out of range
    return lock_set, key_set


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_25_input.txt"
    with open(file_path, "r") as file:
        lines = file.readlines()

    lock_set, key_set = extract_lock_key(lines)
    # print(lock_set)
    # print(key_set)

    fit_count = 0
    for lock in lock_set:
        for key in key_set:
            misfit = [max(0, int(a) + int(b) - 5) for a, b in zip(lock, key)]
            if sum(misfit) == 0:
                fit_count += 1
    print(
        "Number of unique lock/key pairs that fit together without overlapping in any column is",
        fit_count,
    )


if __name__ == "__main__":
    main()
