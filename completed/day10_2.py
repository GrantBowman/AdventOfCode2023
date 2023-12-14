import re
# https://regex101.com/r/nH4nD3/3
from collections import deque

with open("input10.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

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
    # ((toX, toY), (fromX, fromY), rotation)
    # count rotation anticlockwise (positive maths rotation)
    rotation = 0
    firstStep = None
    posQueue = deque()
    # ^
    if (startPos[0] > 0) and (maze[startPos[0]-1][startPos[1]] in hasSouth):
        posQueue.append(((startPos[0]-1, startPos[1]), startPos, rotation))
        firstStep = "north"
    # <
    elif (startPos[1] > 0) and (maze[startPos[0]][startPos[1]-1] in hasEast):
        posQueue.append(((startPos[0], startPos[1]-1), startPos, rotation))
        firstStep = "west"
    # v
    elif (startPos[0] < len(maze)-1) and (maze[startPos[0]+1][startPos[1]] in hasNorth):
        posQueue.append(((startPos[0]+1, startPos[1]), startPos, rotation))
        firstStep = "south"
    # >
    elif (startPos[1] < len(maze[startPos[0]])-1) and (maze[startPos[0]][startPos[1]+1] in hasWest):
        posQueue.append(((startPos[0], startPos[1]+1), startPos, rotation))
        firstStep = "east"
    for pos in posQueue:
        if debugPrint: print(f"startpos: {pos}")
    # BFS and increment distance in mazeDistance
    maxDistance = -1
    while True:
        if len(posQueue) == 0:
            break
        curPos, fromPos, rotation = posQueue.popleft()
        # check if already visited
        if mazeDistance[curPos[0]][curPos[1]] != -1:
            continue
        # increment step counter
        thisDistance = mazeDistance[fromPos[0]][fromPos[1]]
        mazeDistance[curPos[0]][curPos[1]] = thisDistance+1
        maxDistance = max(maxDistance, thisDistance+1)
        # check where to go next
        # ^
        if (curPos[0] > 0) and (maze[curPos[0]][curPos[1]] in hasNorth) and (maze[curPos[0]-1][curPos[1]] in hasSouth) and ((curPos[0]-1, curPos[1]) != fromPos):
            # if next == "7", rotation += 1
            if maze[curPos[0]-1][curPos[1]] == "7":
                rotation += 1
            # if next == "F", rotation -= 1
            if maze[curPos[0]-1][curPos[1]] == "F":
                rotation -= 1
            posQueue.append(((curPos[0]-1, curPos[1]), curPos, rotation))
        # <
        if (curPos[1] > 0) and (maze[curPos[0]][curPos[1]] in hasWest) and (maze[curPos[0]][curPos[1]-1] in hasEast) and ((curPos[0], curPos[1]-1) != fromPos):
            # if next == "F", rotation += 1
            if maze[curPos[0]][curPos[1]-1] == "F":
                rotation += 1
            # if next == "L", rotation -= 1
            if maze[curPos[0]][curPos[1]-1] == "L":
                rotation -= 1
            posQueue.append(((curPos[0], curPos[1]-1), curPos, rotation))
        # v
        if (curPos[0] < len(maze)-1) and (maze[curPos[0]][curPos[1]] in hasSouth) and (maze[curPos[0]+1][curPos[1]] in hasNorth) and ((curPos[0]+1, curPos[1]) != fromPos):
            # if next == "L", rotation += 1
            if maze[curPos[0]+1][curPos[1]] == "L":
                rotation += 1
            # if next == "J", rotation -= 1
            if maze[curPos[0]+1][curPos[1]] == "J":
                rotation -= 1
            posQueue.append(((curPos[0]+1, curPos[1]), curPos, rotation))
        # >
        if (curPos[1] < len(maze[curPos[0]])-1) and (maze[curPos[0]][curPos[1]] in hasEast) and (maze[curPos[0]][curPos[1]+1] in hasWest) and ((curPos[0], curPos[1]+1) != fromPos):
            # if next == "J", rotation += 1
            if maze[curPos[0]][curPos[1]+1] == "J":
                rotation += 1
            # if next == "7", rotation -= 1
            if maze[curPos[0]][curPos[1]+1] == "7":
                rotation -= 1
            posQueue.append(((curPos[0], curPos[1]+1), curPos, rotation))
    if debugPrint: print(f"maze=")
    for line in maze:
        if debugPrint: print(line)
    if debugPrint: print(f"mazeDistance=")
    for line in mazeDistance:
        if debugPrint: print(line)
    
    # fix 'S' for expansion later. just need to look right and down                
    # v
    if (startPos[0] < len(maze)-1) and (maze[startPos[0]+1][startPos[1]] in hasNorth):
        maze[startPos[0]][startPos[1]] = '-'
    # >
    if (startPos[1] < len(maze[startPos[0]])-1) and (maze[startPos[0]][startPos[1]+1] in hasWest):
        if maze[startPos[0]][startPos[1]] == '-':
            maze[startPos[0]][startPos[1]] = "F"
        else:
            maze[startPos[0]][startPos[1]] = "|"
    # created the expanded grid to flood interior
    floodMazeRow = [0 for x in range(0,2*len(maze[0])+1)]
    floodMaze = [floodMazeRow.copy() for x in range(0,2*len(maze)+1)]
    for x in range(0,len(maze)):
        for y in range(0,len(maze[x])):
            if mazeDistance[x][y] >= 0:
                floodMaze[2*x+1][2*y+1] = -1
                # expand blocking to the right or below as needed
                if maze[x][y] in "|7F":
                    floodMaze[2*x+2][2*y+1] = -1
                if maze[x][y] in "-LF":
                    floodMaze[2*x+1][2*y+2] = -1

    # now flood, starting from startPos based on rotation
    floodQueue = deque()
    rotation = 1 if rotation > 0 else -1
    if debugPrint: print(f"firstStep: '{firstStep}'")
    if firstStep == "north":
        floodQueue.append((2*startPos[0]+1-1, 2*startPos[1]+1-rotation))
    if firstStep == "west":
        floodQueue.append((2*startPos[0]+1+rotation, 2*startPos[1]+1-1))
    if firstStep == "south":
        floodQueue.append((2*startPos[0]+1+1, 2*startPos[1]+1+rotation))
    if firstStep == "east":
        floodQueue.append((2*startPos[0]+1-rotation, 2*startPos[1]+1+1))

    if debugPrint: print(f"floodQueue beginnings:")
    for item in floodQueue:
        if debugPrint: print(f"{item}")
    # flood
    while True:
        if len(floodQueue) == 0:
            break
        x, y = floodQueue.popleft()
        if debugPrint: print(f"flooding ({x}, {y})")
        floodMaze[x][y] = 1
        if (x > 0) and (floodMaze[x-1][y] == 0):
            floodMaze[x-1][y] = 1
            floodQueue.append((x-1, y))
        if (x < len(floodMaze)-1) and (floodMaze[x+1][y] == 0):
            floodMaze[x+1][y] = 1
            floodQueue.append((x+1, y))
        if (y > 0) and (floodMaze[x][y-1] == 0):
            floodMaze[x][y-1] = 1
            floodQueue.append((x, y-1))
        if (y < len(floodMaze[x])-1) and (floodMaze[x][y+1] == 0):
            floodMaze[x][y+1] = 1
            floodQueue.append((x, y+1))

    # calculate filled
    for x in range(0,len(floodMaze)-1, 2):
        for y in range(0,len(floodMaze[x])-1, 2):
            if floodMaze[x+1][y+1] == 1:
                sum += 1


    # display cuz pretty
    if debugPrint: print(f"expanded flood maze:")
    for line in floodMaze:
        for inLoop in line:
            if inLoop == -1:
                if debugPrint: print('#', end="")
            if inLoop == 0:
                if debugPrint: print(' ', end="")
            if inLoop == 1:
                if debugPrint: print('.', end="")
        if debugPrint: print()



# ans < 1001
# < 500
# 256 <
# 256 < ans < 500
# 384 ..? 5 minute delay
# 384 ..? 5 minute delay (it knows)

# the loop cuts the grid in 2 pieces, and 

# could instead expand on the given maze...
# expand pipes alone right and below, with a . bottom right
# turning:
'''
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
'''
# info
'''
....F-7...
....|.|...
..F-J.|...
..|...|...
SoJ...L-7.
o.......|.
|.F-----J.
|.|.......
L-J.......
..........
'''
# ^ honestly could just be formed from mazeDistance checking for -1 or not for in path or not
# then use starting pos, rotation, and firstStep to determine where to flood from
# loop through every other flooded pos (eg. 0, 2, 4, ...) and see if was flooded and += 1 to sum

# then the only ones to count have -1 distance in the original, at indice (x/2, y/2) when only checking even x,y
# rotation > 0 means went around positive, so 

# ...
# .S.
# ...

# padding before the first row and column? that way just move clockwise/anticlockwise a step depending on rotation?
# then check grid pos starting at 1, 3, 5, ...which become (x-1)/2 in the original

print(f"rotation={rotation}")
print(sum)
print("goodbye world")
