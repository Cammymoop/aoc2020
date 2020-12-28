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

# Validation Functions
def get_num_validator(min, max):
    return lambda x: x.isnumeric() and int(x) >= min and int(x) <= max

def height_check(h):
    unit = h[-2:]
    if unit != 'cm' and unit != 'in':
        #invalid unit
        return False

    num_check = get_num_validator(150, 193) if unit == 'cm' else get_num_validator(59, 76)
    return num_check(h[:-2])

def hex_code_check(hex):
    if len(hex) != 7:
        return False
    if len(hex.strip('#0123456789abcdef')) > 0:
        return False
    return True

def color_abr_check(color):
    return color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def pid_check(pid):
    if not pid.isnumeric():
        return False
    return len(pid) == 9

field_requirements = {
    'byr': get_num_validator(1920, 2002),
    'iyr': get_num_validator(2010, 2020),
    'eyr': get_num_validator(2020, 2030),
    'hgt': height_check,
    'hcl': hex_code_check,
    'ecl': color_abr_check,
    'pid': pid_check,
}

def doc_is_valid(doc):
    for req in actual_required_fields:
        if not req in doc:
            return False

    for key in doc:
        if key in field_requirements:
            if not field_requirements[key](doc[key]):
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

