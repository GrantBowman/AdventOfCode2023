import re
# https://regex101.com/r/nH4nD3/3

def partSum(part):
    result = 0
    for k in part:
        result += part[k]
    return result

with open("input19.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    i = 0
    # workflows have an order, so keep as arrays of strings to be parsed as needed. use labels to point to each workflow
    workflows = {}
    # items are dicts of different parts. have an array of dicts
    parts = []

    # gather the workflows
    while True:
        line = input.readline().strip()
        if line == "":
            break
        foundGroups = re.findall(r"([^{},]+)", line)
        label = foundGroups[0]
        guts = foundGroups[1:-1]
        finalDest = foundGroups[-1]
        workflow = [[int(x) if x.isdigit() else x for x in re.findall(r"(.+)([<>])(.+):(.+)", wf)[0]] for wf in guts]
        workflows[label] = (workflow, finalDest)
    # debug print the workflows
    if debugPrint: 
        for k in workflows:
            print(k, workflows[k][0], workflows[k][1])
    
    # gather the parts
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
    # debug print the parts
    if debugPrint: 
        for p in parts:
            print(p)

    # now run the alg
    for p in parts:
        if debugPrint: print(f"testing part: {p}")
        curState = "in"
        # walk through the states until reach and A or R
        while True:
            instList = workflows[curState][0]
            if debugPrint: print(f"working in {curState}: {instList} | {workflows[curState][1]}")
            transferred = False
            for inst in instList:
                var, cmp, val, dest = inst 
                if debugPrint: print(var, cmp, val, dest)
                if cmp == "<" and (p[var] < val):
                    curState = dest
                    transferred = True
                    break
                if cmp == ">" and (p[var] > val):
                    curState = dest
                    transferred = True
                    break
            if not transferred:
                curState = workflows[curState][1]

            if debugPrint: print(f"inst done. state={curState}, transferred? {transferred}")

            # hope we reached one?
            if curState == "A":
                result = partSum(p)
                sum += result
                if debugPrint: print(f"accepted, + {result}")
                break
            if curState == "R":
                if debugPrint: print("rejected")
                break
    print(sum)

        
print("goodbye world")