import re
# https://regex101.com/r/nH4nD3/3
import itertools

debugPrint = True


class BrickStack:
    def __init__(self, sx, sy, sz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.bricks = {}
        self.stack = [[[-1 for z in range(sz)] for y in range(sy)] for x in range(sx)]
        assert len(self.stack)==sx and len(self.stack[0])==sy and len(self.stack[0][0])==sz

    def addBrick(self, b):
        curBID = b.id
        self.bricks[curBID] = b
        for x in range(b.x1,b.x2+1):
            for y in range(b.y1,b.y2+1):
                for z in range(b.z1,b.z2+1):
                    if self.stack[x][y][z] != -1:
                        assert False, f"brick already as position ({x},{y},{z}): {self.stack[x][y][z]}"
                    self.stack[x][y][z] = b.id
                    
    def removeBrick(self, b):
        curBID = b.id
        self.bricks.pop(curBID)
        for x in range(b.x1,b.x2+1):
            for y in range(b.y1,b.y2+1):
                for z in range(b.z1,b.z2+1):
                    if self.stack[x][y][z] != curBID:
                        assert False, f"brick cannot be removed from position ({x},{y},{z}): {self.stack[x][y][z]}"
                    self.stack[x][y][z] = -1

    def printSliceX(self):
        print(f"viewing looking along X-axis")
        for nz in range(0,self.sz):
            z = self.sz-nz-1
            for y in range(0,self.sy):
                value = "."
                for x in range(0,self.sx):
                    newVal = self.stack[x][y][z]
                    if newVal != -1:
                        if value == ".":
                            value = newVal
                        elif newVal != value:
                            value = "????"
                print(f"{value:>4}", end=" ")
            print(f"\tz={z}")
        for y in range(0,self.sy):
            print(f"----", end=" ")
        print()
        for y in range(0,self.sy):
            print(f"{y:>4}", end=" ")
        print(f"\t=y")

    def printSliceY(self):
        print(f"viewing looking along Y-axis")
        for nz in range(0,self.sz):
            z = self.sz-nz-1
            for x in range(0,self.sx):
                value = "."
                for y in range(0,self.sy):
                    newVal = self.stack[x][y][z]
                    if newVal != -1:
                        if value == ".":
                            value = newVal
                        elif newVal != value:
                            value = "????"
                print(f"{value:>4} ", end="")
            print(f"\tz={z}")
        for x in range(0,self.sx):
            print(f"----", end=" ")
        print()
        for x in range(0,self.sx):
            print(f"{x:>4}", end=" ")
        print(f"\t=x")

    def getStack(self):
        return self.stack
    def getBrick(self, bid):
        return self.bricks[bid]
    
    def settle(self):
        floor = [[0 for y in range(0,self.sy)] for x in range(0,self.sx)]
        seenBID = []
        for zi in range(0,self.sz):
            for xi in range(0,self.sx):
                for yi in range(0,self.sy):
                    # find bricks
                    if self.stack[xi][yi][zi] != -1:
                        curBID = self.stack[xi][yi][zi]
                        if curBID in seenBID:
                            continue
                        curBrick = self.getBrick(curBID)
                        seenBID.append(curBID)
                        print(f"settling: found brick: {curBID}: {curBrick}")
                        # get all bricks points
                        points = curBrick.getPoints()
                        print(f"settling: found points: {points}")
                        # see if anything below
                        seenBelowBID = self.getBelow(curBID, points)
                        print(f"settling: below: {seenBelowBID}")
                        # if nothin below, move down
                        if seenBelowBID == []:
                            self.moveBrickDown(curBrick)
                            # move down
                        # something was below, preventing moving down. update support lists
                        else:
                            self.updateSupportedBy(curBrick, seenBelowBID)
                        seenBID.append(curBID)

    def getBrickPoints(self, x, y, z):
        points = []
        bid = self.stack[x][y][z]
        # not a brick
        if bid == -1:
            return points
        # assume starts at lowest corner
        for zi in range(z,self.sz):
            for xi in range(x,self.sx):
                for yi in range(y,self.sy):
                    if self.stack[x][y][z] == bid:
                        points.append((xi, yi, zi))
        return points
    def moveBrickDown(self, curBrick):
        points = curBrick.getPoints()
        curBID = curBrick.id
        seenBelowBID = []
        dz = -1
        while True:
            canDown = True
            for p in points:
                x, y, z = p
                # cant move into the ground
                if z+dz < 0:
                    canDown = False
                    break
                # possible to move more than 1 down; loop until hit something
                if self.stack[x][y][z+dz] not in [-1, curBID]:
                    canDown = False
                    seenBelowBID.append(self.stack[x][y][z+dz])
            if canDown:
                dz -= 1
            else:
                dz += 1
                break
        # move down dz spots. first remove current spot, then reinsert
        print(f"moving BID={curBID} dz={dz}")
        self.removeBrick(curBrick)
        curBrick.shift(0, 0, dz)
        self.addBrick(curBrick)
        # update supports if moved
        if dz != 0:
            for b1 in curBrick.supporting:
                b1.supportedBy.remove(curBrick)
            curBrick.supporting = []
            self.updateSupportedBy(curBrick, seenBelowBID)
 
    def getBelow(self, curBID, bPoints):
        seenBelow = []
        for xj, yj, zj in bPoints:
            # dont go below floor
            if zj <= 0:
                continue
            below = self.stack[xj][yj][zj-1]
            # dont see itself
            if below in [-1,curBID]:
                continue
            # must be something else, add to seenBelow if new
            if below not in seenBelow:
                seenBelow.append(below)
        return seenBelow
    def updateSupportedBy(self, curBrick, belowListBid):
        for belowBID in belowListBid:
            bBrick = self.getBrick(belowBID)
            
            if curBrick not in bBrick.supporting:
                bBrick.supporting.append(curBrick)
                curBrick.supportedBy.append(bBrick)


class Brick:
    nextId = itertools.count()
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.id = next(Brick.nextId)


        self.size = (x2-x1+1)*(y2-y1+1)*(z2-z1+1)
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.supporting = []
        self.supportedBy = []

    def __str__(self):
        return f"Brick #{self.id}"
    def infoString(self):
        return f"Brick #{self.id}: Size={self.getSize()} ({self.x1},{self.y1},{self.z1}) ~ ({self.x2},{self.y2},{self.z2})"
    def getSize(self):
        return self.size
    def getPoints(self):
        points = []
        for x in range(self.x1,self.x2+1):
            for y in range(self.y1,self.y2+1):
                for z in range(self.z1,self.z2+1):
                    points.append((x,y,z))
        return points

    def shift(self, dx, dy, dz):
        print(f"brick {self.id} is shifting by ({dx},{dy},{dz})")
        self.x1 += dx
        self.y1 += dy
        self.z1 += dz
        self.x2 += dx
        self.y2 += dy
        self.z2 += dz


with open("input22.txt") as input:
# with open("input22_demo.txt") as input:
    print("hello world")
    
    # space =[][][]
    # no negatives, nice
    xMax = 0
    yMax = 0
    zMax = 0
    inputBrickList = []
    for line in input:
        # 1,0,1~1,2,1
        x1, y1, z1, x2, y2, z2 = [int(a) for a in re.findall(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line.strip())[0]]
        # assuming input
        b = Brick(x1, y1, z1, x2, y2, z2)
        inputBrickList.append(b)
        assert (x1<=x2) and (y1<=y2) and (z1<=z2), f"coords not given low->high: {(x1, y1, z1, x2, y2, z2)}"

        xMax = max(xMax, x1+1)
        xMax = max(xMax, x2+1)
        yMax = max(yMax, y1+1)
        yMax = max(yMax, y2+1)
        zMax = max(zMax, z1+1)
        zMax = max(zMax, z2+1)
    print(f"max xyz: {xMax},{yMax},{zMax}")
    myBricks = BrickStack(xMax,yMax,zMax)
    maxSize = 0
    for b in inputBrickList:
        # print(b, b.getSize())
        print(b.infoString())
        myBricks.addBrick(b)
        maxSize = max(maxSize,b.size)
    print(maxSize)

    myBricks.printSliceX()
    myBricks.printSliceY()
    print(f"Settling...")
    # 3->434
    myBricks.settle()
    myBricks.settle()
    myBricks.settle()
    myBricks.settle()
    print(f"Settled.")
    myBricks.printSliceX()
    myBricks.printSliceY()

    for b in inputBrickList:
        print(f"{b.infoString()}: supporting: {[str(a) for a in b.supporting]}")
    print()
    for b in inputBrickList:
        print(f"{b.infoString()}: supportedBy: {[str(a) for a in b.supportedBy]}")

    # part 1 = bricks safe to disintegrate (eg. )
    # check each brick above current, and if theyre supported by >1, curBrick is safe to remove


    # ??? < ans < 614 < 767
    # support graph, hmm. DP?
    DP = {}
    result = 0
    print(f"time to disintegrate...")
    def cascade(curBlock, unsafeBIDs):
        # print(f"cascading {curBlock} with unstables {unsafeBIDs}")
        curBID = curBlock.id
        key = (curBID, tuple(sorted(unsafeBIDs)))
        if key in DP:
            return DP[key]
        # cascade if the block would make part 1 unsafe
        result = 0
        # assume curBlock unsafe for future cascade calls
        unsafeBIDs.append(curBID)
        # check how many will fall (eg. curBlock is only support it has)
        # b2 are below b1
        for b1 in curBlock.supporting:
            # its possible everything under a almost-stable block is also falling
            # eg. if every b2 in unsafe, b1 is unsafe
            allFall = True
            for b2 in b1.supportedBy:
                # print(f"does {b2} still support {b1}? ", end="")
                if b2.id not in unsafeBIDs:
                    allFall = False
                    # print(f"Yes. Onward!")
                    break
                # else:
                    # print(f"No...")
            if allFall:
                # print(f"{curBlock} cascades to {b1} giving unstable: {sorted(unsafeBIDs)}")
                # itself falls, + what else comes after
                result += 1+cascade(b1, unsafeBIDs)
        DP[(curBID, tuple(sorted(unsafeBIDs)))] = result
        return result
    
    # bl = len(inputBrickList)
    # for bi in range(0,bl):
    #     cascade(inputBrickList[bl-bi-1], [])
    result = 0
    for b in inputBrickList:
        result += cascade(b, [])
    # result = cascade(inputBrickList[0], [])
    # for k, v in DP.items():
    #     print(f"{k}: {v}")
        # result += v
    print(f"result = {result}")




    # next step: check each brick up the stack;
    # for b2 in b1.above()
    #   if len(b2.below())>1:
    #       safeBricks += 1


print("goodbye world")