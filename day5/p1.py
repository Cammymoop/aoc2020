import operator
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for raw in raw_rows:
    rows.append(raw.strip())

high_chars = ["B", "R"]

def str_binary(acc, character):
    acc *= 2
    acc += 1 if character in high_chars else 0
    return acc

max_seat_id = 0
d = True

for seat in rows:
    seat_row = reduce(str_binary, seat[:7], 0)
    seat_col = reduce(str_binary, seat[7:], 0)

    seat_id = seat_row * 8 + seat_col
    max_seat_id = max(seat_id, max_seat_id)
    
    if d:
        d = False
        print("row " + seat[:7] + ": " + str(seat_row))
        print("column " + seat[7:] + ": " + str(seat_col))


print("Max seat ID: " + str(max_seat_id))

