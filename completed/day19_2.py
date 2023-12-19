import re
# https://regex101.com/r/nH4nD3/3
from copy import deepcopy
# import copy 

with open("input19.txt") as input:
    print("hello world")
    debugPrint = False

    # workflows have an order, so keep as arrays of strings to be parsed as needed. use labels to point to each workflow
    workflows = {}
    # items are dicts of different parts. have an array of dicts
    parts = []

    while True:
        line = input.readline().strip()
        if line == "":
            break
        foundGroups = re.findall(r"([^{},]+)", line)
        # print(line, foundGroups)
        label = foundGroups[0]
        guts = foundGroups[1:-1]
        finalDest = foundGroups[-1]
        workflow = [[int(x) if x.isdigit() else x for x in re.findall(r"(.+)([<>])(.+):(.+)", wf)[0]] for wf in guts]
        workflows[label] = (workflow, finalDest)
    if debugPrint: 
        for k in workflows:
            print(k, workflows[k][0], workflows[k][1])
    
    # finding parts doesnt matter for pt2
    while True:
        line = input.readline().strip()
        if line == "":
            break
        foundGroups = re.findall(r"([^{},]+)", line)
        part = {}
        for g in foundGroups:
            found = re.findall(r"([xmas])=(\d+)", g)
            k,v = found[0]
            part[k] = int(v)
        parts.append(part)
    if debugPrint: 
        for p in parts:
            print(p)
    
    #     X   -    M   -    A   -    S   -
    q = [[1, 4000, 1, 4000, 1, 4000, 1, 4000, "in"]]
    accepted = []
    rejected = []
    while q:
        item = q.pop()
        minX, maxX, minM, maxM, minA, maxA, minS, maxS, state = item
        # base cases: found A or R
        if state == "A":
            accepted.append(item)
            # print(f"Accepted {curVar} {curVarMin}-{curVarMax}")
            continue
        if state == "R":
            rejected.append(item)
            # print(f"Rejected {curVar} {curVarMin}-{curVarMax}")
            continue
        instList = workflows[state][0]
        for inst in instList:
            var, cmp, val, dest = inst 
            if debugPrint: print(var, cmp, val, dest)
            # trim if its our var
            if cmp == "<":
                i = "xmas".index(var)*2
                # add item with the restraint
                newItem = deepcopy(item)
                newItem[i+1] = val-1
                newItem[-1] = dest
                q.append(newItem)
                # continue this set of inst with the negation
                item[i] = val
            elif cmp == ">":
                i = "xmas".index(var)*2
                # add item with the restraint
                newItem = deepcopy(item)
                newItem[i] = val+1
                newItem[-1] = dest
                q.append(newItem)
                # continue this set of inst with the negation
                item[i+1] = val
        # made it through inst
        item[-1] = workflows[state][1]
        q.append(deepcopy(item))
    sum = 0
    if debugPrint:
        for r in rejected:
            print(r)
        for a in accepted:
            print(a)
    for a in accepted:
        minX, maxX, minM, maxM, minA, maxA, minS, maxS, state = a
        sx = maxX-minX+1 
        sm = maxM-minM+1
        sa = maxA-minA+1
        ss = maxS-minS+1
        result = sx*sm*sa*ss
        sum += result
        if debugPrint: print(sx, sm, sa, ss, result, sum)

    print(sum)

        
print("goodbye world")