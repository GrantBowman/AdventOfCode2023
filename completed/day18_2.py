import re
# https://regex101.com/r/nH4nD3/3
from collections import deque

with open("input18.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    points = []
    instructions = []
    i = 0
    for line in input:
        line = line.strip()
        found = re.match(r"(\w) (\d+) \(#(.+)(\d)\)", line)
        _, _, dist, dir = found.groups()
        instructions.append((int(dir), int(dist,16)))

    x = 0
    y = 0
    perim = 0
    # 0r, 1d, 2l, 3u
    for inst in instructions:
        # 0 = Right
        if inst[0] == 0:
            y += inst[1]
        # 1 = Down
        if inst[0] == 1:
            x += inst[1]
        # 2 = Left
        if inst[0] == 2:
            y -= inst[1]
        # 3 = Up
        if inst[0] == 3:
            x -= inst[1]
        perim += abs(inst[1])
        points.append((x, y))

    if debugPrint:
        for pt in points:
            print(pt)
    A = 0
    # of course its gauss... shoelace algorithm
    for i in range(0,len(points)):
        A += points[i][0] * points[(i + 1) % len(points)][1] - points[i][1] * points[(i + 1) % len(points)][0]
    A //= 2
    A = abs(A)
    # perimeter is weird, and off by 1 (in the print)
    perim //= 2
    print(A)
    print(perim)
    print(A+perim+1)

# 952404941483 < 1904809882966 < ans < ???

print("goodbye world")