from collections import deque

with open('input') as f:
    raw_rows = f.readlines()

numbers = []
for row in raw_rows:
    numbers.append(int(row.strip()))

last_numbers = deque()
buffer_length = 25

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
        break

    last_numbers.append(num)
    last_numbers.popleft()

