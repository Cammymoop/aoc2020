
with open('input') as f:
    rows = f.readlines()

numbers = []
for row in rows:
    numbers.append(int(row))

fnum = 0
target = 0

while len(numbers) > 1:
    fnum = numbers.pop()
    target = 2020 - fnum
    if target in numbers:
        break

print("Numbers: " + str([target, fnum]))
print("Product: " + str(fnum * target))
