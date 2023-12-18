import re
# https://regex101.com/r/nH4nD3/3
from collections import deque
from sys import maxsize
import copy
import heapq 

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
