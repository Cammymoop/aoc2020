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

bag_phrase = re.compile('([0-9]*) ' + bag_r)

some_bags = re.compile(bag_r + ' contain [0-9]* ' + bag_r + '(, [0-9]* ' + bag_r + ')*')

def bags_in_list(bag_list):
    split_list = bag_list.strip('.').split(', ')
    bags = {}
    for b in split_list:
        m = re.match(bag_phrase, b)
        bags[m.group(2)] = int(m.group(1))

    return bags

# store {color of bag: {color of contained bag: number of them, ...}}
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
def total_contained_by(color, checked):
    if bag_contains[color] == False:
        return 0

    total_bags = 0
    immediate_contents = bag_contains[color]

    checked.add(color)
    for c in immediate_contents:
        if c in checked:
            #recursive bag rules mean infinite bags
            print('checked colors so far: ' + str(checked))
            print('current bag color ' + str(c))
            return float('inf')

        # Add the number of bags of this color in this bag
        total_bags += immediate_contents[c]
        # Add the number of bags inside those bags (mulitplied by how many there are)
        total_bags += total_contained_by(c, set(checked)) * immediate_contents[c]

    return total_bags

bags_that_shiny_contains = total_contained_by('shiny gold', set([]))

print("Total bags are contained in a shiny gold bag: " + str(bags_that_shiny_contains))

