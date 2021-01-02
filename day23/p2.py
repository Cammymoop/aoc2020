import sys
import time
from functools import reduce
from collections import deque


class ListNode:
    def __init__(self, val=None):
        self.value = val
        self.nextitem = None

    def after_me(self, node):
        node.nextitem, self.nextitem = self.nextitem, node

class CupList:
    def __init__(self):
        self.firstcup = None
        self.lastcup = None
        self.number_to_cup = {}

    def append(self, cup_number):
        new_cup = ListNode(cup_number)
        if self.lastcup == None:
            self.firstcup = new_cup
            self.lastcup = new_cup
        else:
            self.lastcup.nextitem = new_cup
            self.lastcup = new_cup

        self.number_to_cup[cup_number] = new_cup

    def head(self):
        return self.firstcup

    def first_20(self):
        head_list = []
        first = self.firstcup
        for _ in range(20):
            head_list.append(first.value)
            first = first.nextitem
        return head_list

    def pophead(self):
        head = self.firstcup
        self.firstcup = self.firstcup.nextitem
        return head

    def next_head(self):
        head = self.firstcup
        self.firstcup = head.nextitem
        self.lastcup.nextitem = head
        self.lastcup = head
            

input = "792845136"

#cups = deque(map(int, input))
input_list = map(int, input)
cups_list = CupList()
for c in input_list:
    cups_list.append(c)

# Fill in the rest of the cups
MAX_CUP = 1000000
for x in range(10, MAX_CUP + 1):
    cups_list.append(x)

MAX_MOVE = 10000000

# number of moves for 0.01%
percent = MAX_MOVE / 20

debug = 3

start_time = time.time()
move = 0
while move < MAX_MOVE:
    move += 1
    current_val = cups_list.head().value
    cups_list.next_head()

    if debug > 0:
        debug -= 1
        print([move, "head", current_val, "cups", cups_list.first_20()])

    c1 = cups_list.pophead()
    c1v = c1.value
    c2 = cups_list.pophead()
    c2v = c2.value
    c3 = cups_list.pophead()
    c3v = c3.value
    next_c = current_val - 1
    if next_c == 0:
        next_c = MAX_CUP
    while next_c == c1v or next_c == c2v or next_c == c3v:
        next_c -= 1
        if next_c == 0:
            next_c = MAX_CUP

    insert_after = cups_list.number_to_cup[next_c]
    #cups_list.rotate(-shift_amount)
    insert_after.after_me(c3)
    insert_after.after_me(c2)
    insert_after.after_me(c1)
    #cups_list.rotate(shift_amount)

    if move % percent == 0:
        progress = (move // percent) * 5
        print("{:.2f}% Complete".format(progress))

end_time = time.time()
duration = end_time - start_time
print("Finished after {:.2f} seconds, {:.2f} minutes".format(duration, duration / 60))

cup1 = cups_list.number_to_cup[1].nextitem
cup2 = cup1.nextitem.value
cup1 = cup1.value

print(["First 2 cups after cup \"1\", after " + str(MAX_MOVE) + " moves", cup1, cup2, cup1 * cup2])

