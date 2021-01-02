import sys
from functools import reduce
from collections import deque

input = "792845136"

cups = deque(map(int, input))

MAX_MOVE = 100
CUPS = 9

percent = MAX_MOVE / 100

after_100 = 0
move = 0
while move < MAX_MOVE:
    move += 1
    current = cups[0]
    cups.rotate(-1)
    c1 = cups.popleft()
    c2 = cups.popleft()
    c3 = cups.popleft()
    next_c = current - 1
    if next_c == 0:
        next_c = 9
    while next_c == c1 or next_c == c2 or next_c == c3:
        next_c -= 1
        if next_c == 0:
            next_c = 9

    # Rotate the destination to the front
    shift_amount = cups.index(next_c) + 1
    cups.rotate(-shift_amount)
    cups.appendleft(c3)
    cups.appendleft(c2)
    cups.appendleft(c1)
    # Rotate back so the next current cup is at the front
    cups.rotate(shift_amount)

    if move == 100:
        after_100 = cups.copy()
    if move % percent == 0:
        progress = (move // percent)
        print("{}% Complete".format(progress))

def answer(q):
    q = q.copy()
    one_pos = q.index(1)
    q.rotate(-one_pos)
    q.popleft()
    return reduce(lambda acc, x: acc + str(x), q, "")

print(["Cups after 100 moves", after_100, answer(after_100)])

