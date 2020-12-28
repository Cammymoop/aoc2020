import sys

with open('input') as f:
    raw_rows = f.readlines()

commands = []
for row in raw_rows:
    if row[:4] == "mask":
        commands.append(["mask", row.split('=')[1].strip()])
    elif row[:4] == "mem[":
        end_index = row.find("]")
        mem_addr = int(row[4:end_index])
        mem_val = int(row.split("=")[1].strip())
        commands.append(["mem", mem_addr, mem_val])

or_mask = 0
nor_mask = 0
memmory = {}

for command in commands:
    if command[0] == "mask":
        mask = command[1]
        or_mask = 0
        nor_mask = 0
        for char in mask:
            or_mask = or_mask << 1
            nor_mask = nor_mask << 1
            if char == "1":
                or_mask += 1
            if char == "0":
                nor_mask += 1
        continue

    mem_addr = command[1]
    value = command[2]
    value = ~value | nor_mask
    value = ~value | or_mask
    memmory[mem_addr] = value

mem_sum = 0
for m in memmory:
    mem_sum += memmory[m]

print("Memmory sum: " + str(mem_sum))


