import sys

with open('input') as f:
    raw_rows = f.readlines()

pub_keys = []
for row in raw_rows:
    pub_keys.append(int(row.strip()))

initial_subject = 7
mod = 20201227

def transform(num, subject):
    return num * subject % mod

other_key = 0
val = 1
loop_size = 0
while True:
    val = transform(val, initial_subject)
    loop_size += 1
    if val == pub_keys[0]:
        other_key = pub_keys[1]
        break
    elif val == pub_keys[1]:
        other_key = pub_keys[0]
        break

print(["Loop size is", loop_size])

val = 1
for i in range(loop_size):
    val = transform(val, other_key)

print(["Encryption key", val])
