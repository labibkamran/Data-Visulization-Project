import json

# path to your file
path = "dataset_split.json"

with open(path, "r") as f:
    data = json.load(f)

train = data.get("train_files", [])
val = data.get("val_files", [])
test = data.get("test_files", [])

# Convert to sets for fast comparison
train_set = set(train)
val_set = set(val)
test_set = set(test)


# ---- Check duplicates inside each split ----
def find_duplicates(lst):
    seen = set()
    dup = set()
    for x in lst:
        if x in seen:
            dup.add(x)
        seen.add(x)
    return dup

dup_train = find_duplicates(train)
dup_val = find_duplicates(val)
dup_test = find_duplicates(test)

# ---- Check leakage between splits ----
leak_train_val = train_set & val_set
leak_train_test = train_set & test_set
leak_val_test = val_set & test_set

# ---- Print results ----
print("\n==== DUPLICATES IN SPLITS ====")
print(f"Train duplicates: {len(dup_train)}")
print(f"Val duplicates:   {len(dup_val)}")
print(f"Test duplicates:  {len(dup_test)}")

print("\n==== LEAKAGE BETWEEN SPLITS ====")
print(f"Train ↔ Val overlaps: {len(leak_train_val)}")
print(f"Train ↔ Test overlaps: {len(leak_train_test)}")
print(f"Val ↔ Test overlaps:   {len(leak_val_test)}")

# Print actual leaked items (optional)
if leak_train_val:
    print("\nItems in BOTH Train and Val:")
    for item in leak_train_val:
        print(" -", item)

if leak_train_test:
    print("\nItems in BOTH Train and Test:")
    for item in leak_train_test:
        print(" -", item)

if leak_val_test:
    print("\nItems in BOTH Val and Test:")
    for item in leak_val_test:
        print(" -", item)
