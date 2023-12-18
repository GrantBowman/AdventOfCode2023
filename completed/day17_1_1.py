import re
# https://regex101.com/r/nH4nD3/3
from collections import deque
from sys import maxsize


stepLimit = 3
n = 0b1000
w = 0b0100
s = 0b0010
e = 0b0001
# DP[key] is the shortest distance to get to that spot
# NO cuz loops. its the fisr titme
DP = {}
visited = {}
def findShortest(grid, x, y, going=0, steps=0, depth=0):
    xlen = len(grid)
    ylen = len(grid[0])
    key = (x, y, going, steps, depth)
    depth += 1
    # print(f"depth={depth} key={key} hehehe")
    if key in visited:
        print(f"returning from visited")
        return DP[key]
    visited[(x, y)] = True
    if key in DP:
        print(f"returning from DP")
        return DP[key]
    if (x==xlen-1) and (y==ylen-1):
        DP[key] = grid[x][y]
        return DP[key]
    minResult = maxsize
    # go every direction unless steplimit, add 1 to steps if going the same direction
    # all loops are > 0, so dont revisit nodes (ie. dont travel to already visited nodes)
    # e
    steps = steps+1 if going == e else 0
    if (y < ylen-1) and ((going!=e) or (steps<stepLimit)):
        if (x, y+1) not in visited:
            result = findShortest(grid, x, y+1, e, steps, depth)
            result += grid[x][y+1]
            minResult = min(minResult, result)
    # s
    steps = steps+1 if going == s else 0
    if (x < xlen-1) and ((going!=s) or (steps<stepLimit)):
        if (x+1, y) not in visited:
            result = findShortest(grid, x+1, y, s, steps, depth)
            result += grid[x+1][y]
            minResult = min(minResult, result)
    # n
    steps = steps+1 if going == n else 0
    if (x > 0) and ((going!=n) or (steps<stepLimit)):
        if (x-1, y) not in visited:
            result = findShortest(grid, x-1, y, n, steps, depth)
            result += grid[x-1][y]
            minResult = min(minResult, result)
    # w
    steps = steps+1 if going == w else 0
    if (y > 0) and ((going!=w) or (steps<stepLimit)):
        if (x, y-1) not in visited:
            result = findShortest(grid, x, y-1, w, steps, depth)
            result += grid[x][y-1]
            minResult = min(minResult, result)
    DP[key] = minResult
    return DP[key]




with open("input17_demo.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True


    grid = []
    for line in input:
        line = line.strip()
        grid.append([int(x) for x in line]) 
    # for row in grid:
    #     print(''.join([str(x) for x in row]))

    distGrid = [[999 for x in range(0,len(grid[0]))] for y in range(0,len(grid))]
    visitedGrid = [[False for x in range(0,len(grid[0]))] for y in range(0,len(grid))]

    result = findShortest(grid, 0, 0, 0, 0)

    xlen = len(grid)
    ylen = len(grid[0])
    for key in DP:
        x = key[0]
        y = key[1]
        distGrid[x][y] = min(distGrid[x][y], DP[key])
    for row in distGrid:
        print(row)

    print(result)


# 803 < ans < ???


print("goodbye world")
