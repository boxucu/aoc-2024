import re


# Na*ax + Nb*bx = px
# Na*ay + Nb*by = py
def solve_matrix(ax, ay, bx, by, px, py):
    # find the inverse matrix
    a1 = ax
    b1 = bx
    c1 = ay
    d1 = by

    det = a1 * d1 - b1 * c1
    if det == 0:
        if c1 * px != a1 * py:
            Na = -1
            Nb = -1
            solvable = False
        else:
            Na = -1
            Nb = -1
            solvable = True
            while Nb < 100:
                Nb += 1
                A = px - b1 * Nb
                if A % a1 == 0:
                    Na = A // a1
                    break
                else:
                    Na = A / a1

    else:
        # inverse matrix
        a2 = d1 / det
        b2 = -b1 / det
        c2 = -c1 / det
        d2 = a1 / det

        Na = a2 * px + b2 * py
        Nb = c2 * px + d2 * py
        solvable = True

    # check if Na and Nb are in range and are integers
    rel_tol = 1e-3
    if Na > 100 or Nb > 100:
        solvable = False
    elif Na < 0 or Nb < 0:
        solvable = False
    elif abs(Na - round(Na)) > rel_tol or abs(Nb - round(Nb)) > rel_tol:
        solvable = False

    # print(Na, Nb, solvable)
    return Na, Nb, solvable


def solve_matrix_corrected(ax, ay, bx, by, px, py):
    # find the inverse matrix
    px += 10000000000000
    py += 10000000000000

    a1 = ax
    b1 = bx
    c1 = ay
    d1 = by

    det = a1 * d1 - b1 * c1
    if det == 0:
        if c1 * px != a1 * py:
            Na = -1
            Nb = -1
            solvable = False
        else:
            Na = -1
            Nb = -1
            solvable = True
            while Nb < px//b1:
                Nb += 1
                A = px - b1 * Nb
                if A % a1 == 0:
                    Na = A // a1
                    break
                else:
                    Na = A / a1

    else:
        # inverse matrix
        a2 = d1 / det
        b2 = -b1 / det
        c2 = -c1 / det
        d2 = a1 / det

        Na = a2 * px + b2 * py
        Nb = c2 * px + d2 * py
        solvable = True

    # check if Na and Nb are in range and are integers
    rel_tol = 1e-3
    if Na < 0 or Nb < 0:
        solvable = False
    elif abs(Na - round(Na)) > rel_tol or abs(Nb - round(Nb)) > rel_tol:
        solvable = False

    # print(Na, Nb, solvable)
    return Na, Nb, solvable


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day_13_input.txt"
    with open(file_path, "r") as file:
        description = file.read()

    # extract the parameters from the machine description
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\s+Button B: X\+(\d+), Y\+(\d+)\s+Prize: X=(\d+), Y=(\d+)"
    matches = re.findall(pattern, description)

    # solve for each machine
    N_price = 0
    N_token = 0

    for match in matches:
        ax, ay, bx, by, px, py = (int(x) for x in match)
        #Na, Nb, solvable = solve_matrix(ax, ay, bx, by, px, py)
        Na, Nb, solvable = solve_matrix_corrected(ax, ay, bx, by, px, py)
        if solvable:
            N_price += 1
            N_token += 3*Na + Nb

    print(N_price, N_token)


if __name__ == "__main__":
    main()
