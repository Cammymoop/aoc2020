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


flipped = {}

for row in rows:
    x = 0
    y = 0

    previous = 'b'
    for char in row:
        x, y = move(char, previous, x, y)
        previous = char

    coord = (x, y)
    if coord not in flipped:
        flipped[coord] = True
    else:
        flipped[coord] = not flipped[coord]

flipped_tiles = 0
for coord in flipped:
    if flipped[coord]:
        flipped_tiles += 1

print("There are now " + str(flipped_tiles) + " flipped hexes")

