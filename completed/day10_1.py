import re
# https://regex101.com/r/nH4nD3/3
from collections import deque

with open("input10.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    maze = []
    mazeDistance = []
    i = 0
    for line in input:
        line = line.strip()
        maze.append(list(line))
        mazeDistance.append([-1 for x in range(0,len(line))])
        pass
    for line in maze:
        if debugPrint: print(line)

    # find starting position
    startPos = (-1, -1)
    for x in range(0,len(maze)):
        for y in range(0,len(maze[x])):
            if maze[x][y] == "S":
                startPos = (x, y)
                mazeDistance[startPos[0]][startPos[1]] = 0
                break
    if debugPrint: print(f"startPos = {startPos}")

    # find the first valid spots
    # valid pipe options = "|-LJ7F"
    hasNorth = "|LJ"
    hasEast  = "-LF"
    hasSouth = "|7F"
    hasWest  = "-J7"
    # posQueue element form:
    # ((toX, toY), (fromX, fromY))
    posQueue = deque()
    # ^
    if (startPos[0] > 0) and (maze[startPos[0]-1][startPos[1]] in hasSouth):
        posQueue.append(((startPos[0]-1, startPos[1]), startPos))
    # v
    if (startPos[0] < len(maze)-1) and (maze[startPos[0]+1][startPos[1]] in hasNorth):
        posQueue.append(((startPos[0]+1, startPos[1]), startPos))
    # <
    if (startPos[1] > 0) and (maze[startPos[0]][startPos[1]-1] in hasEast):
        posQueue.append(((startPos[0], startPos[1]-1), startPos))
    # >
    if (startPos[1] < len(maze[startPos[0]])-1) and (maze[startPos[0]][startPos[1]+1] in hasWest):
        posQueue.append(((startPos[0], startPos[1]+1), startPos))
    for pos in posQueue:
        if debugPrint: print(f"startpos: {pos}")
    # BFS and increment distance in mazeDistance
    maxDistance = -1
    while True:
        if len(posQueue) == 0:
            break
        curPos, fromPos = posQueue.popleft()
        if debugPrint: print(f"curPos: {curPos}, fromPos: {fromPos}, '{maze[curPos[0]][curPos[1]]}' with {mazeDistance[curPos[0]][curPos[1]]}")
        # check if already visited
        if mazeDistance[curPos[0]][curPos[1]] != -1:
            continue
        # increment step counter
        thisDistance = mazeDistance[fromPos[0]][fromPos[1]]
        mazeDistance[curPos[0]][curPos[1]] = thisDistance+1
        maxDistance = max(maxDistance, thisDistance+1)
        # check where to go next
        # ^
        if (curPos[0] > 0) and (maze[curPos[0]-1][curPos[1]] in hasSouth):
            posQueue.append(((curPos[0]-1, curPos[1]), curPos))
            if debugPrint: print(f"append ^")
        # v
        if (curPos[0] < len(maze)-1) and (maze[curPos[0]+1][curPos[1]] in hasNorth):
            posQueue.append(((curPos[0]+1, curPos[1]), curPos))
            if debugPrint: print(f"append v")
        # <
        if (curPos[1] > 0) and (maze[curPos[0]][curPos[1]-1] in hasEast):
            posQueue.append(((curPos[0], curPos[1]-1), curPos))
            if debugPrint: print(f"append <")
        # >
        if (curPos[1] < len(maze[curPos[0]])-1) and (maze[curPos[0]][curPos[1]+1] in hasWest):
            posQueue.append(((curPos[0], curPos[1]+1), curPos))
            if debugPrint: print(f"append >")
    if debugPrint: print(f"maze=")
    for line in maze:
        if debugPrint: print(line)
    if debugPrint: print(f"mazeDistance=")
    for line in mazeDistance:
        if debugPrint: print(line)


print(maxDistance)
print("goodbye world")