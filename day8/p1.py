import operator
from functools import reduce
import re

with open('input') as f:
    raw_rows = f.readlines()

instructions = []
for row in raw_rows:
    instructions.append(row.strip().split(' '))

last_instruction = len(instructions) - 1

PC = 0
ACC = 0

executed_instructions = set([])

while True:
    if PC in executed_instructions:
        print('About to loop! PC: ' + str(PC) + ' ACC: ' + str(ACC))
        print('Aborting...')
        break

    executed_instructions.add(PC)

    next_i = instructions[PC]
    num_val = int(next_i[1][1:]) * (-1 if next_i[1][0] == '-' else 1)

    # acc adds to the ACC
    if next_i[0] == "acc":
        ACC += num_val

    # jmp adds to the PC, otherwise advance the PC 1
    if next_i[0] == "jmp":
        PC += num_val
    else:
        PC += 1

    if PC < 0 or PC > last_instruction:
        print('Out of range instruction. Aborting...')
        print(executed_instructions)
        break

