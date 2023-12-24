import re
# https://regex101.com/r/nH4nD3/3
debugPrint = True
from copy import deepcopy

def printGridWithSeen(grid, seen):
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            if (x,y) in seen:
                print("O", end="")
            else:
                print(grid[x][y], end="")
        print()

def dfs(grid, seenIn, pos):
    # print(f"pos = {pos}")
    x, y = pos
    seen = deepcopy(seenIn)
    seen.add(pos)
    if pos == (xlen-1, ylen-2):
        # printGridWithSeen(grid, seen)            
        return 1
    n, w, s, e = 0, 0, 0, 0
    dn, dw, ds, de = 0, 0, 0, 0
    test = False
    # if pos == (5, 3):
    #     print(f"AAAAAAAAAAAAAAAAAAAAAH {pos}")
    #     test = True
    # no slopes into walls (eg. ">#") nor a slope into the exit, so omitting some checks
    if grid[x-1][y] not in ["#", "<", "v", ">"] and (x-1,y) not in seen:
        # if test: print("EEP ^")
        if grid[x-1][y] == "^":
            # print(f"jumping ^ from {pos}")
            n = dfs(grid, seen, (x-2, y))
            dn=1 if n else 0
        else:
            n = dfs(grid, seen, (x-1, y))
    if grid[x][y-1] not in ["#", "^", "v", ">"] and (x,y-1) not in seen:
        # if test: print("EEP <")
        if grid[x][y-1] == "<":
            # print(f"jumping < from {pos}")
            w = dfs(grid, seen, (x, y-2))
            dw=1 if w else 0
        else:
            w = dfs(grid, seen, (x, y-1))
    if grid[x+1][y] not in ["#", "^", "<", ">"] and (x+1,y) not in seen:
        # if test: print("EEP v")
        if grid[x+1][y] == "v":
            # print(f"jumping v from {pos}")
            s = dfs(grid, seen, (x+2, y))
            ds=1 if s else 0
        else:
            s = dfs(grid, seen, (x+1, y))
    if grid[x][y+1] not in ["#", "^", "<", "v"] and (x,y+1) not in seen:
        # if test: print("EEP >")
        if grid[x][y+1] == ">":
            # print(f"jumping > from {pos}")
            e = dfs(grid, seen, (x, y+2))
            de=1 if e else 0
        else:
            e = dfs(grid, seen, (x, y+1))
    options = [n+dn, w+dw, s+ds, e+de]
    # print(f"{pos} returning: {options}; len(seen)={len(seen)}")
    result = max(options)
    return 1+result if result else 0




with open("input23.txt") as input:
    # print("hello world")
    
    grid = []
    for line in input:
        grid.append(list(line.strip()))
        pass
    # for row in grid:
    #     print(row)
    xlen = len(grid)
    ylen = len(grid[0])

    # printGridWithSeen(grid, {})

    seen = {(0,1)}
    start = (1, 1)
    # result = dfs(grid, seen, start)
    # print(result)

    # dfs via stack data structure
    # key = (x, y, [in+1/out=-1], d)
    stack = [(1,1,1,1)]
    results = []
    maxResult = 0
    while stack:
        item = stack.pop()
        x, y, inOut, d = item
        # backtracking out of the stack
        if inOut == -1:
            grid[x][y] = "."
            continue
        if inOut == 1:
            grid[x][y] = "O"
            stack.append((x,y,-1,d))
        # print(f"pos = {pos}")
        if (x,y) == (xlen-1,ylen-2):
            # printGridWithSeen(grid, {})
            if d > maxResult:
                 print(f"new max: {maxResult}")
            maxResult = max(maxResult, d)
            continue
        if grid[x-1][y] not in ["#", "O"]:
                stack.append((x-1,y,1,d+1))
        if grid[x][y-1] not in ["#", "O"]:
                stack.append((x,y-1,1,d+1))
        if grid[x+1][y] not in ["#", "O"]:
                stack.append((x+1,y,1,d+1))
        if grid[x][y+1] not in ["#", "O"]:
                stack.append((x,y+1,1,d+1))

    print(f"{maxResult}")


# 6046 < 6082 < ans
# wrong: 6250, 6251

# found: 6134? 6266? 
# maybe jump to ~6332 ish to see if high/low?
print("goodbye world")