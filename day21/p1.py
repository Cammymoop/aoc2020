import sys
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

all_ingredients = []
all_alergins = []
foods = []

for row in rows:
    ingredients, alergins = row.split('(')
    if alergins[:9] != "contains ":
        print("misformed alergin list?")
        sys.exit()
    alergins = alergins[9:].strip(')').split(', ')
    ingredients = ingredients.strip().split(' ')
    for ing in ingredients:
        if ing not in all_ingredients:
            all_ingredients.append(ing)
    for aler in alergins:
        if aler not in all_alergins:
            all_alergins.append(aler)
    foods.append([ingredients, alergins])

print(all_ingredients)
print(all_alergins)

safe_ingredients = all_ingredients.copy()
alergin_to_possible_ingredients = {}
alergin_to_foods = {}
for alergin in all_alergins:
    food_list = []
    possible_ingredients = set()
    for f in foods:
        if alergin in f[1]:
            if len(possible_ingredients) == 0:
                possible_ingredients = set(f[0])
            else:
                possible_ingredients = possible_ingredients & set(f[0])
            food_list.append(f)

    for ing in possible_ingredients:
        if ing in safe_ingredients:
            safe_ingredients.remove(ing)
    alergin_to_possible_ingredients[alergin] = possible_ingredients
    alergin_to_foods[alergin] = food_list


safe_ingredient_count = 0
for f in foods:
    for ing in safe_ingredients:
        if ing in f[0]:
            safe_ingredient_count += 1

print("Number of times a safe ingredient is listed: " + str(safe_ingredient_count))
