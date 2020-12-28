import sys

with open('input') as f:
    raw_rows = f.readlines()

numbers = [0] # 0 is the wall joltage
for row in raw_rows:
    numbers.append(int(row))
numbers.sort()

jumps = {1: 0, 2: 0, 3: 0}

for i in range(len(numbers)):
    if i == len(numbers) - 1:
        diff = 3
        print(str(numbers[i]) + " -> " + str(numbers[i] + 3) + " ^3(phone)")
    else:
        diff = numbers[i+1] - numbers[i]
        print(str(numbers[i]) + " -> " + str(numbers[i+1]) + " ^" + str(diff))

    if diff > 3:
        print("Oh no, I dont have an adapter that can accept " + str(numbers[i]) + " jolts!!!")
        sys.exit()
    jumps[diff] += 1

print("total joltage differences: " + str(jumps))
print("joltage difference characteristic: " + str(jumps[1] * jumps[3]))

