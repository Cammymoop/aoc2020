import sys

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

def move(char, prev, x, y):
    if char == "n":
        return x, y - 1
    elif char == "s":
        return x, y + 1
    elif char == "w" and prev != "s":
        return x - 1, y
    elif char == "e" and prev != "n":
        return x + 1, y
    return x, y


grid = {}
smallest_x = 0
smallest_y = 0
biggest_x = 0
biggest_y = 0

for row in rows:
    x = 0
    y = 0

    previous = 'b'
    for char in row:
        x, y = move(char, previous, x, y)
        previous = char

    coord = (x, y)
    if coord not in grid:
        grid[coord] = True
    else:
        grid[coord] = not grid[coord]

    biggest_x = max(biggest_x, x)
    biggest_y = max(biggest_y, y)
    smallest_x = min(smallest_x, x)
    smallest_y = min(smallest_y, y)

def count_neighbors(x, y):
    neighbors = 0
    x_offsets = [0, 0, -1, 1, -1, 1] 
    y_offsets = [-1, 1, 0, 0, -1, 1] 
    for i in range(len(x_offsets)):
        coord = (x + x_offsets[i], y + y_offsets[i])
        if coord in grid and grid[coord] == True:
            neighbors += 1
    return neighbors

def next_gen():
    global grid, smallest_x, smallest_y, biggest_x, biggest_y
    new_grid = {}
    for j in range(smallest_y - 1, biggest_y + 2):
        for i in range(smallest_x - 1, biggest_x + 2):
            coord = (i, j)
            n = count_neighbors(i, j)
            got_set = False
            if coord not in grid or grid[coord] != True:
                if n == 2:
                    new_grid[coord] = True
                    got_set = True
            elif n == 1 or n == 2:
                new_grid[coord] = True
                got_set = True

            if got_set:
                biggest_x = max(biggest_x, i)
                biggest_y = max(biggest_y, j)
                smallest_x = min(smallest_x, i)
                smallest_y = min(smallest_y, j)

    grid = new_grid


def count_tiles():
    flipped_tiles = 0
    for coord in grid:
        if grid[coord]:
            flipped_tiles += 1
    return flipped_tiles

for gen in range(100):
    next_gen()

print("There are now " + str(count_tiles()) + " flipped hexes")

