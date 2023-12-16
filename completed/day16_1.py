import re
# https://regex101.com/r/nH4nD3/3
from collections import deque

with open("input16.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    mirrorGrid = []
    for line in input:
        mirrorGrid.append([ x for x in line.strip()])
        pass
    for row in mirrorGrid:
        for char in row:
            print(char, end="")
        print()

    lightGrid =[[0b0000 for y in mirrorGrid[0]] for x in mirrorGrid]
    # print lightGrid, with hex per direction entering that square
    # for row in lightGrid:
    #     for isLit in row:
    #         print(hex(isLit)[2:], end="")
    #     print()

    lightQueue = deque()
    # NWSE = 0000 -> 0-F
    n = 0b1000
    w = 0b0100
    s = 0b0010
    e = 0b0001
    # append the 
    lightQueue.append((0,0,e))
    
    # progress
    while True:
        if len(lightQueue) == 0:
            break
        x, y, going = lightQueue.popleft()
        m = mirrorGrid[x][y]
        # prevent repeating
        if lightGrid[x][y] & going == 1:
            continue
        lightGrid[x][y] |= going
        # reflect
        if m == "/":
            # n->e, w->s, s->w, e->n
            if (going == n) and (y < len(mirrorGrid[x])-1):
                lightQueue.append((x, y+1, e))
            elif (going == w) and (x < len(mirrorGrid)-1):
                lightQueue.append((x+1, y, s))
            elif (going == s) and (y > 0):
                lightQueue.append((x, y-1, w))
            elif (going == e) and (x > 0):
                lightQueue.append((x-1, y, n))
        elif m == "\\":
            # n->w, w->n, s->e, e->s  
            if (going == n) and (y > 0):
                lightQueue.append((x, y-1, w))
            elif (going == w) and (x > 0):
                lightQueue.append((x-1, y, n))
            elif (going == s) and (y < len(mirrorGrid[x])-1):
                lightQueue.append((x, y+1, e))
            elif (going == e) and (x < len(mirrorGrid)-1):
                lightQueue.append((x+1, y, s))
        # split W/E
        elif m == "|":
            if going & (e|w):
                if x > 0:
                    lightQueue.append((x-1, y, n))
                if x < len(mirrorGrid)-1:
                    lightQueue.append((x+1, y, s))
            if going & n:
                if x > 0:
                    lightQueue.append((x-1, y, n))
            if going & s:
                if x < len(mirrorGrid)-1:
                    lightQueue.append((x+1, y, s))
        # split W/E
        elif m == "-":
            if going & (n|s):
                if y > 0:
                    lightQueue.append((x, y-1, w))
                if y < len(mirrorGrid[x])-1:
                    lightQueue.append((x, y+1, e))
            if going & w:
                if y > 0:
                    lightQueue.append((x, y-1, w))
            if going & e:
                if y < len(mirrorGrid[x])-1:
                    lightQueue.append((x, y+1, e))
        elif m == ".":
            if (going == n) and (x > 0):
                lightQueue.append((x-1, y, n))
            elif (going == w) and (y > 0):
                lightQueue.append((x, y-1, w))
            elif (going == s) and (x < len(mirrorGrid)-1):
                lightQueue.append((x+1, y, s))
            elif (going == e) and (y < len(mirrorGrid[x])-1):
                lightQueue.append((x, y+1, e))


    # print lightGrid, with hex per direction entering that square
    for row in lightGrid:
        for isLit in row:
            print(hex(isLit)[2:], end="")
        print()
    # sum up the answer
        sum = 0
    for row in lightGrid:
        for isLit in row:
            if isLit:
                sum += 1
        


print(sum)    
print("goodbye world")