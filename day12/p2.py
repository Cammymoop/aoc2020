import sys

with open('input') as f:
    raw_rows = f.readlines()

commands = []
numbers = []
for row in raw_rows:
    commands.append(row[0])
    numbers.append(int(row[1:]))

# rotation = 1, 2, or 3 (anticlockwise, 180, or clockwise)
def rotated_x_y(rotation, x, y):
    if rotation == 2:
        return [-x, -y]
    elif rotation == 1:
        return [-y, x]
    elif rotation == 3:
        return [y, -x]
    print("invalid rotated x y")
    return []

def direction_to_x_y(direction):
    if direction == 'E':
        return [1, 0]
    elif direction == 'N':
        return [0, 1]
    elif direction == 'W':
        return [-1, 0]
    elif direction == 'S':
        return [0, -1]
    print("Invalid direction: " + direction)
    return []

ship_pos_x = 0
ship_pos_y = 0

waypoint_x = 10
waypoint_y = 1
for i in range(len(commands)):
    comm = commands[i]
    if comm == "R" or comm == "L":
        rotation = numbers[i]/90 if comm == "L" else 4 - numbers[i]/90
        xy = rotated_x_y(rotation, waypoint_x, waypoint_y)
        waypoint_x = xy[0]
        waypoint_y = xy[1]
    elif comm == "F":
        ship_pos_x += waypoint_x * numbers[i]
        ship_pos_x += waypoint_y * numbers[i]
    else: 
        xy = direction_to_x_y(comm)
        waypoint_x += xy[0] * numbers[i]
        waypoint_y += xy[1] * numbers[i]

print("Ship's new position: " + str([ship_pos_x, ship_pos_y]))
print("Current relative waypoint: " + str([waypoint_x, waypoint_y]))
print("Ship's manhattan distance: " + str(abs(ship_pos_x) + abs(ship_pos_y)))

