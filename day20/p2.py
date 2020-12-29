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

new_right = get_edges(first_corner)[3]
if not matching_edge_exists_in(new_right, first_tid, side_ids):
    print("no side attaches right?")

# Ok got first corner set up, now just start attaching on side pieces where they match left
# I need to get 10 side pieces that match where one of the corners also matches on the end
# I'm going to assume if I find a set of sides/corner that work then they are the only ones that can go there

########################################
# Top row of puzzle

final_picture = [first_corner]
initial_index = 1
max_index = 144
grid_width = 12
sides = grid_width - 2

def stick_row_together(top_bottom, acc, sides_left, depth):
    if len(acc) == 0:
        stick_to_tile = final_picture[0]
    else:
        stick_to_tile = acc[-1]
    stick_to_edge = get_edges(stick_to_tile)[3]

    is_corner_time = len(acc) == 0 or len(acc) == sides
    if top_bottom == "top" or top_bottom == "bottom":
        loop_through = corner_ids if is_corner_time else sides_left
    else:
        loop_through = corner_ids if is_corner_time else sides_left

    loops = 0
    for tid in loop_through:
        loops += 1
        edge_i, flip = find_matching_edge_and_flip(stick_to_edge, tid)
        if edge_i == -1:
            continue

        next_tile = tiles[tid]
        if edge_i == 1:
            next_tile = tile_flip_v(next_tile)
        elif edge_i == 3:
            next_tile = tile_flip_h(next_tile)
        if edge_i == 0 or edge_i == 1:
            next_tile = tile_transpose(next_tile)

        if flip:
            next_tile = tile_flip_v(next_tile)

        if top_bottom == "top":
            top = next_tile[0]
            if matching_edge_exists(top, tid):
                # Matched a side piece but in the wrong orientation to be a side/corner
                e = get_edges_from_id(tid)
                continue

        # update row and sides/corners left
        new_acc = acc.copy()
        new_acc.append(next_tile)
        new_sides_left = sides_left.copy()
        if is_corner_time:
            new_corners_left = corner_ids
            new_corners_left.remove(tid)
            # Dont recurse this is the far corner
            print("Top row completed, collapsing recurse")
            return new_acc, new_sides_left, new_corners_left
        else:
            new_sides_left.remove(tid)

        # valid match, recurse to see if the whole row matches after it
        print("side found going into depth " + str(depth + 1))
        res_acc, res_sides, res_corners = stick_top_edge(new_acc, new_sides_left, depth + 1)
        if len(res_acc) == 0:
            # No valid row after this tile
            print("back to depth " + str(depth) + " continuing to look for new matches")
            continue
        else:
            # Found a valid row, assume the first valid row is correct
            print("collapsing recurse, depth = " + str(depth))
            return res_acc, res_sides, res_corners

    # No valid tiles left
    print("No matches, depth = " + str(depth) + " loops = " + str(loops))
    return [], [], []

top_row, sides_left, corners_left = stick_row_together([first_corner], side_ids, 1)


#all_remaining = corner_ids.copy()
#all_remaining.extend(side_ids)
#all_remaining.extend(mid_ids)

#loop_count = 1
#
#for destination_index in range(initial_index, max_index):
#    loop_count += 1
#    if destination_index % grid_width == 0:
#        stick_to_tile = final_picture[destination_index - grid_width]
#        stick_to_edge = get_edges(stick_to_tile)[1]
#        vertical = True
#    else:
#        stick_to_tile = final_picture[destination_index - 1]
#        stick_to_edge = get_edges(stick_to_tile)[3]
#        vertical = False
#
#    for tid in all_remaining:
#        edge_i, flip = find_matching_edge_and_flip(stick_to_edge, tid)
#        if edge_i == -1:
#            continue
#
#        transpose = vertical
#        next_tile = tiles[tid]
#        if edge_i == 1:
#            next_tile = tile_flip_v(next_tile)
#        elif edge_i == 3:
#            next_tile = tile_flip_h(next_tile)
#
#        if edge_i == 0 or edge_i == 1:
#            transpose = not transpose
#
#        if transpose:
#            next_tile = tile_transpose(next_tile)
#
#        if flip:
#            if vertical:
#                next_tile = tile_flip_h(next_tile)
#            else:
#                next_tile = tile_flip_v(next_tile)
#        
#        if not vertical and destination_index >= grid_width:
#            other_t = final_picture[destination_index - grid_width]
#            bottom = get_edges(other_t)[1]
#            top = next_tile[0]
#            if top != bottom:
#                print("It's not working, tile: " + str(loop_count))
#                sys.exit()
#
#        final_picture.append(next_tile)
#        break

