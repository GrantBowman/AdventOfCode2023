import re
# https://regex101.com/r/nH4nD3/3

with open("input8.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    i = 0
    directions = input.readline()[:-1]
    if debugPrint: print(f"directions = \'{directions}\'")
    # eat the separator
    input.readline()

    nodes = {}
    for line in input:
        # (?:(\w+)+)
        found = re.match(r"(\w+) = \(((?:(?:\w+)+(?:, )?)+)\)", line)
        label = found.group(1)
        paths = found.group(2).split(", ")
        nodes[label] = paths
        pass

    # traverse
    cur = "AAA"
    while True:
        if debugPrint: print(f"cur = {cur}, i = {i}")
        if cur == "ZZZ":
            break
        rl = 0 if directions[i] == "L"  else 1
        i += 1
        # loop over directions
        if i >= len(directions):
            i = 0
        sum +=1
        if debugPrint: print(f"options = {nodes[cur]} going {rl}")
        cur = nodes[cur][rl]
    for n in nodes.items():
        if debugPrint: print(n)
print(sum)
print("goodbye world")