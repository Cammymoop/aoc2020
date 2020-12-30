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

def tile_transpose(tile):
    new_tile = []
    for i in range(len(tile[0])):
        new_tile.append(reduce(lambda acc, x: acc + x[i], tile, ""))
    return new_tile

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
    return matching_edge_exists_in(edge, from_id, tile_ids)
def matching_edge_exists_in(edge, from_id, ids):
    backwards = reverse(edge)
    for tile_id in ids:
        if tile_id == from_id:
            continue
        edges = get_edges_from_id(tile_id)
        for e in edges:
            if e == edge or e == backwards:
                return True
    return False

def which_sides_are_edges(tile_data, from_id):
    edges = get_edges(tile_data)
    sides = []
    for e in edges:
        sides.append(not matching_edge_exists(e, from_id))
    return sides

# given an edge and a tile id, find the matching edge in the tile if it exists
# return the edge index (TOP, BOTTOM, LEFT, RIGHT) and whether or not it needs to be flipped
# if it doesn't match at all return -1
def find_matching_edge_and_flip(edge, tile_id):
    backwards = reverse(edge)
    check_edges = get_edges_from_id(tile_id)
    for i in range(4):
        if check_edges[i] == edge:
            return i, False
        if check_edges[i] == backwards:
            return i, True
    return -1, False


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

# Ok ok matching edges arent unique, gotta actually put it together like a jigsaw puzzle

########################################
# Just the top left corner

first_tid = corner_ids.pop()
first_corner = tiles[first_tid]
edges = get_edges(first_corner)

if matching_edge_exists(edges[0], first_tid):
    first_corner = tile_flip_v(first_corner)

edges = get_edges(first_corner)
if matching_edge_exists(edges[2], first_tid):
    first_corner = tile_flip_h(first_corner)

tile_bag = tile_ids.copy()
tile_bag.remove(first_tid)

# Ok got first corner set up, now just start attaching on side pieces where they match left
# I need to get 10 side pieces that match where one of the corners also matches on the end
# I'm going to assume if I find a set of sides/corner that work then they are the only ones that can go there

########################################
# Top row of puzzle

G_WIDTH = 12
G_MAX = G_WIDTH - 1
sides = G_WIDTH - 2

empty_row = [False] * G_WIDTH
semifinal_picture = []
for i in range(G_WIDTH):
    semifinal_picture.append(empty_row.copy())

def coord_type(x, y):
    sides = 0
    if x == 0 or x == G_WIDTH - 1:
        sides += 1
    if y == 0 or y == G_WIDTH - 1:
        sides += 1
    return "mid" if sides == 0 else ("side" if sides < 2 else "corner")

def type_matches_coord(tile_id, x, y):
    c_type = coord_type(x, y)
    if tile_id in corner_ids:
        return c_type == "corner"
    if tile_id in side_ids:
        return c_type == "side"
    return c_type == "mid"

def opposite(a, b):
    return a + b == 5 or a + b == 1

def perpendicular(a, b):
    if a > b:
        b, a = a, b
    return b > 1 and a < 2

def find_piece(coords):
    x, y = coords
    needed_matches = {}
    if x == 0 or semifinal_picture[y][x - 1] != False:
        needed_matches[2] = "side" if x == 0 else get_edges(semifinal_picture[y][x - 1])[3]
    if y == 0 or semifinal_picture[y - 1][x] != False:
        needed_matches[0] = "side" if y == 0 else semifinal_picture[y - 1][x][-1]

    if x == G_WIDTH - 1 or semifinal_picture[y][x + 1] != False:
        needed_matches[3] = "side" if x == G_WIDTH - 1 else get_edges(semifinal_picture[y][x + 1])[2]
    if y == G_WIDTH - 1 or semifinal_picture[y + 1][x] != False:
        needed_matches[1] = "side" if y == G_WIDTH - 1 else semifinal_picture[y + 1][x][0]

    found = False
    correct_type_but_no = 0
    for side in needed_matches:
        edge_to_check = needed_matches[side]
        if edge_to_check == "side":
            continue
        for tid in tile_bag:
            if not type_matches_coord(tid, x, y):
                continue
            edge_i, flip = find_matching_edge_and_flip(edge_to_check, tid)
            if edge_i < 0:
                correct_type_but_no += 1
                continue

            next_tile = tiles[tid]
            o = 2 if side > 1 else 0
            if perpendicular(edge_i, side):
                next_tile = tile_transpose(next_tile)
                edge_i = edge_i + 2 % 4
            if opposite(edge_i, side):
                if not flip:
                    if side > 1:
                        next_tile = tile_flip_h(next_tile)
                    else:
                        next_tile = tile_flip_v(next_tile)
                else:
                    next_tile = tile_flip_h(next_tile)
                    next_tile = tile_flip_v(next_tile)
                edge_i = (edge_i + 1 % 2) + o
            elif flip:
                if side > 1:
                    next_tile = tile_flip_v(next_tile)
                else:
                    next_tile = tile_flip_h(next_tile)


            good = True
            new_edges = get_edges(next_tile)
            for side2 in needed_matches:
                if side == side2:
                    continue
                edge_to_check2 = needed_matches[side2]
                if edge_to_check2 == "side":
                    if matching_edge_exists(new_edges[side2], tid):
                        print("Was supposed to be a side but wasnt " + str(side2))
                        good = False
                        break
                elif edge_to_check2 != new_edges[side2]:
                    print("Was supposed to be " + edge_to_check2 + " but was " + new_edges[side2] + " side " + str(side2))
                    good = False
                    break

            if not good:
                print("checking all sides failed, heres which sides are edges: " + str(which_sides_are_edges(next_tile, tid)))
                continue

            # Found a matching tile!
            return tid, next_tile

        # No tiles found? (shouldn't be happening)
        print("Ok I didnt find any tiles to put here... " + str(correct_type_but_no))
        print(coord)
        print(needed_matches)
        break
    print("shouldnt be here at the end of find_tile")

def diagonal_coord_generator(diagonal):
    a = max(diagonal - G_MAX, 0)
    coords = []
    limit = min(diagonal, G_MAX)
    while a <= limit:
        coords.append((a, diagonal - a))
        a += 1
    return coords

def print_filled_tiles():
    print("/" + ("-" * G_WIDTH) + "\\")
    for row in semifinal_picture:
        row_str = reduce(lambda acc, x: acc + ("·" if x == False else "X"), row, "")
        print("|" + row_str + "|")
    print("\\" + ("-" * G_WIDTH) + "/")

semifinal_picture[0][0] = first_corner
for diagonal in range(1, 23):
    print("diagonal: " + str(diagonal))
    print_filled_tiles()
    coords_to_put = diagonal_coord_generator(diagonal)
    for coord in coords_to_put:
        tile_id, tile_data = find_piece(coord)
        x, y = coord
        tile_bag.remove(tile_id)
        semifinal_picture[y][x] = tile_data


# Ok my 3rd or so attempt at putting the puzzle together worked lol
# Now to strip the borders and output the resulting image

t1 = 1
t2 = len(tiles[tile_ids[0]][0]) - 1
strings = t2 - t1

final_picture = []
for row in semifinal_picture:
    strings = []
    for row_i in range(t1, t2):
        acc = ""
        for tile in row:
            acc += tile[row_i][t1:t2]
        strings.append(acc)
    for s in strings:
        final_picture.append(s)

print(["Assembled pic", len(final_picture[0]), len(final_picture)])

for transpose in range(1):
    for flip_h in range(1):
        for flip_v in range(1):
            pic_copy = final_picture.copy()
            if transpose > 0:
                pic_copy = tile_transpose(pic_copy)
            if flip_h > 0:
                pic_copy = tile_flip_h(pic_copy)
            if flip_v > 0:
                pic_copy = tile_flip_v(pic_copy)



