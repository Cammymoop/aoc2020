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

games_completed = 0
game_print_interval = 10000

def shorten(q, n):
    for _ in range(len(q) - n):
        q.popleft()
    return q

def do_game(player1, player2, depth):
    global games_completed, game_print_interval
    round = 1
    prev_positions = []
    while True:
        #print(["GAME DEPTH", depth, "ROUND", round])
        p1_hash = ','.join(map(str, player1))
        p2_hash = ','.join(map(str, player2))
        #print([p1_hash, p2_hash])
        #print('.')
        this_position = (p1_hash, p2_hash)
        if this_position in prev_positions:
            return 1, player1
        prev_positions.append(this_position)

        p1_card = player1.pop()
        p2_card = player2.pop()
        if p1_card > len(player1) or p2_card > len(player2):
            # cant recurse, winner is the one with the bigger card
            p1_wins = p1_card > p2_card
        else:
            # Winner of round is winner of recursive game
            winner, _ = do_game(shorten(player1.copy(), p1_card), shorten(player2.copy(), p2_card), depth + 1)
            games_completed += 1
            if games_completed % game_print_interval == 0:
                print(str(games_completed) + " games finished!")
            p1_wins = winner == 1


        if p1_wins:
            player1.appendleft(p1_card)
            player1.appendleft(p2_card)
        else:
            player2.appendleft(p2_card)
            player2.appendleft(p1_card)

        losers_deck = min(len(player1), len(player2))
        if losers_deck == 0:
            if len(player1) > 0:
                return 1, player1
            else:
                return 2, player2

        round += 1

winner, winners_deck = do_game(player1, player2, 1)

score = 0
multiplier = 1
for card in winners_deck:
    score += card * multiplier
    multiplier += 1

crab = "🦀" if winner == 2 else ""

print(crab + "Player " + str(winner) + " wins!" + crab)
print(["final score:", score, "deck", winners_deck])

