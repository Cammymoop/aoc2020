import sys
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

grid = []
for row in raw_rows:
    grid.append(row.strip())

WIDTH = len(grid[0])
HEIGHT = len(grid)

def count_occupied_neighbors(x, y):
    x_1 = max(x - 1, 0)
    x_2 = min(x + 2, WIDTH)
    y_1 = max(y - 1, 0)
    y_2 = min(y + 2, HEIGHT)

    occupied = 0
    for j in range(y_1, y_2):
        for i in range(x_1, x_2):
            if i < 0 or j < 0 or i > WIDTH - 1 or j > HEIGHT - 1:
                print("Oops I messed up the coords" + str([(x_1, x_2), (y_1, y_2), i, j]))
            if i == x and j == y:
                continue
            if grid[j][i] == '#':
                occupied += 1
    return occupied


new_grid = []

finished = False
infinite_protection = 10000

while not finished:
    infinite_protection -= 1
    if infinite_protection < 0:
        print("Infinite protection activate!")
        sys.exit()

    change = False
    for y in range(HEIGHT):
        new_row = ""
        for x in range(WIDTH):
            cell = grid[y][x]
            if cell == ".":
                new_row += "."
                continue

            neighbors = count_occupied_neighbors(x, y)
            if cell == "L" and neighbors == 0:
                change = True
                new_row += "#"
            elif cell == "#" and neighbors >= 4:
                change = True
                new_row += "L"
            else:
                new_row += cell

        new_grid.append(new_row)

    if not change:
        finished = True

    grid = new_grid
    new_grid = []

print("simulated " + str(10000 - infinite_protection) + " generations")

total_filled = reduce(lambda acc, row: acc + row.count('#'), grid, 0)

print(str(total_filled) + " seats are filled")
