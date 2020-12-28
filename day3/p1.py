
with open('input') as f:
    rows = f.readlines()

width = len(rows[0]) - 1
trees = [0, 0, 0, 0, 0]

def str_insert(string, i, char):
    return string[:i] + char + string[i+1:]

slopes = [1, 3, 5, 7, .5]

for x in range(len(rows)):
    for si in range(len(slopes)):
        if not isinstance(slopes[si], int) and not (slopes[si] * x).is_integer():
            continue
        if rows[x][int(slopes[si] * x) % width] != '.':
            trees[si] += 1

    #view = str_insert(rows[x], (3*x) % width, 'Q')
    #if x < 20:
        #print(view.strip())

total = 0
product = 1
for i in range(len(trees)):
    total += trees[i]
    product *= trees[i]
    print("Hit " + str(trees[i]) + " trees on the " + str(slopes[i]) + " slope.")

print("In total, " + str(total) + " trees. Or multiplied together: " + str(product) + ".")
if total > 0:
    print("Ouch.")
else:
    print("Wow, unexpected...")
