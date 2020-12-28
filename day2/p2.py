import operator
from functools import reduce

with open('input') as f:
    rows = f.readlines()

total = len(rows)
valids = 0

for row in rows:
    pieces = row.strip().split(' ')
    letter = pieces[1][0]
    fi = int(pieces[0].split('-')[0]) - 1
    si = int(pieces[0].split('-')[1]) - 1

    letter_occ = (pieces[2][fi] + pieces[2][si]).count(letter)
    if letter_occ == 1:
        valids += 1


print("Total passwords: " + str(total))
print("Valid passwords: " + str(valids))
print("Invalid passwords: " + str(total - valids))

