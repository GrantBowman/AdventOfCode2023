import re
# https://regex101.com/r/nH4nD3/3
from copy import deepcopy
from collections import deque

# global variables because this is a mess
debugPrint = False
# maxSteps = 100
maxSteps = 26501365
parity = maxSteps%2

# boundary being copies of grid away from the origin grid (0,0)
# paths to things beyond this are dominated by pathing through the "highway"
# and thus can just add a constant to the distance to get to within that boundary 
boundary = 4

# add a line of options based on how many grids we can continue beyong
# n 1 2 3 4
extendEdgeSeen = {}
def extendEdge(d, maxSteps, elen):
    key = (d, maxSteps, elen)
    if key in extendEdgeSeen:
        return extendEdgeSeen[key]
    ext = (maxSteps-d) // elen
    result = 0
    # sanity check within bounds and parity matches
    for i in range(1, ext+1):
        if (d+i*elen)<=maxSteps and (d+i*elen)%2==parity%2:
            result += 1
    extendEdgeSeen[key] = result
    print(f"extendEdge {d, ext}: {result}")
    return result

# add a triange of options based on how many grids we can continue beyond
# a = 4
# 4
# 3 3
# 2 2 2
# 1 1 1 1
# n ? ? ? ?

# n 1 2 3 4 <- final edge add
extendCornerSeen = {}
def extendCorner(d, maxSteps, elen):
    key = (d, maxSteps, elen)
    if key in extendCornerSeen:
        return extendCornerSeen[key]
    ext = (maxSteps-d) // elen
    result = 0
    # sanity check within bounds and parity matches
    for i in range(1, ext+1):
        if (d+i*elen)<=maxSteps and (d+i*elen)%2==parity%2:
            result += i+1
    #         result += ext+1 - i
    # result += ext
    extendCornerSeen[key] = result
    print(f"extendCorner {d, ext}: {result}")
    return result


with open("input21.txt") as input:
    print("hello world")
    print(f"maxSteps = {maxSteps}")

    i = 0
    grid = []
    for line in input:
        grid.append(list(line.strip()))
        pass


    ### first, get some information about the problem

    # make the step grid
    # for part2 holds the (x,y) of the parallel universes
    # if steps of the grid left, gets added to the rigt side with a (x-1,y) universe
    xlen = len(grid)
    ylen = len(grid[0])
    sx = None
    sy = None
    # find start spot
    for x in range(0,xlen):
        for y in range(0,ylen):
            if grid[x][y] == "S":
                sx, sy = x, y


    ### find distances to spots in grid.
    # each grid holds a dictionary of parallel universes and the steps away

    stepQueue = deque()
    seen = {}
    lastd = 0
    boundary = 4
    # key = dimX, dimY, x, y dist
    stepQueue.append((0, 0, sx, sy, 0))
    while stepQueue:
        dimX, dimY, x, y, d = stepQueue.popleft()
        key = (dimX, dimY, x, y)
        if d > maxSteps:
            continue
        if abs(dimX) > boundary or abs(dimY) > boundary:
            continue
        # tracking seen to keep distance (+parity) without overwriting universes like before >.<
        if key in seen:
            continue
        else:
            seen[key] = d
        # distance beyond boundary, leave
        # if debugPrint or d != lastd:
        #     print(f"looking at {key}: {d} {'+' if d%2==parity else ''}")
        #     lastd = d

        # n inbounds
        if x > 0 and grid[x-1][y] != "#":
            if debugPrint: print(f"n inbounds")
            stepQueue.append((dimX,dimY,x-1,y,d+1))
            
        # n outbounds
        elif x==0 and grid[xlen-1][y] != "#":
            if debugPrint: print(f"n outbounds")
            stepQueue.append((dimX-1,dimY,xlen-1,y,d+1))

        # w inbounds
        if y > 0 and grid[x][y-1] != "#":
            if debugPrint: print(f"w inbounds")
            stepQueue.append((dimX,dimY,x,y-1,d+1))
        # w outbounds
        elif y==0 and grid[x][ylen-1] != "#":
            if debugPrint: print(f"w outbounds")
            stepQueue.append((dimX,dimY-1,x,ylen-1,d+1))

        # s inbounds
        if x < xlen-1 and grid[x+1][y] != "#":
            if debugPrint: print(f"s inbounds")
            stepQueue.append((dimX,dimY,x+1,y,d+1))
        # s outbounds
        elif x==xlen-1 and grid[0][y] != "#":
            if debugPrint: print(f"s outbounds")
            stepQueue.append((dimX+1,dimY,0,y,d+1))

        # e inbounds
        if y < ylen-1 and grid[x][y+1] != "#":
            if debugPrint: print(f"e inbounds")
            stepQueue.append((dimX,dimY,x,y+1,d+1))
        # e outbounds
        elif y==ylen-1 and  grid[x][0] != "#":
            if debugPrint: print(f"e outbounds")
            stepQueue.append((dimX,dimY+1,x,0,d+1))

    print(f"len(seen) = {len(seen)}")

    '''
    print(f"brute force result finding =")
    # print(seen)
    result = 0
    inGridSum = 0
    # boundary = 3
    # 317098492122624 from resetting boundary = 3 above ^
    # 317095357476328 when not reset.. hmmm
    for (dimX, dimY, x, y), d in seen.items():
        # print(f"result loop {(dimX, dimY, x, y), d}")
        if d > maxSteps:
            continue
        if d%2 != parity:
            continue
        if dimX > boundary or dimY > boundary:
            continue
        result += 1
        inGridSum += 1
        # extend additionally in triangle if corner
        if abs(dimX)==boundary and abs(dimY)==boundary:
            result += extendCorner(d, maxSteps, xlen)
        # extend beyond boundaries using MATHS!
        elif abs(dimX)==boundary or abs(dimY)==boundary:
            result += extendEdge(d, maxSteps, xlen)
    print(f"inGridSum = {inGridSum}")
    print(f"result brute force = {result}")
    '''

    inGridSum = 0
    edgeSum = 0
    edgeCount = 0
    cornerSum = 0
    cornerCount = 0
    result = 0
    OPT = [-3, -2, -1, 0, 1, 2, 3]
    for x in range(0,xlen):
        for y in range(0,ylen):
            if (0,0,x,y) in seen:
                for dimX in OPT:
                    for dimY in OPT:
                        d = seen[(dimX,dimY,x,y)]
                        if d%2==parity and d<=maxSteps:
                            result+=1
                            inGridSum+=1
                        if dimX in [min(OPT),max(OPT)] and dimY in [min(OPT),max(OPT)]:
                            temp = extendCorner(d,maxSteps,xlen)
                            result += temp
                            cornerSum += temp
                            cornerCount += 1
                        elif dimX in [min(OPT),max(OPT)] or dimY in [min(OPT),max(OPT)]:
                            temp = extendEdge(d,maxSteps,xlen)
                            result += temp
                            edgeSum += temp
                            edgeCount += 1
    print(f"inGridSum = {inGridSum}")
    for item in sorted(list(seen)):
        print(f"{item}: {seen[item]}")
    print(f"inGridSum = {inGridSum}")
    print(f"cornerCount = {cornerCount}")
    print(f"cornerSum = {cornerSum}")
    print(f"edgeCount = {edgeCount}")
    print(f"edgeSum = {edgeSum}")
    print(f"result brute force = {result}")




    #  attempt 2            attempt 3
    # 317095357538312 < 317098492223420 < ans
    #                       317098496206572    B=6
    #                       317098499972600    B=7
    #                       317098507969716    B=8
    #                 which, doubled, is still < jp's
    # jp shows ............ 634549784009844


    # i used to have a 2d array of dimension dicts that i like but it was getting cumbersome to keep checking spots we dont care about :(
    # but i liked it so here is the code
    '''
    stepGrid = [[{} for y in row] for row in grid]
    emptyStepGrid = deepcopy(stepGrid)
    stepGrid[sx][sy][(0,0)] |= even

    # -=-    -=-    -=-

    # run iters
    for i in range(0,maxSteps):
        newStepGrid = deepcopy(emptyStepGrid)
        curParity = even if i%2 else odd
        # grid space
        for x in range(0,xlen):
            for y in range(0,ylen):
                if stepGrid[x][y].items():
                    if debugPrint: print(f"universes for ({x}, {y}):")
                # grid universes
                for (xx, yy), c in stepGrid[x][y].items():
                    # distance beyond boundary, leave
                    if abs(xx) > boundary or abs(yy) > boundary:
                        continue
                    if debugPrint: print(f"({xx}, {yy}), {c}")
                    # n inbounds
                    if x > 0 and grid[x-1][y] != "#":
                        if debugPrint: print(f"n inbounds")
                        newStepGrid[x-1][y][(xx,yy)] |= curParity #= newStepGrid[x-1][y].get((xx,yy), 0) + c
                    # n outbounds
                    elif x==0 and grid[xlen-1][y] != "#":
                        if debugPrint: print(f"n outbounds")
                        newStepGrid[xlen-1][y][(xx-1,yy)] |= curParity #= newStepGrid[xlen-1][y].get((xx-1,yy), 0) + c

                    # w inbounds
                    if y > 0 and grid[x][y-1] != "#":
                        if debugPrint: print(f"w inbounds")
                        newStepGrid[x][y-1][(xx,yy)] |= curParity # = newStepGrid[x][y-1].get((xx,yy), 0) + c
                    # w outbounds
                    elif y==0 and grid[x][ylen-1] != "#":
                        if debugPrint: print(f"w outbounds")
                        newStepGrid[x][ylen-1][(xx,yy-1)] |= curParity #= newStepGrid[x][ylen-1].get((xx,yy-1), 0) + c

                    # s inbounds
                    if x < xlen-1 and grid[x+1][y] != "#":
                        if debugPrint: print(f"s inbounds")
                        newStepGrid[x+1][y][(xx,yy)] |= curParity #= newStepGrid[x+1][y].get((xx,yy), 0) + c
                    # s outbounds
                    elif x==xlen-1 and grid[0][y] != "#":
                        if debugPrint: print(f"s outbounds")
                        newStepGrid[0][y][(xx+1,yy)] |= curParity #= newStepGrid[0][y].get((xx+1,yy), 0) + c

                    # e inbounds
                    if y < ylen-1 and grid[x][y+1] != "#":
                        if debugPrint: print(f"e inbounds")
                        newStepGrid[x][y+1][(xx,yy)] |= curParity #= newStepGrid[x][y+1].get((xx,yy), 0) + c
                    # e outbounds
                    elif y==ylen-1 and  grid[x][0] != "#":
                        if debugPrint: print(f"e outbounds")
                        newStepGrid[x][0][(xx,yy+1)] |= curParity #= newStepGrid[x][0].get((xx,yy+1), 0) + c
        stepGrid = newStepGrid
    
    # print(f"\tbrute force =")
    result = 0
    for x in range(0,len(stepGrid)):
        for y in range(0,len(stepGrid[x])):
            for (xx, yy), p in stepGrid[x][y].items():
                if p != parity :
                    continue
                result += 1
                # extend beyond boundaries using MATHS!
                if abs(xx)==boundary or abs(yy)==boundary:
                    result += extendEdge(c, maxSteps, xlen)
                # extend additionally in triangle if corner
                if abs(xx)==boundary and abs(yy)==boundary:
                    result += extendCorner(c, maxSteps, xlen)
    print(f"result brute force = {result}")
    '''
    

print("goodbye world")