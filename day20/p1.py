import sys
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

tile_data_rows = []
tile_ids = []
for row in rows:
    if len(row) == 0:
        continue
    if row.find("Tile") == 0:
        tile_ids.append(int(row[5:].strip(':')))
        continue

    tile_data_rows.append(row)

tiles = {}
for i in range(len(tile_data_rows)):
    ti = i//10
    tile_id = tile_ids[ti]
    if i % 10 == 0:
        tiles[tile_id] = []
    tiles[tile_id].append(tile_data_rows[i])

# Various functions
def reverse(s):
    new_s = ""
    for c in s:
        new_s = c + new_s
    return new_s

def get_edges(tile_id):
    tile_data = tiles[tile_id]
    edges = [tile_data[0], tile_data[9], "", ""]
    for i in range(10):
        edges[2] += tile_data[i][0]
        edges[3] += tile_data[i][9]
    return edges

def matching_edge_exists(edge, from_id):
    backwards = reverse(edge)
    for tile_id in tiles:
        if tile_id == from_id:
            continue
        edges = get_edges(tile_id)
        for e in edges:
            if e == edge or e == backwards:
                return True


# finding corners should be easy assuming what the description said is true about 
# outer edges not matching any other tiles
corner_ids = []

corner_count = 0
side_count = 0
mid_count = 0

for tile_id in tiles:
    good_edges = 0
    edges = get_edges(tile_id)
    for e in edges:
        if matching_edge_exists(e, tile_id):
            good_edges += 1

    if good_edges == 4:
        mid_count += 1
    elif good_edges == 1:
        print("1 connected edge???")
    elif good_edges == 2:
        print("Corner found! " + str(tile_id))
        corner_ids.append(tile_id)
        corner_count += 1
    elif good_edges == 3:
        side_count += 1
    elif good_edges == 0:
        print("0 connected edges :o ???")
    else:
        print(str(good_edges) + " connected edges!!!")

print("Piece counts, corners: {}, sides: {}, middles: {}".format(corner_count, side_count, mid_count))
print("Corners: " + str(corner_ids))
print("Corner product: " + str(reduce(lambda acc, x: acc * x, corner_ids, 1)))

