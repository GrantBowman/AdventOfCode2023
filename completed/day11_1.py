import re
# https://regex101.com/r/nH4nD3/3

def expand(space):
    # expand rows
    x = 0
    while x < len(space):
        if re.match(r"^\.+$", space[x]):
            space.insert(x, space[x])
            x += 1
        x += 1
    # object is maniputlated
    

with open("input11.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False
    space = []

    i = 0
    for line in input:
        i += 1
        line = line.strip()
        space.append(line)
        pass
    # expand the spaces
    expand(space)
    # transpose to expand cols (now rows)
    # https://stackoverflow.com/questions/17037566/transpose-a-matrix-in-python
    space = [''.join([space[row][col] for row in range(0,len(space))]) for col in range(0,len(space[0]))]
    expand(space)

    for row in space:
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
            sum += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
    print(f"pairCount={pairCount}")
    print(f"sum={sum}")
print("goodbye world")
