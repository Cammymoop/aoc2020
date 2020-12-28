import sys
from collections import deque

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

def symbol_type(character):
    if character == '(':
        return 'open'
    elif character.isdigit():
        return 'number'
    elif character == '+' or character == '*':
        return 'operator'
    else:
        print("dont think I should be here")

# gets the whole problem after the opening paren
def cut_out_inside_parens(problem):
    paren_count = 0
    inside = deque([])
    while len(problem):
        character = problem.popleft()
        if character == '(':
            paren_count += 1
        if character == ')':
            if paren_count == 0:
                # Return the string of the inside of the parens and the string after it
                return (inside, problem)
            else:
                paren_count -= 1
        inside.append(character)

    print("failed to find close paren: " + str(problem))
    sys.exit()

def oper(operator, numbers):
    return numbers[0] + numbers[1] if operator == "+" else numbers[0] * numbers[1]

# problem is deque of characters in input line
def solve_recursive(problem):
    numbers = []
    operator = "none"
    while len(problem) > 0:
        next_char = problem.popleft()
        if next_char == " ":
            continue
        symb = symbol_type(next_char)
        if symb == "open":
            inside, problem = cut_out_inside_parens(problem)
            numbers.append(solve_recursive(inside))
        elif symb == "number":
            numbers.append(int(next_char))
        elif symb == "operator":
            operator = next_char

        if operator != "none" and len(numbers) == 2:
            numbers = [oper(operator, numbers)]
            operator = "none"

    return numbers[0]

sum_of_all = 0
for row in rows:
    q = deque(row)
    sum_of_all += solve_recursive(q)

print("Summed results of all rows: " + str(sum_of_all))
