import sys

with open('input') as f:
    raw_rows = f.readlines()

commands = []
numbers = []
for row in raw_rows:
    commands.append(row[0])
    numbers.append(int(row[1:]))

def command_to_direction(command, facing):
    if command == "E":
        return 0
    elif command == "N":
        return 1
    elif command == "W":
        return 2
    elif command == "S":
        return 3
    elif command == "F":
        return facing

    print("invalid move command")
    return 0 #should never get here


def direction_to_x_y(direction):
    if direction == 0:
        return [1, 0]
    elif direction == 1:
        return [0, 1]
    elif direction == 2:
        return [-1, 0]
    elif direction == 3:
        return [0, -1]

ship_pos_x = 0
ship_pos_y = 0
ship_facing = 0 # 0 east, 1 north, 2 west, 3 south
for i in range(len(commands)):
    if commands[i] == "R" or commands[i] == "L":
        sign = 1 if commands[i] == "L" else -1
        ship_facing += numbers[i]/90 * sign
        if ship_facing < 0:
            ship_facing += 4
        elif ship_facing > 3:
            ship_facing -= 4
        continue

    move_dir = command_to_direction(commands[i], ship_facing)
    xy = direction_to_x_y(move_dir)
    ship_pos_x += xy[0] * numbers[i]
    ship_pos_y += xy[1] * numbers[i]

print("Ship's new position: " + str([ship_pos_x, ship_pos_y]))
print("Ship's manhattan distance: " + str(abs(ship_pos_x) + abs(ship_pos_y)))

