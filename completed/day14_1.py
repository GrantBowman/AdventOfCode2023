import re
# https://regex101.com/r/nH4nD3/3

def tilt(grid):
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

def solve(grid):
    grid = tilt(grid)
    return score(grid)

with open("input14.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    grid = []
    for line in input:
        grid.append([x for x in line.strip()])

    print(solve(grid))

print("goodbye world")