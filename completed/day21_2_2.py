import re
# https://regex101.com/r/nH4nD3/3
from copy import deepcopy

# global variables because this is a mess
debugPrint = True
maxSteps = 16
parity = maxSteps%2

def getSpotSum(stepGrid):
    result = 0
    for x in range(0,len(stepGrid)):
        for y in range(0,len(stepGrid[x])):
            for (xx, yy), c in stepGrid[x][y].items():
                result += 1
    return result

# from a start and stop point, walk these many steps and return sum of possible locations 
def walkGrid(grid, sx, sy, maxSteps, debugPrint=False):
    stepGrid = [[-1 for y in row] for row in grid]
    stepGrid[sx][sy] = 0

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
    # sum it up
    result = 0
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            if stepGrid[x][y] == maxSteps:
                result += 1
    if debugPrint:
        print(f"start = ({sx},{sy}), {maxSteps} result = {result}")
        for x in range(0,len(grid)):
            for y in range(0,len(grid[x])):
                if x==sx and y==sy:
                    print("S",end="")
                elif stepGrid[x][y] == maxSteps:
                    print("O",end="")
                else:
                    print(f"{grid[x][y]}",end="")
            print()
    return result
                        


with open("input21_demo.txt") as input:
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


    # new idea: maths!
    # find the number of middle, completely filled grid based
    # the step count and the fact the base grid has a window-outline unobstructed path
    # and find out the boundary from there based on entering the new grid from either the corner or mid-edge
    # N, W, S, E, NW, SW, SE, NE
    # from the corner, takes at max xlen+ylen steps to fill the grid
    #  ^ not neccessarily true if a spiral pattern, oof
    # the given input is pretty sparse tho
    # if seen n whole grids from center, the total full-seen grids are (4*n*(n+1)/2) + 1 = 2n*(n+1) + 1
    # also note S starts in the center, 

    midToCorner = xlen//2 + ylen//2
    # move into corner + -> opposite corner
    fillFromOutCorner = xlen + ylen
    # gridLength is the number of full grids seen along the axis.
    # since the grids are square, they should be equal
    xGridLength = (maxSteps-xlen//2) // xlen
    yGridLength = (maxSteps-ylen//2) // ylen

    # takes 1 move to move adjacent to next corner grid's corner, thus fillFromOutCorner + 1
    # 1|2
    # -+-
    # x|1
    # need to know how far we go outward for partially full grids later
    # eg. [full grids] + a bit, save that bit for later
    fullGridSeenDiagonal = (maxSteps-midToCorner) // (fillFromOutCorner+1)

    if debugPrint: print(f"xlen is {xlen}")
    if debugPrint: print(f"ylen is {ylen}")
    if debugPrint: print(f"midToCorner is {midToCorner}")
    if debugPrint: print(f"fillFromOutCorner is {fillFromOutCorner}")
    if debugPrint: print(f"start is ({sx}, {sy})")

    # parity swaps betwwen grids, eg on even vs odd spaces:
    # +-+-      3
    # -+-+      2 3
    # +-+-      1 + -
    # -+-+      n - + -
    # get sum for ecah full grid parity
    # so multiply total grid sum by full grids seen
    fullOddGridSum = 0
    fullEvenGridSum = 0
    # get those 
    for x in range(0,xlen):
        for y in range(0,ylen):
            if (x+y) % 2 == 0:
                if grid[x][y] != "#":
                    fullEvenGridSum += 1
            elif (x+y) % 2 == 1:
                if grid[x][y] != "#":
                    fullOddGridSum += 1

    if debugPrint: print(f"fullEvenGridSum = {fullEvenGridSum}")
    if debugPrint: print(f"fullOddGridSum = {fullOddGridSum}")
    if debugPrint: print(f"maxSteps = {maxSteps}")
    if debugPrint: print(f"xGridLength = {xGridLength}")
    if debugPrint: print(f"yGridLength = {yGridLength}")
    if debugPrint: print(f"fullGridSeenDiagonal = {fullGridSeenDiagonal}")
    if debugPrint: print(f"furthest up: {xlen//2}+{xGridLength*xlen}+{maxSteps-xlen//2-xGridLength*xlen} ?= {maxSteps}")
    if debugPrint: print(f"furthest right: {ylen//2}+{yGridLength*ylen}+{maxSteps-ylen//2-yGridLength*ylen} ?= {maxSteps}")

    # corner coord ;   *= full grid lengths |
    #  exit start v                         v
    cornerx = xlen//2 + fullGridSeenDiagonal*xlen
    # coord in the corner grid, eg. half of leftover bits
    cornerxInside = (maxSteps//2 - cornerx)
    cornerx += cornerxInside
    # repeat for x corner coord (cornery) and spot in partial grid (corneryInside)
    cornery = ylen//2 + fullGridSeenDiagonal*ylen
    corneryInside = (maxSteps//2-cornery)
    cornery += corneryInside

    if debugPrint: print(f"furthest corner: {cornerx}+{cornery} ?<= {maxSteps}")
    if debugPrint: print(f"coord in cornerGrid: ({cornerxInside}, {corneryInside})")

    # calc sum of the grids that are full:
    # -
    # + - ..
    # - + - ..
    # n - + - ..
    # by adding the 4 triangles of full grids calculated by the axis extentions and the triangle of grids to their right (*=4) + middle
    i = xGridLength # = yGridLength
    # parity swaps as we move sideways; track that for summing
    jparity = 0
    fullGridsSum = 0
    while i > 0:
        stretchSum = 0
        # if n is even (+) parity
        # n-+-+-
        stretchSum += (fullOddGridSum+fullEvenGridSum)*(i//2)
        # the furthest away, if odd grid away, is opposite the middle's parity
        if i%2 == 1 and (parity+jparity)%2==0:
            stretchSum += fullOddGridSum
        if i%2 == 1 and (parity+jparity)%2==1:
            stretchSum += fullEvenGridSum
        
        fullGridsSum += 4*stretchSum
        i -= 1
        jparity +=1
    # add middle's sum based on even/odd parity
    if parity==1:
        fullGridsSum += fullOddGridSum
    if parity==0:
        fullGridsSum += fullEvenGridSum
    print(f"fullGridsSum = {fullGridsSum}")


    # next, to count the partial grids
    # will either enter from an edge or a corner,
    # BUT the parity of that grid could be odd OR even! so need to track both per entrypoint
    # then just call how many steps into that grid, *= how many of those partial grids
    #         n
    #       F - 7
    #     F - + - 7
    #   F - + - + - 7
    # w - + - x - + - e
    #   L - + - + - J
    #     L - + - J
    #       L - J
    #         s
    # always 1 each of n,w,s,e entrypoints
    # the numbers of NW=F, SW=L, SE=J, NE=7 varies by diamond size
    # but is always = xGridLength = yGridLength (visualize sliding the axis to each's right)
    # xGridLength * (NE[]) 
    # careful of that parity step, which is truncated. steps in these grids is = cornerxInside+corneryInside+parity-1
    # -1 at the end because of the step to get into the grid

    # the cardinal points represent location in the big diamond; the actual entrypoint is opposite
    cornerSteps = cornerxInside + corneryInside + parity - 1
    print(f"cornerSteps = {cornerSteps}")
    nwSteps = walkGrid(grid, xlen-1, ylen-1, cornerSteps)
    swSteps = walkGrid(grid, 0, ylen-1, cornerSteps)
    seSteps = walkGrid(grid, 0, 0, cornerSteps)
    neSteps = walkGrid(grid, xlen-1, 0, cornerSteps)
    print(f"{cornerSteps} corner fills nw={nwSteps}, sw={swSteps}, se={seSteps}, ne={neSteps}")
    # and the edges
    edgeSteps = maxSteps - (xGridLength*xlen)
    print(f"edgeSteps = {edgeSteps}")
    nSteps = walkGrid(grid, xlen-1, sy, edgeSteps)
    wSteps = walkGrid(grid, sx, ylen-1, edgeSteps)
    sSteps = walkGrid(grid, 0, sy, edgeSteps)
    eSteps = walkGrid(grid, sx, 0, edgeSteps)
    print(f"{edgeSteps} edge steps n={nSteps}, w={wSteps}, s={sSteps}, e={eSteps}")

    partialGridsSum = 0
    print(f"xGridLength = {xGridLength}")
    partialGridsSum += xGridLength * (nwSteps + swSteps + seSteps + neSteps)
    partialGridsSum += nSteps + wSteps + sSteps + eSteps
    print(f"partialGridsSum = {partialGridsSum}")

    finalAnswer =  fullGridsSum + partialGridsSum
    print(finalAnswer)

# 470,149,872,588,260 < ans < ???

print("goodbye world")