import re
# https://regex101.com/r/nH4nD3/3
from collections import deque
from sys import maxsize
import copy
import heapq 

stepLimit = 3
n = 0b1000
w = 0b0100
s = 0b0010
e = 0b0001

def getInHeap(toVisitHeap, x1=None, y1=None, l1=None):
    results = []
    for item in toVisitHeap:
        dist, x2, y2, l2 = item
        if (not x1 or x1==x2) and (not y1 or y1==y2) and (not l1 or l1==l2):
            results.append(item)
    return results

def updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x, y, level, fromDist):
    # add to visited if not in
    if visitGrid[level][x][y] == 0:
        visitGrid[level][x][y] = 1
        dist = fromDist + inputGrid[x][y]
        distGrid[level][x][y] = dist
        heapq.heappush(toVisitHeap, (dist, x, y, level))
    '''
    # else update its value
    elif visitGrid[level][x][y] == 1:
        dist = min(distGrid[level][x][y], fromDist + inputGrid[x][y])
        distGrid[level][x][y] = dist
        # update every level in the grid
        for item in getInHeap(toVisitHeap, x, y, level):
            # 
            newDist = min(dist,item[0])
            heapq.heapreplace(toVisitHeap, (item[0], x, y, level))
    '''
    # put it back in if the path could be shorter
    # elif visitGrid[level][x][y] == 2:
    #     dist = curDist + inputGrid[x][y]
    #     if dist < distGrid[level][x][y]:
    #         distGrid[level][x][y] = dist
    #         visitGrid[level][x][y] = 1
    #         heapq.heappush(toVisitHeap, (dist, x, y, level))

with open("input17.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    stepLimit = 3
    bigGrid =[]
    inputGrid = []
    # the (0, 0) is only used for the beginning. perhaps just start with all (0,0) in n1, w1, s1, e1?
    # 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11
    # n1, n2, n3, w1, w2, w3, s1, s2, s3, e1, e2, e3 
    for line in input:
        line = line.strip()
        inputGrid.append([int(x) for x in line])
    for direction in [n, w, s, e]:
        for i in range(0, stepLimit):
            bigGrid.append(copy.deepcopy(inputGrid))

    # remember - moving up costs 0
    # distGrid  = [[[maxsize for x in row] for row in g] for g in bigGrid]
    distGrid  = [[[999 for x in row] for row in g] for g in bigGrid]
    visitGrid = [[[      0 for x in row] for row in g] for g in bigGrid]
    for g in distGrid:
        g[0][0] = 0
    # print(f"levels={len(bigGrid)}")
    # print(f"x={len(bigGrid[0])}")
    # print(f"y={len(bigGrid[0][0])}")
    # print("can you hear me")
    # print(bigGrid)
    # for row in visitGrid[0]:
    #     for val in row:
    #         print(val, end=" ")
    #     print()
    # print("yes i can hear you")

    # define levels
    n1 = 0
    n2 = 1
    n3 = 2
    w1 = 3
    w2 = 4
    w3 = 5
    s1 = 6
    s2 = 7
    s3 = 8
    e1 = 9
    e2 = 10
    e3 = 11
    levelList = ["n1", "n2", "n3", "w1", "w2", "w3", "s1", "s2", "s3", "e1", "e2", "e3"]
    toVisitHeap = []
    # (dist, x, y, level)
    heapq.heappush(toVisitHeap, (0, 0, 0, -1))
    # heapq.heappush(toVisitHeap, (0, 0, 0, w1))
    # heapq.heappush(toVisitHeap, (0, 0, 0, s1))
    # heapq.heappush(toVisitHeap, (0, 0, 0, e1))

    # dijkstra:
    # pull lowest from heap
    # fix neighbors in distGrid
    # add neighbors in toVisitHeap if their distGrid val is max
    # repeat
    # at end, grab the distance of endpoints at each level and compare

    xlen = len(inputGrid)
    ylen = len(inputGrid[0])
    while True:
        if len(toVisitHeap) == 0:
            break
        curDist, x, y, level = heapq.heappop(toVisitHeap)
        if debugPrint: print(f"dist={curDist}, @({x},{y}) {levelList[level]}, level={level}, len(heap)={len(toVisitHeap)}")

        # n
        if (x > 0):
            # already went 3 in a row
            if level == n3:
                pass
            elif level in [n1, n2]:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x-1},{y})[{levelList[level+1]}] from n23")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x-1, y, level+1, curDist)
            else:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x-1},{y})[{levelList[n1]}] from n1")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x-1, y, n1, curDist)
        # w
        if (y > 0):
            # already went 3 in a row
            if level == w3:
                pass
            elif level in [w1, w2]:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x},{y-1})[{levelList[level+1]}] from w23")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x, y-1, level+1, curDist)
            else:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x},{y-1})[{levelList[w1]}] from w1")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x, y-1, w1, curDist)
        # s
        if (x < xlen-1):
            # already went 3 in a row
            if level == s3:
                pass
            elif level in [s1, s2]:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x+1},{y})[{levelList[level+1]}] from s23")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x+1, y, level+1, curDist)
            else:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x+1},{y})[{levelList[s1]}] from s1")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x+1, y, s1, curDist)
        # e
        if (y < ylen-1):
            # already went 3 in a row
            if level == e3:
                pass
            elif level in [e1, e2]:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x},{y+1})[{levelList[level+1]}] from e23")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x, y+1, level+1, curDist)
            else:
                if debugPrint: print(f"({x},{y})[{levelList[level]}] to ({x},{y+1})[{levelList[e1]}] from e1")
                updateDijkstra(toVisitHeap, distGrid, visitGrid, inputGrid, x, y+1, e1, curDist)
        visitGrid[level][x][y] = 2

    # condense the shortest paths for every spot
    resultGrid = [[999 for x in row] for row in inputGrid]
    for level in range(0, len(distGrid)):
        for x in range(0,len(distGrid[level])):
            for y in range(0,len(distGrid[level][x])):
                dist = min(resultGrid[x][y], distGrid[level][x][y])
                resultGrid[x][y] = dist
    # print the result grid
    debugPrint = True
    for x in range(0,len(resultGrid)):
        for y in range(0,len(resultGrid[x])):
            if debugPrint: print(f"{resultGrid[x][y]: >4}", end="")
        if debugPrint: print()
    if debugPrint: print(f"Here is the original inputGrid")
    for x in range(0,len(inputGrid)):
        for y in range(0,len(inputGrid[x])):
            if debugPrint: print(f"{inputGrid[x][y]: >4}", end="")
        if debugPrint: print()
    # debugging why some distances were off, specifically (0,2)
    # print(f"distGrid[level][0][2] (should be 5 from 0->4->1):")
    # for level in range(0, len(distGrid)):
    #     print(f"{distGrid[level][0][2]} | ", end ="")
    # print()

    print(resultGrid[xlen-1][ylen-1])


# 803 < 842 < ans < ???


print("goodbye world")
