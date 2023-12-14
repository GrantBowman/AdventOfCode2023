import re
# https://regex101.com/r/nH4nD3/3

def expand(space, distances):
    # expand rows
    # stretchFactor = 100
    stretchFactor = 1000000
    x = 0
    while x < len(space):
        if re.match(r"^\.+$", space[x]):
            distances[x] = [stretchFactor for a in distances[x]]
        x += 1
    # object is maniputlated
    

with open("input11.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True
    space = []
    distances = []

    i = 0
    for line in input:
        i += 1
        line = line.strip()
        space.append(line)
        distances.append([1 for x in line])
        pass
    # expand the spaces
    expand(space, distances)
    # transpose to expand cols (now rows)
    # https://stackoverflow.com/questions/17037566/transpose-a-matrix-in-python
    space = [''.join([space[row][col] for row in range(0,len(space))]) for col in range(0,len(space[0]))]
    distances = [[distances[row][col] for row in range(0,len(distances))] for col in range(0,len(distances[0]))]
    expand(space, distances)

    for row in space:
        if debugPrint: print(row)
    for row in distances:
        if debugPrint: print(row)

    # go through and get a list of all galaxy '#' positions
    galaxies = []
    for x in range(0,len(space)):
        for y in range(0,len(space[x])):
            if space[x][y] == '#':
                galaxies.append((x, y))
    
    # loop through and get min
    # only count pairs once
    pairCount = 0
    for i in range(0,len(galaxies)):
        for j in range(i+1,len(galaxies)):
            pairCount += 1
            dist = 0
            x1 = galaxies[i][0]
            y1 = galaxies[i][1]
            x2 = galaxies[j][0]
            y2 = galaxies[j][1]
            dirx = 1 if (x2-x1>0) else -1
            diry = 1 if (y2-y1>0) else -1
            x = x1
            y = y1
            while x != x2:
                dist += distances[x][y]
                x += dirx
            while y != y2:
                dist += distances[x][y]
                y += diry
            # if debugPrint: print(f"pair {galaxies[i]} and {galaxies[j]} x={x}, y={y}, dist={dist}")
            sum += dist
    print(f"pairCount={pairCount}")
    print(f"sum={sum}")
print("goodbye world")

# 16429218 < ans < ??