import re
# https://regex101.com/r/nH4nD3/3

with open("input21.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    grid = []
    
    for line in input:
        grid.append(list(line.strip()))
        pass
    # make the step grid
    stepGrid = [[-1 for y in row] for row in grid]
    # find start spot
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            if grid[x][y] == "S":
                sx, sy = x, y
    stepGrid[sx][sy] = 0
    # print(sx, sy)
    # for row in grid:
    #     print(row)
    # print()
    # for row in stepGrid:
    #     print(row)


    maxSteps = 64
    # run iters
    for i in range(0,maxSteps):
        for x in range(0,len(grid)):
            for y in range(0,len(grid[x])):
                if stepGrid[x][y] == i:
                    # n
                    if x > 0 and grid[x-1][y] != "#":
                        stepGrid[x-1][y] = i+1
                    # w
                    if y > 0 and grid[x][y-1] != "#":
                        stepGrid[x][y-1] = i+1
                    # s
                    if x < len(grid)-1 and grid[x+1][y] != "#":
                        stepGrid[x+1][y] = i+1
                    # e
                    if y < len(grid[x])-1 and grid[x][y+1] != "#":
                        stepGrid[x][y+1] = i+1
        # print(f"iter {i}:")
        # for row in stepGrid:
        #     print(row)
            
    result = 0
    for x in range(0,len(stepGrid)):
        for y in range(0,len(stepGrid[x])):
            if stepGrid[x][y] == maxSteps:
                result += 1
    print(f"result = {result}")

print("goodbye world")