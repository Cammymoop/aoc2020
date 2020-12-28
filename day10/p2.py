import sys
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

numbers = [0] # 0 is the wall joltage
for row in raw_rows:
    numbers.append(int(row))
numbers.sort()

jumps = {1: 0, 2: 0, 3: 0}
straights_of_dif_1 = []
cur_straight = -1 

debug = False

for i in range(len(numbers)):
    if i == len(numbers) - 1:
        diff = 3
        if debug:
            print(str(numbers[i]) + " -> " + str(numbers[i] + 3) + " ^3(phone)")
    else:
        diff = numbers[i+1] - numbers[i]
        if debug:
            print(str(numbers[i]) + " -> " + str(numbers[i+1]) + " ^" + str(diff))

    if diff > 3:
        print("Oh no, I dont have an adapter that can accept " + str(numbers[i]) + " jolts!!!")
        sys.exit()
    jumps[diff] += 1

    if diff == 1:
        cur_straight += 1
    if diff == 3:
        if cur_straight > 0:
            straights_of_dif_1.append(cur_straight)
        cur_straight = -1

# Number of possible ways to choose adapters from the straight of 1s that still work
def f(x):
    if x < 3: # short enough that you can leave or take any adapter
        return 2 ** x
    # Otherwise you simply subtract the number of combos that leave out 3 adapters in a row
    # For 3 thats just one way
    if x == 3:
        return (2 ** x) - 1
    # I dont have any straights longer than 3 which is good because I haven't figured out the generalized formula yet

def combine(acc, x):
    return acc * f(x)

valid_combo_count = reduce(lambda acc, x: acc * f(x), straights_of_dif_1, 1) 

print("staights of consecutive differences of 1 joltage: " + str(straights_of_dif_1))
print("Total number of valid ways to chain adapters: " + str(valid_combo_count))

