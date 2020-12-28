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
floating_bits = []
memmory = {}

def set_mem_recurse(value, addr, f_bits):
    if len(f_bits) == 0:
        memmory[addr] = value
        return
    f_bits2 = f_bits.copy()
    bit = f_bits2.pop()

    # set floated bit to 0
    addr = addr & ~(1 << bit)
    addr = addr & 0b111111111111111111111111111111111111
    set_mem_recurse(value, addr, f_bits2)
    # set floated bit to 1
    set_mem_recurse(value, addr | (1 << bit), f_bits2)


for command in commands:
    if command[0] == "mask":
        mask = command[1]
        or_mask = 0
        floating_bits = []
        bit = 35
        for char in mask:
            or_mask = or_mask << 1
            if char == "1":
                or_mask += 1
            if char == "X":
                floating_bits.append(bit)
            bit -= 1
        continue

    mem_addr = command[1]
    mem_addr = mem_addr | or_mask

    value = command[2]
    set_mem_recurse(value, mem_addr, floating_bits)

mem_sum = 0
for m in memmory:
    mem_sum += memmory[m]

print("Memmory sum: " + str(mem_sum))


