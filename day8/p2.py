import sys

with open('input') as f:
    raw_rows = f.readlines()

instructions = []
for row in raw_rows:
    instructions.append(row.strip().split(' '))

last_instruction = len(instructions)

fixes_tried = set([])
successful_fix = False

while not successful_fix:
    PC = 0
    ACC = 0
    executed_instructions = set([])
    fix_available = True
    cur_fix = -1

    while True:
        if PC in executed_instructions:
            #print('About to loop! PC: ' + str(PC) + ' ACC: ' + str(ACC))
            #print('Aborting...')
            break

        executed_instructions.add(PC)

        next_i = instructions[PC]
        num_val = int(next_i[1][1:]) * (-1 if next_i[1][0] == '-' else 1)
        jump = 1

        # acc adds to the ACC
        if next_i[0] == "acc":
            ACC += num_val

        # jmp adds to the PC
        if next_i[0] == "jmp":
            if fix_available and PC not in fixes_tried:
                # switch jmp to nop
                fix_available = False
                cur_fix = PC
                fixes_tried.add(PC)
            else:
                jump = num_val

        # nop does nothing
        if next_i[0] == "nop":
            if fix_available and PC not in fixes_tried:
                # switch nop to jmp
                fix_available = False
                cur_fix = PC
                fixes_tried.add(PC)
                jump = num_val

        PC += jump

        if PC == last_instruction:
            print('End of boot code reached, terminating successfully...')
            print('PC: ' + str(PC) + ' ACC: ' + str(ACC) + ' Modified instruction: ' + str(cur_fix))
            successful_fix = True
            break
        if PC < 0 or PC > last_instruction:
            print('Out of range instruction. Aborting...')
            sys.exit()
            break

    if fix_available:
        print("All possible fixes tried, no solution found...")
        print(fixes_tried)
        break

