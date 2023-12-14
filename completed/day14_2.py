import re
# https://regex101.com/r/nH4nD3/3

def tiltNorth(grid):
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            # found a rock
            if grid[x][y] == "O":
                a = x
                while a > 0 and grid[a-1][y] == ".":
                    # bubble sort it cuz why not
                    temp = grid[a][y]
                    grid[a][y] = grid[a-1][y]
                    grid[a-1][y] = temp
                    a -= 1        
    return grid

def tiltWest(grid):
    for y in range(0,len(grid[0])):
        for x in range(0,len(grid)):
            # found a rock
            if grid[x][y] == "O":
                a = y
                while a > 0 and grid[x][a-1] == ".":
                    # bubble sort it cuz why not
                    temp = grid[x][a]
                    grid[x][a] = grid[x][a-1]
                    grid[x][a-1] = temp
                    a -= 1
    return grid

def tiltSouth(grid):
    xlen = len(grid)
    for x in range(0,len(grid)):
        xi = xlen - x - 1
        for y in range(0,len(grid[xi])):
            # found a rock
            if grid[xi][y] == "O":
                a = xi
                while a < xlen-1 and grid[a+1][y] == ".":
                    # bubble sort it cuz why not
                    temp = grid[a+1][y]
                    grid[a+1][y] = grid[a][y]
                    grid[a][y] = temp
                    a += 1        
    return grid

def tiltEast(grid):
    ylen = len(grid[0])
    for y in range(0,len(grid[0])):
        yi = ylen - y - 1
        for x in range(0,len(grid)):
            # found a rock
            if grid[x][yi] == "O":
                a = yi
                while a < ylen-1 and grid[x][a+1] == ".":
                    # bubble sort it cuz why not
                    temp = grid[x][a+1]
                    grid[x][a+1] = grid[x][a]
                    grid[x][a] = temp
                    a += 1        
    return grid


def score(grid):
    weight = len(grid)
    result = 0
    for i in range(0,len(grid)):
        rowWeight = 0
        for char in grid[i]:
            if char == "O":
                rowWeight += weight-i
        result += rowWeight
    return result

def cycle(grid):
    grid = tiltNorth(grid)
    grid = tiltWest(grid)
    grid = tiltSouth(grid)
    grid = tiltEast(grid)
    return grid

def solve(grid, n=1000000000):
    i = 0
    seen = {}
    seen[tuple(tuple(x) for x in grid)] = i
    while i < n:
        grid = cycle(grid)
        print(f"i={i}, score={score(grid)}")
        if tuple(tuple(x) for x in grid) in seen:
            print(f"iter {i} seen before at iter {seen[tuple(tuple(x) for x in grid)]}")
            break
        seen[tuple(tuple(x) for x in grid)] = i
        i += 1
    # since it is cyclic, find the index of the cycle
    start = seen[tuple(tuple(x) for x in grid)]
    print(f"start={start}")
    cycleLength = i - seen[tuple(tuple(x) for x in grid)]
    print(f"cycleLength={cycleLength}")
    destinationIndex = ((n-start) % cycleLength) + start + 1
    print(f"destinationIndex={destinationIndex}")
    destinationGrid = [g for g in seen if seen[g] == destinationIndex]
    # print(destinationGrid)

    return score(destinationGrid[0])

with open("input14.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    grid = []
    for line in input:
        grid.append([x for x in line.strip()])

    print(solve(grid, 10000))

print("goodbye world")