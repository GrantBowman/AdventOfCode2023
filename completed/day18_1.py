import re
# https://regex101.com/r/nH4nD3/3
from collections import deque

def fill(grid, x, y, val):
    q = deque()
    q.append((x, y))
    xlen = len(grid)
    ylen = len(grid[0])
    while q:
        x, y = q.popleft()
        # print(x, y)
        if grid[x][y] != 0:
            continue
        grid[x][y] = val
        if x>0:
            q.append((x-1, y))
        if x<xlen-1:
            q.append((x+1, y))
        if y>0:
            q.append((x, y-1))
        if y<ylen-1:
            q.append((x, y+1))

with open("input18.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    instructions = []
    i = 0
    for line in input:
        line = line.strip()
        found = re.match(r"(\w) (\d+) (.+)", line)
        # print(found.groups())
        d, n, inst = found.groups()
        instructions.append((d, int(n), inst))

        # R num stuff
        # grid.append(line)
        # pitGrid.append([0 for x in line])
        pass

    xStart = 0
    x = 0
    xMin = 0
    xMax = 0
    y = 0
    yStart = 0
    yMin = 0
    yMax = 0
    for inst in instructions:
        if inst[0] == "U":
            x -= inst[1]
        if inst[0] == "D":
            x += inst[1]
        if inst[0] == "L":
            y -= inst[1]
        if inst[0] == "R":
            y += inst[1]
        xMax = max(xMax, x)
        xMin = min(xMin, x)
        yMax = max(yMax, y)
        yMin = min(yMin, y)
    dx = xMax-xMin
    dy = yMax-yMin
    # print(dx, dy)

    grid = [[0 for y in range(0,dy+1+2)] for x in range(0,dx+1+2)]
    pitGrid = [[0 for y in range(0,dy+1+2)] for x in range(0,dx+1+2)]
    x = -xMin+1
    y = -yMin+1
    # print(x, y)
    # grid[0][0] = 1
    for inst in instructions:
        if inst[0] == "U":
            d = (-1, 0)
        if inst[0] == "D":
            d = (1, 0)
        if inst[0] == "L":
            d = (0, -1)
        if inst[0] == "R":
            d = (0, 1)
        dx, dy = d
        for i in range(0,inst[1]):
            x += dx
            y += dy
            # print(f"({x},{y}) {i}/{inst[1]} in {inst}")
            grid[x][y] = 1

    



    # print built grid
    if debugPrint:
        for row in grid:
            print(''.join([str(a) for a in row]))
    # fill
    # q = queue()
        
    # fill "outter"
    fill(grid, 0, 0, 2)
    finished = False
    # find "inner"
    for i in range(0, len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 0:
                fill(grid, i, j, 3)
                finished = True
                break
        if finished:
            break
    # count regions
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for i in range(0, len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 1:
                sum1 += 1
            if grid[i][j] == 2:
                sum2 += 1
            if grid[i][j] == 3:
                sum3 += 1



    # print built grid
    if debugPrint:
        for row in grid:
            print(''.join([str(a) for a in row]))

    print(f"should be inner: inner={sum3}, border inclusive={sum1+sum3}")
    print(f"should be outer: inner={sum2}, border inclusive={sum1+sum2}")
    print(f"border: inner={sum1}")

    # '''
    # print(len(grid), len(grid[0]))
    # print(len(pitGrid), len(pitGrid[0]))
    # calculate inner grid space
        
    # for i in range(0, len(grid)):
    #     for j in range(0,len(grid[i])):
    #         pass

    # for row in pitGrid:
    #     print(row)

    # print(sum)
    # '''


    #    ###.###
    #    #.###.#
    #    #.....#
    #    ##....#
    #    .#.##.#
    #    .######

print("goodbye world")