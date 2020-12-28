import operator
from functools import reduce
import re

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for raw in raw_rows:
    rows.append(raw.strip())

debug = 4

bag_r = '([a-z]+ [a-z]+) bags?'
no_bags_sentence = re.compile(bag_r + ' contain no other bags')
some_bags_sentence = re.compile(bag_r + ' contain (?=[0-9]* )')

bag_phrase = re.compile('[0-9]* ' + bag_r)

some_bags = re.compile(bag_r + ' contain [0-9]* ' + bag_r + '(, [0-9]* ' + bag_r + ')*')

def bags_in_list(bag_list):
    split_list = bag_list.strip('.').split(', ')
    bags = []
    for b in split_list:
        m = re.match(bag_phrase, b)
        bags.append(m.group(1))

    return bags

# store {color of bag: [color of contained bag, ...]}
bag_contains = {}

for row in rows:
    # For bags that contain nothing
    no_bag_match = re.match(no_bags_sentence, row)
    if no_bag_match != None:
        bag_contains[no_bag_match.group(1)] = False
        if debug > 0:
            debug -= 1
            print(color + ' contains nada')
        continue


    # For bags that contain some number of other bags
    bag_match = re.match(some_bags_sentence, row)
    if bag_match != None:
        color = bag_match.group(1)
        contents = row[bag_match.end():]
        contained_colors = bags_in_list(contents)
        bag_contains[color] = contained_colors
        if debug > 0:
            debug -= 1
            print(color + ' contains: ' + str(bag_contains[color]))
    else:
        print("Invalid Sentence: " + row)
        break

# Recursively get all colors a color can contain
def colors_contained_by(color, checked):
    if bag_contains[color] == False:
        return []
    immediate_colors = bag_contains[color]
    all_colors = immediate_colors

    checked.add(color)
    for c in immediate_colors:
        if c in checked:
            continue
        c_contains = colors_contained_by(c, checked)
        for new_c in c_contains:
            if not new_c in all_colors:
                all_colors.append(new_c)

    return all_colors

bags_that_can_contain_shiny = 0
debug = True

for color in bag_contains:
    recurs_contents = colors_contained_by(color, set([]))
    if debug:
        debug = False
        print(color + ' recursively contains: ' + str(recurs_contents))
    if 'shiny gold' in recurs_contents:
        bags_that_can_contain_shiny += 1
    

print("Total bags that can contain shiny gold: " + str(bags_that_can_contain_shiny))

