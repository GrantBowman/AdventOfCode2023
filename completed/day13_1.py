import re
# https://regex101.com/r/nH4nD3/3


def solve(grid):
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
        result = solve(grid)
        sum += result * 100
        print(f"  rows? : {result}")
        # transpose to expand cols (now rows)
        # https://stackoverflow.com/questions/17037566/transpose-a-matrix-in-python
        grid = [''.join([grid[row][col] for row in range(0,len(grid))]) for col in range(0,len(grid[0]))]

        # print("transposed:")
        # for row in grid:
        #     print(row)

        # find mirrored cols (transposed to rows now)
        result = solve(grid)
        sum += result
        print(f"  cols? : {result}")


        if not line:
            break

print(sum)    
print("goodbye world")

# 34556 < ans = 35360 < ???