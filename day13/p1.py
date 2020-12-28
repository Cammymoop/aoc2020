

with open('input') as f:
    earliest_time = int(f.readline())
    raw_busses = f.readline().strip().split(',')

busses = []
for b in raw_busses:
    if b == "x":
        continue
    busses.append(int(b))

cur_time = earliest_time
infinite_protection = 1000

rode = False
while True:
    for bus in busses:
        if cur_time % bus == 0:
            print("Riding bus " + str(bus))
            waited_mins = cur_time - earliest_time
            print("Current time is: " + str(cur_time) + ", I waited " + str(waited_mins) + " minutes. (bus * waited = " + str(bus * waited_mins) + ")")
            rode = True
            break

    if rode:
        break

    cur_time += 1
    infinite_protection -= 1
    if infinite_protection < 0:
        print("oops something went wrong")
        break
