
puz_input = [12,20,0,6,1,17,7]

last_appearance = {}
for i in range(len(puz_input)):
    last_appearance[puz_input[i]] = i + 1

previous = puz_input[-1]
num_2020 = -2
last_turn = 30000000

for turn in range(len(puz_input) + 1, last_turn + 1):
    if previous in last_appearance: 
        number = turn - last_appearance[previous] - 1
    else:
        number = 0

    last_appearance[previous] = turn - 1
    previous = number
    if turn == 2020:
        num_2020 = number

print("Number at turn 2020: " + str(num_2020))
print("Number at turn 30,000,000: " + str(previous))

