import operator
from functools import reduce

with open('input') as f:
    rows = f.readlines()

raw_documents = [[]]
doc_index = 0

for row in rows:
    trimmed = row.strip()
    # if we've read some already for this doc and theres a blank row, start reading the next doc
    if len(raw_documents[doc_index]) > 0 and len(trimmed) == 0:
        doc_index += 1
        raw_documents.append([])
        continue

    words = trimmed.split(' ')
    for w in words:
        raw_documents[doc_index].append(w)

documents = []
for d in raw_documents:
    doc_dict = {}
    for item in d:
        doc_dict[item.split(':')[0]] = item.split(':')[1]
    documents.append(doc_dict)

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
actual_required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def doc_is_valid(doc):
    for req in actual_required_fields:
        if not req in doc:
            return False

    return True


invalids = 0
valids = 0
for doc in documents:
    if doc_is_valid(doc):
        valids += 1
    else:
        invalids += 1

print("Total documents: " + str(len(documents)))
print("Valid documents: " + str(valids))
print("Invalid documents: " + str(invalids))

