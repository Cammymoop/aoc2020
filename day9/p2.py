import sys
from collections import deque

with open('input') as f:
    raw_rows = f.readlines()

numbers = []
for row in raw_rows:
    numbers.append(int(row.strip()))

last_numbers = deque()
buffer_length = 25

first_invalid = None

for num in numbers:
    if len(last_numbers) < buffer_length:
        last_numbers.append(num)
        continue

    valid = False
    n_copy = last_numbers.copy()
    while len(n_copy) > 1:
        a = n_copy.popleft()
        for b in n_copy:
            if a + b == num:
                valid = True
                break
        if valid:
            break

    if not valid:
        print('Found first invalid number: ' + str(num))
        first_invalid = num
        break

    last_numbers.append(num)
    last_numbers.popleft()

for num_i in range(len(numbers)):
    subset = [numbers[num_i]]
    sub_sum = numbers[num_i]
    for x in range(num_i + 1, len(numbers)):
        sub_sum += numbers[x]
        subset.append(numbers[x])
        if sub_sum == first_invalid:
            print("Found straight that adds to " + str(first_invalid))
            n_min = min(subset)
            n_max = max(subset)
            print("min: " + str(n_min) + " max: " + str(n_max) + " min + max: " + str(n_min + n_max))
            sys.exit()
        if sub_sum > first_invalid:
            break

