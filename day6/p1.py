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

for row in rows:
    if group_id >= len(group_ans):
        group_ans.append(set([]))
    if len(row) < 1:
        if debug:
            debug = False
            print("set: " + str(group_ans[group_id]))
            print("total answers: " + str(len(group_ans[group_id])))

        if len(group_ans[group_id]) > 0:
            group_id += 1
        continue
        
    group_ans[group_id] = group_ans[group_id].union(row)
    
total_ans = reduce(lambda a, x: a + len(x), group_ans, 0)


print("Total of groups yes answers: " + str(total_ans))

