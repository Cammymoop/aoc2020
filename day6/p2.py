import operator
from functools import reduce

with open('input') as f:
    raw_rows = f.readlines()

rows = []
for raw in raw_rows:
    rows.append(raw.strip())

debug = True

group_id = 0
group_ans = []
last_blank = False

for row in rows:
    if group_id >= len(group_ans):
        group_ans.append(set(row))
    if len(row) < 1:
        if debug:
            #debug = False
            print("set: " + str(group_ans[group_id]))
            print("total answers: " + str(len(group_ans[group_id])))

        if not last_blank:
            group_id += 1
            last_blank = True
        continue

    last_blank = False
        
    group_ans[group_id] = group_ans[group_id].intersection(row)
    
total_ans = reduce(lambda a, x: a + len(x), group_ans, 0)


print("Total of groups yes answers: " + str(total_ans))

