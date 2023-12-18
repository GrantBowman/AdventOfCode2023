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

def updateDijkstra(toVisitHeap, distGrid, visitGrid, grid, x, y, level, fromDist):
    # add to visited if not in
    if visitGrid[level][x][y] == 0:
        visitGrid[level][x][y] = 1
        dist = curDist + grid[x][y]
        distGrid[level][x][y] = dist
        heapq.heappush(toVisitHeap, (dist, x, y, level))
    # else update its value
    elif visitGrid[level][x][y] == 1:
        dist = min(distGrid[level][x][y], curDist + grid[x][y])
        distGrid[level][x][y] = dist
        # update every level in the grid
        for item in getInHeap(toVisitHeap, x, y, level):
            # 
            newDist = min(dist,item[0])
            heapq.heapreplace(toVisitHeap, (item[0], x, y, level))
    # put it back in if the path could be shorter
    # elif visitGrid[level][x][y] == 2:
    #     dist = curDist + grid[x][y]
    #     if dist < distGrid[level][x][y]:
    #         distGrid[level][x][y] = dist
    #         visitGrid[level][x][y] = 1
    #         heapq.heappush(toVisitHeap, (dist, x, y, level))

with open("input17.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    stepLimit = 3
    grid = []
    # the (0, 0) is only used for the beginning. perhaps just start with all (0,0) in n1, w1, s1, e1?
    # 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11
    # n1, n2, n3, w1, w2, w3, s1, s2, s3, e1, e2, e3
    for line in input:
        line = line.strip()
        grid.append([int(x) for x in line])


    # heatLoss, row, col, dr, dc, steps
    pq = [(0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0)]
    seen = set()

    while pq:
        node = heapq.heappop(pq)
        heatLoss, row, col, dr, dc, steps = node
        # print(node)
        # bounds check
        # if not (0<row<len(grid)-1 or 0<col<len(grid[0])-1):
        if row<0 or row>len(grid)-1 or col<0 or col>len(grid[0])-1:
            continue

        # seen check and add
        if (row, col, dr, dc, steps) in seen:
            continue
        seen.add((row, col, dr, dc, steps))

        # found end
        if row==len(grid)-1 and col==len(grid[0])-1 and steps>=4:
            print(f"found end: {heatLoss}")
            break

        # same dir
        if steps <10 and (dr, dc) != (0, 0):
            # print("going straight")
            if row+dr<0 or row+dr>len(grid)-1 or col+dc<0 or col+dc>len(grid[0])-1:
                pass
            else:
                heapq.heappush(pq, (heatLoss+grid[row+dr][col+dc], row+dr, col+dc, dr, dc, steps+1))

        # turn
        if steps>3 and steps<=10:
            # print("turning")
            for nd in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ndr, ndc = nd
                # check not going forward like first check or going backwards cuz common sense
                if (dr==ndr and dc==ndc) or (dr==-ndr and dc==-ndc):
                    # print(f"oof ({dr},{dc}), ({dr},{dc})")
                    continue
                if row+ndr<0 or row+ndr>len(grid)-1 or col+ndc<0 or col+ndc>len(grid[0])-1:
                    continue
                heapq.heappush(pq, (heatLoss+grid[row+ndr][col+ndc], row+ndr, col+ndc, ndr, ndc, 1))

    
# 981 < ans=982 < ???


print("goodbye world")
