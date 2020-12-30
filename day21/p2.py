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

single_ingredient_alergins = 0
alergins_to_ingredients = {}
while single_ingredient_alergins < len(all_alergins):
    last = single_ingredient_alergins
    single_ingredient_alergins = 0
    for a in all_alergins:
        possible = alergin_to_possible_ingredients[a]
        if len(possible) == 1:
            single_ingredient_alergins += 1
            if a not in alergins_to_ingredients:
                ingredient = list(possible)[0]
                alergins_to_ingredients[a] = ingredient
                for a2 in all_alergins:
                    if a == a2:
                        continue
                    possible2 = alergin_to_possible_ingredients[a2]
                    alergin_to_possible_ingredients[a2] = possible2 - set([ingredient])
    if last == single_ingredient_alergins:
        print("stuck on " + str(last) + " decided ingredients out of " + str(len(all_alergins)))
        sys.exit()

print(alergins_to_ingredients)
#Sort alergins here
sorted_alergins = all_alergins

answer = ""
for a in sorted_alergins:
    if answer != "":
        answer += ","
    answer += alergins_to_ingredients[a]

print("Ingredients that contain alergins sorted by their respective alergins alphabetically")
print(answer)
