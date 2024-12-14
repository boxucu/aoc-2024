import re


# for a given robot, find the location for it after N seconds
def locate_robot(x, y, vx, vy, Nx, Ny, Ns):
    x_after_Ns = (x + vx * Ns) % Nx
    y_after_Ns = (y + vy * Ns) % Ny

    return x_after_Ns, y_after_Ns


# for a given list of discription, return the robot location map with count after N seconds
def create_robot_map(description, Nx, Ny, Ns):
    # dict to store the location of robot and counts
    robot_map = {}

    # extract the parameters from the description
    pattern = r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)"
    matches = re.findall(pattern, description)

    for match in matches:
        x, y, vx, vy = map(int, match)
        xNs, yNs = locate_robot(x, y, vx, vy, Nx, Ny, Ns)
        if (xNs, yNs) in robot_map:
            robot_map[(xNs, yNs)] += 1
        else:
            robot_map[(xNs, yNs)] = 1

    return robot_map


# calculate the safety factor
def safety_factor_calc(robot_map, Nx, Ny):
    xhalf = Nx // 2
    yhalf = Ny // 2

    Nq1 = 0
    Nq2 = 0
    Nq3 = 0
    Nq4 = 0
    for x, y in robot_map:
        if x < xhalf and y < yhalf:
            Nq1 += robot_map[(x, y)]
        elif x < xhalf and y >= Ny - yhalf:
            Nq2 += robot_map[(x, y)]
        elif x >= Nx - xhalf and y < yhalf:
            Nq3 += robot_map[(x, y)]
        elif x >= Nx - xhalf and y >= Ny - yhalf:
            Nq4 += robot_map[(x, y)]

    return Nq1 * Nq2 * Nq3 * Nq4


def accumulation_check(point_set, tolerance):
    # Define the 8 possible neighbor directions
    directions = [
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    ]

    # A function to count neighbors for a given point
    def count_neighbors(x, y):
        count = 0
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in point_set:
                count += 1
        return count

    # Count the total number of points that have at least one neighbor
    neighbor_count = 0
    for x, y in point_set:
        if count_neighbors(x, y) > 0:  # If a point has neighbors
            neighbor_count += 1
            if neighbor_count > tolerance:  # Early exit if more than 20
                return True

    return False


# polt the unqiue spots in robot map
def map_polt(robot_map, Nx, Ny):
    grid = [["." for _ in range(Nx)] for _ in range(Ny)]
    for x, y in robot_map:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


def main_part1():
    file_path = "/Users/boxu/Dev/aoc 2024/day 14_input.txt"
    with open(file_path, "r") as file:
        description = file.read()

    # define the periodic boundary size
    Nx = 101  # wide
    Ny = 103  # tall
    Ns = 100  # second

    robot_map = create_robot_map(description, Nx, Ny, Ns)

    safety_factor = safety_factor_calc(robot_map, Nx, Ny)
    print(safety_factor)


def main():
    file_path = "/Users/boxu/Dev/aoc 2024/day 14_input.txt"
    with open(file_path, "r") as file:
        description = file.read()

    # define the periodic boundary size
    Nx = 101  # wide
    Ny = 103  # tall
    Ns = 0  # second

    # iterate seconds and looking for special looking ones
    while True:
        robot_map = create_robot_map(description, Nx, Ny, Ns)
        accumulation = accumulation_check(robot_map, 200)
        # map_polt(robot_map, Nx, Ny)
        if accumulation:
            map_polt(robot_map, Nx, Ny)
            print(Ns)
        elif Ns > 10000:
            break

        Ns += 1


if __name__ == "__main__":
    main()
