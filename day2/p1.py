import operator
from functools import reduce

with open('input') as f:
    rows = f.readlines()

total = len(rows)
valids = 0

for row in rows:
    pieces = row.strip().split(' ')
    letter = pieces[1][0]
    min_occ = int(pieces[0].split('-')[0])
    max_occ = int(pieces[0].split('-')[1])

    letter_occ = pieces[2].count(letter)
    if letter_occ >= min_occ and letter_occ <= max_occ:
        valids += 1


print("Total passwords: " + str(total))
print("Valid passwords: " + str(valids))
print("Invalid passwords: " + str(total - valids))

