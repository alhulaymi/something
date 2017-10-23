import datetime
old = []
new = []
with open("configs.csv","rb") as f:
    for line in f:
        if len(line) <= 1:
            continue
        new.append(line.strip().split("|"))

with open("configs_old.csv","rb") as f:
    for line in f:
        if len(line) <= 1:
            continue
        old.append(line.strip().split("|"))

print "Old: "+str(old)
print "New: "+str(new)
keys_indices = [0,1]
old_keys = []
for entry in old:
    old_keys.append([entry[x] for x in keys_indices])
#print old_keys
new_keys = []
for entry in new:
    new_keys.append([entry[x] for x in keys_indices])
#print new_keys

# getting the additions
additions = [x for x in new_keys if x not in old_keys]

# getting deletions
deleted = [x for x in old_keys if x not in new_keys]


# getting changes
changed = []
to_check = [x for x in old_keys if x not in deleted]
for pkey in to_check:
    old_values = []
    new_values = []
    for old_item in old:
        if all([(x in old_item) for x in pkey]):
            old_values = old_item
            break
    for new_item in new:
        if all([(x in new_item) for x in pkey]):
            new_values = new_item
            break
    #print old_values
    #print new_values

    same = all([(old_values[x]==new_values[x]) for x in range(0,len(old_values))])
    if not same:
        changed.append(pkey)
print "Added:\t"+str(additions)
print "Deleted:\t"+str(deleted)
print "Changed:\t"+str(changed)

now = datetime.datetime.now()
current_date = now.strftime("%m/%d/%Y")
for addition_keys in additions:
    target = []
    for item in new:

        match = all([(addition_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))])
        #print [(addition_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))]
        if match:
            target = item
            break
    if not match:
        raise ValueError("no match found for an added item in the new list of configs")
    new_row = target + [current_date,current_date]
    print "Adding:\t"+str(new_row)

for update_keys in changed:
    target = []
    for item in new:

        match = all([(update_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))])
        #print [(addition_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))]
        if match:
            target = item
            break
    if not match:
        raise ValueError("no match found for a changed item in the new list of configs")
    new_row = target + [current_date]
    print "Updating:\t"+str(new_row)

for delete_keys in deleted:
    target = []
    for item in old:

        match = all([(delete_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))])
        #print [(addition_keys[i]==item[keys_indices[i]]) for i in range(0,len(keys_indices))]
        if match:
            target = item
            break
    if not match:
        raise ValueError("no match found for a deleted item in the old list of configs")
    old_row = target
    print "Deleting:\t"+str(old_row)
