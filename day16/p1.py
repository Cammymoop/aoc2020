from functools import reduce
import sys

with open('input') as f:
    raw_rows = f.readlines()

debug = True

rules = []
my_ticket = []
other_tickets = []
section = "rules"

for row in raw_rows:
    row = row.strip()

    if len(row) == 0:
        section = ""
        continue

    if section == "":
        if "your ticket" in row:
            section = "my"
        if "nearby ticket" in row:
            section = "other"
        continue

    if section == "rules":
        split_row = row.split(':')
        numbers = list(map(lambda x: list(map(lambda y: int(y), x.split('-'))), split_row[1].split('or')))
        rules.append({'name': split_row[0], 'ranges': numbers})
    elif section == "my":
        my_ticket = list(map(lambda x: int(x), row.split(',')))
    elif section == "other":
        other_tickets.append(list(map(lambda x: int(x), row.split(','))))

max_valid = reduce(lambda acc, r: max(acc, r['ranges'][-1][-1]), rules, 0)
print("Maximum valid number: " + str(max_valid))


# find all possible gaps in number rules for mid range numbers that are never valid
# (my input has no gaps but do it anyway)
never_valid_numbers = []

n = 0
while True:
    valid = False
    next_min_valid = max_valid
    skip_to = n + 1
    for r in rules:
        ranges = r['ranges']
        if n < ranges[0][0]:
            next_min_valid = min(next_min_valid, ranges[0][0])
        elif n <= ranges[1][1]:
            if n <= ranges[0][1] or n >= ranges[1][0]:
                valid = True
                if n <= ranges[0][1]:
                    skip_to = ranges[0][1] + 1
                else:
                    skip_to = ranges[1][1] + 1
                break
            next_min_valid = min(next_min_valid, ranges[1][0])

    if valid:
        n = skip_to
    else:
        never_valid_numbers.extend(list(range(n, next_min_valid)))
        n = next_min_valid + 2
    if n > max_valid:
        break

print("All numbers that are never valid less than " + str(max_valid + 1) + ": " + str(never_valid_numbers))

found_invalids = []
i = 0
min_n = max_valid
max_n = 0
for ticket in other_tickets:
    for n in ticket:
        min_n = min(min_n, n)
        max_n = max(max_n, n)
        if n in never_valid_numbers or n > max_valid:
            found_invalids.append(n)
            print("Ticket " + str(i) + " was invalid (" + str(n) + ")")
    i += 1

print("Ticket scanning error rate (sum of invalid numbers on other tickets): " + str(sum(found_invalids)))
print("min ticket field value: " + str(min_n) + ", max ticket field value: " + str(max_n))
