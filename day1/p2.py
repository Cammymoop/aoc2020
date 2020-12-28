import operator
from functools import reduce

with open('input') as f:
    rows = f.readlines()

numbers = []
for row in rows:
    numbers.append(int(row))

the_min = min(numbers)

def find_them():
    while len(numbers) > 2:
        fnum = numbers.pop()
        target = 2020 - fnum
        for x in numbers:
            tnum = target - x
            if tnum < the_min:
                continue
            if tnum in numbers:
                print("found them")
                return [fnum, x, tnum]

the_numbers = find_them()

print(str(len(numbers)) + " left")

print("Numbers: " + str(the_numbers))
print("Product: " + str(reduce(operator.mul, the_numbers, 1)))
