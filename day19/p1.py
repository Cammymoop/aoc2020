import sys

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

debug = False

rules = {}
messages = []
rule_zone = True

for row in rows:
    if len(row) == 0:
        rule_zone = False
        continue

    if rule_zone:
        split_row = row.split(':')
        rule = split_row[1].strip()

        quote = rule.find('"')
        if quote != -1:
            rules[split_row[0]] = rule[quote + 1]
            continue

        variants = rule.split('|')
        variants = map(lambda s: s.strip().split(' '), variants)
        rules[split_row[0]] = list(variants)
        continue

    messages.append(row)

# Currently returns the first found match
# Might need to do something else so I can return other possible matches (idk how atm)
# Ok yeah, this doesn't work
# Need some way to recheck prefix or get all possible prefixes

# Ok, now returns array of possible lengths for matched prefix
def prefix_check(rule_id, message):
    global debug
    rule = rules[rule_id]
    if type(rule) == str:
        if message.find(rule) == 0 and len(message) > len(rule):
            return True, [len(rule)]
        else:
            return False, []

    possible_match_lengths = []
    for v in rule:
        if len(v) == 1:
            yes, lengths = prefix_check(v[0], message)
            if yes:
                for l in lengths:
                    if l not in possible_match_lengths and l < len(message):
                        possible_match_lengths.append(l)
            continue

        # hardcoded for rule variants with 2 subrules each because thats easy, and thats as big as they go
        yes, lengths = prefix_check(v[0], message)
        if not yes:
            continue
        for l in lengths:
            yes, lengths2 = prefix_check(v[1], message[l:])
            if yes:
                for l2 in lengths2:
                    if l + l2 not in possible_match_lengths and l + l2 < len(message):
                        possible_match_lengths.append(l + l2)

    return len(possible_match_lengths) > 0, possible_match_lengths

def check(rule_id, message):
    global debug
    rule = rules[rule_id]
    if type(rule) == str:
        return rule == message

    for v in rule:
        if len(v) == 1:
            if check(v[0], message):
                return True

        # hardcoded for rule variants with 2 subrules each because thats easy, and thats as big as they go
        yes, lengths = prefix_check(v[0], message)
        if not yes:
            continue
        for l in lengths:
            if check(v[1], message[l:]):
                return True

    return False

print("106 with 'a': " + str(check("106", "a")))
print("126 with 'bba': " + str(check("126", "bba")))

valids = 0
for m in messages:
    if check("0", m):
        valids += 1

print("Validated messages: " + str(valids) + " out of " + str(len(messages)))
