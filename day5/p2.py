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

ids = []
max_seat_id = 0

for seat in rows:
    seat_row = reduce(str_binary, seat[:7], 0)
    seat_col = reduce(str_binary, seat[7:], 0)

    seat_id = seat_row * 8 + seat_col
    max_seat_id = max(max_seat_id, seat_id)
    ids.append(seat_id)

missing_seat = 0

for seat_id in ids:
    if seat_id == max_seat_id:
        continue
    if seat_id + 1 in ids:
        continue

    missing_seat = seat_id + 1
    break


print("Max seat ID: " + str(max_seat_id))
print("Missing seat: " + str(missing_seat))

