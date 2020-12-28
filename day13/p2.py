import sys
from functools import reduce


# Euclidian algorithm
# Get greatest common factor of two integers
def gcf(a, b):
    if b > a:
        a, b = (b, a)

    while True:
        c = a % b
        if c == 0:
            return b
        a = b
        b = c

# Get lowest common multiple of two integers
def lcm(a, b):
    c = gcf(a, b)
    return int((a/c) * b)

# Extended Euclidian algorithm simplified to get the multiplicative inverse of a mod b
# a and b must be coprime integers
def mod_inverse(a, b):
    r2 = a
    r = b
    x2 = 1
    x = 0

    while r2 != 0:
        r, quot, r2 = (r2,) + divmod(r, r2)
        x, x2 = (x2, x - (x2 * quot))

    # normalize a negative multiplicative inverse mod b
    return x % b

# return the first time offset where [other_bus] leaves [bus_offset] minutes after [origin_bus]
# also return the repeating period, how long it will be until the same thing happens again
def simple_offset_and_period(origin_bus, other_bus, bus_offset):
    period = lcm(origin_bus, other_bus)

    the_gcf = gcf(origin_bus, other_bus)
    if the_gcf > 1:
        #busses/combined bus periods are not coprime
        if bus_offset % the_gcf != 0:
            print("Impossible!!!")
            sys.exit()
        bus_offset = bus_offset // the_gcf
        origin_bus = origin_bus // the_gcf
        other_bus = other_bus // the_gcf
    bus_diff = (other_bus - origin_bus) % other_bus

    # Complicated math to find the first occurance of the busses with the offset
    special_val = mod_inverse(bus_diff, other_bus) * bus_offset
    special_val = special_val % other_bus

    # scale back up by the gcf if they weren't coprime
    # otherwise gcf is 1
    offset = (special_val * origin_bus) * the_gcf
    return (offset, period)

# Figure out the first time offset where both occurances happen
def combined_offset_and_period(offset_a, period_a, offset_b, period_b):
    if offset_a > offset_b:
        offset_a, offset_b = (offset_b, offset_a)
        period_a, period_b = (period_b, period_a)

    offset_diff = offset_b - offset_a
    # Use the same algorithm to find an intersection
    new_offset, new_period = simple_offset_and_period(period_b, period_a, offset_diff)
    return (offset_b + new_offset, new_period)


with open('input') as f:
    discard = int(f.readline())
    raw_busses = f.readline().strip().split(',')

busses = []
# required offsets vs the origin bus to have a valid solution
bus_offsets = []
bus_time_offset = 0

origin_bus = int(raw_busses.pop(0))
print("origin_bus _ " + str(origin_bus))
for b in raw_busses:
    bus_time_offset += 1
    if b == "x":
        continue
    bus = int(b)
    busses.append(bus)

    r_offset = bus_time_offset
    # if the required offset is more than (bus interval) after the answer T
    # rewind the required offset to the earliest time the bus will leave after T
    while r_offset >= bus:
        r_offset -= bus
    bus_offsets.append(r_offset)

# First loop through and find the first time offset where the bus has the correct offset vs the origin bus
# as well as the period that it will happen with
bus_offset_periods = []
for i in range(len(busses)):
    bus_offset_periods.append(simple_offset_and_period(origin_bus, busses[i], bus_offsets[i]))

# reduce func to combine all the offset/periods to find the offset/period of all of them at the same time
def reduce_combine_offsets(o_acc, o_b):
    if o_acc == (0, 0):
        return o_b
    return combined_offset_and_period(*o_acc, *o_b)

final_offset, final_period = reduce(reduce_combine_offsets, bus_offset_periods, (0, 0))
print("Final offset: " + str(final_offset) + " Final period: " + str(final_period))
