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

# Special rules
special_rules = ["8", "11"]
# 8 changed from 8: 42 to 8: 42 | 42 8
# which is equivalent to 42 any number of times

# 11 changed from 11: 42 31 to 11: 42 31 | 42 11 31
# which is equivalent to 42 any number of times followed by 31 the same number of times

def prefix_repeater_42(message):
    yes, lengths = prefix_check("42", message)
    if not yes:
        return False, []

    possible_lengths = []
    for l in lengths:
        yes, lengths2 = prefix_repeater_42(message[l:])
        if yes:
            for l2 in lengths2:
                if l2 + l not in possible_lengths:
                    possible_lengths.append(l2 + l)
        if l not in possible_lengths:
            possible_lengths.append(l)

    return len(possible_lengths) > 0, possible_lengths

def prefix_repeater_42_31(message, depth, part2):
    possible_lengths = []
    if part2:
        depth -= 1
        if depth == 0:
            yes, lengths = prefix_check("31", message)
            if yes:
                for l in lengths:
                    if l not in possible_lengths:
                        possible_lengths.append(l)
            return len(possible_lengths) > 0, possible_lengths
        else:
            yes, lengths = prefix_check("31", message)
            if yes:
                for l in lengths:
                    yes, lengths2 = prefix_repeater_42_31(message[l:], depth, True)
                    if yes:
                        for l2 in lengths2:
                            if l + l2 not in possible_lengths:
                                possible_lengths.append(l + l2)
            return len(possible_lengths) > 0, possible_lengths

    yes, lengths = prefix_check("42", message)
    if yes:
        for l in lengths:
            yes, lengths2 = prefix_repeater_42_31(message[l:], depth + 1, False)
            if yes:
                for l2 in lengths2:
                    if l + l2 not in possible_lengths:
                        possible_lengths.append(l + l2)
        if len(possible_lengths) > 0:
            return True, possible_lengths

    if depth > 0:
        return prefix_repeater_42_31(message, depth, True)

    return False, []

# Functions for special rules checking at the end of the message
def end_repeater_42(message):
    if check("42", message):
        return True

    yes, lengths = prefix_check("42", message)
    if yes:
        for l in lengths:
            result = end_repeater_42(message[l:])
            if result:
                return True
    else:
        return False

def end_repeater_42_31(message, depth, part2):
    if part2:
        depth -= 1
        if depth == 0:
            if check("31", message):
                return True
            return False
        else:
            yes, lengths = prefix_check("31", message)
            if yes:
                for l in lengths:
                    result = end_repeater_42_31(message[l:], depth, True)
                    if result:
                        return True
            return False

    yes, lengths = prefix_check("42", message)
    if yes:
        for l in lengths:
            result = end_repeater_42_31(message[l:], depth + 1, False)
            if result:
                return True

    if depth > 0:
        return end_repeater_42_31(message, depth, True)

    return False

def sp_check(rule_id, message):
    if rule_id == "8":
        return end_repeater_42(message)
    elif rule_id == "11":
        return end_repeater_42_31(message, 0, False)

def sp_prefix_check(rule_id, message):
    if rule_id == "8":
        return prefix_repeater_42(message)
    elif rule_id == "11":
        return prefix_repeater_42_31(message, 0, False)


# Mostly reused code from part 1
def prefix_check(rule_id, message):
    global debug
    if rule_id in special_rules:
        return sp_prefix_check(rule_id, message)
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
    if rule_id in special_rules:
        return sp_check(rule_id, message)
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
