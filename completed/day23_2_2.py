import re
# https://regex101.com/r/nH4nD3/3
debugPrint = True
from copy import deepcopy
from collections import deque

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.vertices = {}
        self.start = None
        self.end = None
        
        # find the vertices
        self.setupVertices()
        print(f"init vertices: found")
        self.printVertices()
        print(f"len={len(self.vertices)}")

        # calculate the distance between each connected pair
        self.calculateInfo()
        print(f"init vertices: lengths")
        self.printVertices()

    def printVertices(self):
        for v in self.vertices.values():
            print(str(v))

    # get vertices
    def setupVertices(self):
        # start and end nodes
        self.start=Node((1,1))
        self.vertices[(1,1)]=self.start
        xlen = len(self.grid)
        ylen = len(self.grid[0])
        self.end=Node((xlen-2,ylen-2))
        self.vertices[(xlen-2,ylen-2)]=self.end
        # get the coords of all forks/splits/hubs. basically not a corridor
        for x in range(1,xlen-1):
            for y in range(1,ylen-1):
                if grid[x][y] == "#":
                    continue
                exitCount = 0
                if grid[x-1][y] not in ["#"]:
                    exitCount+=1
                if grid[x][y-1] not in ["#"]:
                    exitCount+=1
                if grid[x+1][y] not in ["#"]:
                    exitCount+=1
                if grid[x][y+1] not in ["#"]:
                    exitCount+=1
                # at least 'T', maybe even a '+' !
                if exitCount > 2:
                    self.vertices[(x,y)]=Node((x,y))

    # find and hold distances between vertices
    def calculateInfo(self):
        for a in self.vertices.values():
            # print(f"setting up connections for {a}")
            self.setupDistances(a)

    # tries to connect a to b, connect a to neighbors in the process
    def setupDistances(self, a):
        # find distances between
        ax, ay = a.id
        queue = deque()
        seen = []
        # x, y, d
        queue.append((ax, ay, 0))
        while queue:
            x, y, d = queue.popleft()
            # print(f"setupDistBetween: looking at {(x, y, d)}")
            if ((x,y)) in seen:
                continue
            seen.append((x,y))
            # ran into a neighbor! dont try to reach beyond.
            # but while we're here, lets connect them! how nice :3
            if (x,y) != (ax, ay) and (x,y) in self.vertices.keys():
                # print(f"setupDistBetween: connecting {(ax,ay)} to {(x,y)}")
                c = self.vertices[(x,y)]
                a.edges[c] = d
                c.edges[a] = d
                continue
            if grid[x-1][y] != "#": # and (x-1,y) not in seen:
                queue.append((x-1,y,d+1))
            if grid[x][y-1] != "#": # and (x,y-1) not in seen:
                queue.append((x,y-1,d+1))
            if grid[x+1][y] != "#": # and (x+1,y) not in seen:
                queue.append((x+1,y,d+1))
            if grid[x][y+1] != "#": # and (x,y+1) not in seen:
                queue.append((x,y+1,d+1))

    def longestPath(self, a=None, b=None):
        if a == None:
            a = self.start
        if b == None:
            b = self.end
        # key = (node, seen, inOut, d)
        stack = [(a, [], 1, 0)]
        maxDist = -1
        while stack:
            n, seen, inOut, d = stack.pop()
            # print(f"finding longest path {(n, d)}: {seen}")
            # stack weirdness
            if inOut == -1:
                seen.remove(n)
                continue
            if inOut == 1:
                stack.append((n, seen, -1, -1))

            if n in seen:
                continue
            seen.append(n)
            if n == b:
                if d > maxDist:
                    print(f"new maxDist: {d}")
                    maxDist = d
                # print(f"Found an end: {d}, max = {maxDist}")
            for e in n.edges.keys():
                if e in seen:
                    # print(f"\talready seen {e}")
                    continue
                # print(f"\tpushing {e, seen, d+n.edges[e]}")
                stack.append((e, seen, 1, d+n.edges[e]))
        return maxDist




         

          

class Node:
    def __init__(self, id):
        self.id = id
        # self.id -> id:dist
        self.edges = {}
    def __str__(self):
         return f"Node {self.id}: {self.edges}"
    def __repr__(self):
         return f"N{self.id}"


def printGridWithSeen(grid, seen):
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            if (x,y) in seen:
                print("O", end="")
            else:
                print(grid[x][y], end="")
        print()



with open("input23.txt") as input:
    # print("hello world")
    
    grid = []
    for line in input:
        grid.append(list(line.strip()))
        pass
    xlen = len(grid)
    ylen = len(grid[0])
    # close off the start and stop
    # remember to +2 to the result for that now-closed spots
    grid[0][1] = "#"
    grid[xlen-1][ylen-2] = "#"

    myGrid = Grid(grid)
    
    print(f"Time to find the longest path...")
    result = myGrid.longestPath()
    # did you remember the +2?
    result += 2
    print(result)


# wrong: 6333
# should be 6334 ????
             
         
print("goodbye world")