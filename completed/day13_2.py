import re
# https://regex101.com/r/nH4nD3/3

def smudgeDistance(r1, r2):
    result = 0
    for i in range(0, len(r1)):
        if r1[i] != r2[i]:
            result += 1
    return result

def newReflectLine(grid, oldLine):
    # check rows
    # need to be within the grid, not along the edge
    for i in range(0, len(grid)-1):
        # ignore the old line
        if i+1 == oldLine:
            continue
        j = 0
        validMirror = True
        smudges = 0
        while (i-j >= 0) and (i+j+1 < len(grid)):
            smudges += smudgeDistance(grid[i-j], grid[i+j+1])
            if smudges > 1:
                # print(f"checking {i} failed at {i-j} vs {i+j+1}:")
                # print(f"{i-j}: {grid[i-j]}")
                # print(f"{i+j+1}: {grid[i+j+1]}")
                validMirror = False
                break
            j += 1
        if validMirror:
            return i+1
    return 0

def oldReflectionLine(grid):
    # check rows
    # need to be within the grid, not along the edge
    for i in range(0, len(grid)-1):
        j = 0
        validMirror = True
        while (i-j >= 0) and (i+j+1 < len(grid)):
            if grid[i-j] != grid[i+j+1]:
                # print(f"checking {i} failed at {i-j} vs {i+j+1}:")
                # print(f"{i-j}: {grid[i-j]}")
                # print(f"{i+j+1}: {grid[i+j+1]}")
                validMirror = False
                break
            j += 1
        if validMirror:
            return i+1
    return 0



with open("input13.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    id = 0
    grid = []
    while True:
        id += 1
        grid = []
        while True:
            line = input.readline()
            # line = line.strip()
            if line.strip() == "":
                break
            grid.append(line.strip())
        # print("\nwowee new grid!:")
        # for row in grid:
        #     print(row)

        print(f"\tsolving grid {id}:")

        result = 0
        # find mirrored rows (rows = *100)
        oldLine = oldReflectionLine(grid)
        result = newReflectLine(grid, oldLine)
        sum += result * 100
        print(f"  rows? : {result} instead of {oldLine}")
        # transpose to expand cols (now rows)
        # https://stackoverflow.com/questions/17037566/transpose-a-matrix-in-python
        grid = [''.join([grid[row][col] for row in range(0,len(grid))]) for col in range(0,len(grid[0]))]

        # print("transposed:")
        # for row in grid:
        #     print(row)

        # find mirrored cols (transposed to rows now)
        oldLine = oldReflectionLine(grid)
        result = newReflectLine(grid, oldLine)
        sum += result
        print(f"  cols? : {result} instead of {oldLine}")


        if not line:
            break

print(sum)    
print("goodbye world")

# ??? < ans = 36755 < 40109