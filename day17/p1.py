import sys

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

loops = 6

x_min = -loops
y_min = -loops
z_min = -loops

x_max = len(rows[0]) + loops
y_max = len(rows) + loops
z_max = 1 + loops

# Initialize an empty grid (nested dicts)
grid = {}
for z in range(z_min, z_max):
    z_plane = {}
    for y in range(y_min, y_max):
        y_row = {}
        for x in range(x_min, x_max):
            y_row[x] = 0
        z_plane[y] = y_row
    grid[z] = z_plane


def print_plane(plane, grid):
    print("=" * (loops * 2 + len(rows[0])))
    for y in range(y_min, y_max):
        s = ""
        for x in range(x_min, x_max):
            s += "@" if grid[plane][y][x] == 1 else "·"
        print(s)
    print("=" * (loops * 2 + len(rows[0])))


# Load initial state from input
y = 0
for row in rows:
    for x in range(len(row)):
        grid[0][y][x] = 1 if row[x] == "#" else 0
    y += 1

print("Grid loaded, 0 Z plane:")
print_plane(0, grid)

def count_neighbors(x, y, z, grid):
    neighbors = 0
    xa, xb = (max(x_min, x - 1), min(x_max, x + 2))
    ya, yb = (max(y_min, y - 1), min(y_max, y + 2))
    za, zb = (max(z_min, z - 1), min(z_max, z + 2))
    for z_ in range(za, zb):
        for y_ in range(ya, yb):
            for x_ in range(xa, xb):
                neighbors += grid[z_][y_][x_]
    return neighbors - grid[z][y][x]


def next_stage(grid):
    new_grid = {}
    for z in range(z_min, z_max):
        z_plane = {}
        for y in range(y_min, y_max):
            y_row = {}
            for x in range(x_min, x_max):
                neighbors = count_neighbors(x, y, z, grid)
                if z == 0 and y == 1 and x == 6:
                    print("z0y1x6 neighbors: " + str(neighbors) + ", currently: " + ("on" if grid[z][y][x] == 1 else "off"))
                if neighbors == 3:
                    y_row[x] = 1
                elif neighbors == 2 and grid[z][y][x] == 1:
                    y_row[x] = 1
                else:
                    y_row[x] = 0
            z_plane[y] = y_row
        new_grid[z] = z_plane
    return new_grid

def count_active_cells(grid):
    active = 0
    for z in range(z_min, z_max):
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                active += grid[z][y][x]
    return active

for i in range(loops):
    grid = next_stage(grid)
    if i == 0:
        print("second stage Z -1 plane:")
        print_plane(-1, grid)
        print("Z 0 plane:")
        print_plane(0, grid)

print("After 6 stages there are " + str(count_active_cells(grid)) + " cells active")

print("0 Z plane:")
print_0_plane(grid)
