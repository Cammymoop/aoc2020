import sys

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for row in raw_rows:
    rows.append(row.strip())

debug = False

def l_find(list, looking):
    try:
        return list.index(looking)
    except ValueError:
        return -1

def db_str(l):
    s = ""
    for c in l:
        s += str(c)
    return s

def solve_recursive(problem):
    global debug
    # convert to list
    lproblem = list(problem)

    first_paren = l_find(lproblem, '(')
    if debug and first_paren < 0:
        print("called with inner")
    loop = 0
    while first_paren > -1:
        if debug:
            print("loop" + str(loop) + ": " + db_str(lproblem))
            loop += 1
        last_p = lproblem

        open_i = first_paren
        for i in range(first_paren, len(lproblem)):
            if lproblem[i] == '(':
                open_i = i
            elif lproblem[i] == ')':
                result = solve_recursive(lproblem[open_i + 1:i])
                if debug:
                    print(result)
                if i + 1 < len(lproblem):
                    end = lproblem[i + 1:]
                else:
                    end = []
                lproblem = lproblem[0:open_i]
                lproblem.append(result)
                lproblem.extend(end)
                break

        if last_p == lproblem:
            print("infinite looping!")
            sys.exit()
        first_paren = l_find(lproblem, '(')
        debug = False

    # now solve all + from left to right
    # first convert all ints that are still strings
    for x in range(len(lproblem)):
        if type(lproblem[x]) == str and lproblem[x].isdigit():
            lproblem[x] = int(lproblem[x])

    first_plus = l_find(lproblem, '+')
    while first_plus > -1:
        if debug:
            print("ploop" + str(loop) + ": " + db_str(lproblem))
            loop += 1
        val = lproblem[first_plus - 1] + lproblem[first_plus + 1]
        if first_plus + 2 < len(lproblem):
            end = lproblem[first_plus + 2:]
        else:
            end = []
        lproblem = lproblem[:first_plus - 1]
        lproblem.append(val)
        lproblem.extend(end)
        first_plus = l_find(lproblem, '+')

    if debug:
        print("after plus: " + db_str(lproblem))

    # Only operation left is multiply
    product = 1
    for x in lproblem:
        if type(x) is int:
            product *= x

    if debug:
        print("finally: " + str(product))
    return product 

sum_of_all = 0
for row in rows:
    filtered_row = row.replace(" ", "")
    sum_of_all += solve_recursive(filtered_row)
    debug = False

print("Summed results of all rows: " + str(sum_of_all))
