import sys
from collections import deque

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

player1 = deque()
player2 = deque()
is_p1 = True
for row in rows:
    if row == "Player 1:":
        continue
    if row == "Player 2:":
        is_p1 = False
        continue
    if len(row) == 0:
        continue

    if is_p1:
        player1.appendleft(int(row))
    else:
        player2.appendleft(int(row))

round = 1
winner = 0
while True:
    p1_card = player1.pop()
    p2_card = player2.pop()
    p1_wins = True
    if p2_card > p1_card:
        p1_wins = False

    if p1_wins:
        player1.appendleft(p1_card)
        player1.appendleft(p2_card)
    else:
        player2.appendleft(p2_card)
        player2.appendleft(p1_card)

    losers_deck = min(len(player1), len(player2))
    if losers_deck == 0:
        winner = player1 if len(player1) > 0 else player2
        print(["Somebody lost, round", round, "player1", len(player1), "player2", len(player2)])
        break

    round += 1

score = 0
multiplier = 1
for card in winner:
    score += card * multiplier
    multiplier += 1

print(["final score:", score])

