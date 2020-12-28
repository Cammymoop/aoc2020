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

valid_tickets = []
for ticket in other_tickets:
    valid = True
    for n in ticket:
        if n in never_valid_numbers or n > max_valid:
            valid = False
            break

    if valid:
        valid_tickets.append(ticket)

##
# Now to figure out which field is which
##

total_fields = len(my_ticket)
all_rules = list(map(lambda x: x['name'], rules))

def validate_n(n, rule):
    r = rule['ranges']
    return (n >= r[0][0] and n <= r[0][1]) or (n >= r[1][0] and n <= r[1][1])

def get_rule(rule_name):
    for rule in rules:
        if rule['name'] == rule_name:
            return rule

possible_rules = []

for i in range(total_fields):
    rules_for_this_index = []
    for rule in rules:
        if not validate_n(my_ticket[i], rule):
            continue

        valid = True
        for ticket in valid_tickets:
            if not validate_n(ticket[i], rule):
                valid = False
                break
        if not valid:
            continue

        rules_for_this_index.append(rule['name'])

    possible_rules.append(rules_for_this_index)


field_indexes = {}
rules_left = all_rules.copy()
index_left = list(range(total_fields))
while len(rules_left) > 0:
    for i in range(total_fields):
        if i not in index_left:
            continue
        possible_rules[i] = list(filter(lambda x: x in rules_left, possible_rules[i]))
        if len(possible_rules[i]) == 1:
            name = possible_rules[i][0]
            print(name + " is the only valid rule for field " + str(i))
            field_indexes[name] = i
            index_left.remove(i)
            rules_left.remove(name)

    for r in all_rules:
        if r not in rules_left:
            continue
        possible_index = list(filter(lambda x: r in possible_rules[x], index_left))
        if len(possible_index) == 1:
            i = possible_index[0]
            print(r + " is only valid for one field, " + str(i))
            index_left.remove(i)
            rules_left.remove(r)

print("Here are the positions of all the fields: " + str(field_indexes))

departure_fields = list(filter(lambda x: x.find('departure') == 0, all_rules))

ticket_value = 1
for field in departure_fields:
    index = field_indexes[field]
    ticket_value *= my_ticket[index]

print("My ticket departure value: " + str(ticket_value))

