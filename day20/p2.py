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

def tile_flip_h(tile):
    new_tile = []
    for row in tile:
        new_tile.append(reverse(row))
    return new_tile

def tile_flip_v(tile):
    return list(reversed(tile))

# Edge order is TOP, BOTTOM, LEFT, RIGHT
def get_edges_from_id(tile_id):
    return get_edges(tiles[tile_id])
def get_edges(tile_data):
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
        edges = get_edges_from_id(tile_id)
        for e in edges:
            if e == edge or e == backwards:
                return True


# finding corners should be easy assuming what the description said is true about 
# outer edges not matching any other tiles
corner_ids = []
side_ids = []
mid_ids = []

for tile_id in tiles:
    good_edges = 0
    edges = get_edges_from_id(tile_id)
    for e in edges:
        if matching_edge_exists(e, tile_id):
            good_edges += 1

    if good_edges == 4:
        mid_ids.append(tile_id)
    elif good_edges == 2:
        print("Corner found! " + str(tile_id))
        corner_ids.append(tile_id)
    elif good_edges == 3:
        side_ids.append(tile_id)

# Now I want to assemble the puzzle
# I'll start with the first corner in the top left and attach 10 edges to the right by finding an edge with a matching side
# RN I'm assuming all matching sides are unique pairs which isn't necessarily the case
# but if it is it means I dont have to care the orientation of the sides that match
# though I still need to get the orientation of the match to place the piece in the image

first_corner = tiles[corner_ids.pop()]
edges = get_edges(first_corner)

