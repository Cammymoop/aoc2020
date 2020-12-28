import sys
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

grid = []
for row in raw_rows:
    grid.append(row.strip())

WIDTH = len(grid[0])
HEIGHT = len(grid)

# now need to keep searching in each of the 8 directions until a seat is there (not ".")
def count_occupied_neighbors(x, y):
    x_offs = [-1, 0, 1]
    y_offs = [-1, 0, 1]

    occupied = 0
    for y_off in y_offs:
        for x_off in x_offs:
            if x_off == 0 and y_off == 0:
                continue
            i = x + x_off
            j = y + y_off
            while True:
                # Reached the edge of the grid
                if i < 0 or j < 0 or i > WIDTH - 1 or j > HEIGHT - 1:
                    break

                if grid[j][i] == '#':
                    occupied += 1
                    break
                elif grid[j][i] == 'L':
                    break
                
                i += x_off
                j += y_off
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
            elif cell == "#" and neighbors >= 5:
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
