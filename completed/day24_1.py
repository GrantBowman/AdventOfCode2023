import re
# https://regex101.com/r/nH4nD3/3
debugPrint = True

# a lot of maths here, used reference videos to codify it
# especially since i knew there would be libraries and known algorithms for this stuff,
# and christmas time, i really didnt want to put too much effort here.
# using the ax+by+c=0 method form HyperNeutrino:
# https://www.youtube.com/watch?v=guOyA7Ijqgk

# I started by deriving my own formulas but tbh it was a headache i didnt want, sorry!
# still learning a good amount about this type of problem tho

class Hailstone:
    def __init__(self, sx, sy, sz, vx, vy, vz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.vx = vx
        self.vy = vy
        self.vz = vz

        # point on line as (px, py)
        # also given as x+t*vx, := px
        # x+t*vx = px
        # y+t*vy = py
        # solve for the shared variable t:
        # (py-y)/vy = t = (px-x)/vx
        # set t = 0, solve
        # (py-y)/vy -(px-x)/vx = 0
        # multiply so dont have to worry about divide by 0
        # also just need to see if its true (eg. intersects)
        # vy(px-x) - vx(py-y) = 0
        # -vy*x + vx*y + (-vy*x + vx*y) = 0
        # = a*x +  b*y +       c       = 0
        self.a = -vy
        self.b = vx
        self.c = -vy*sx + vx*sy 

    def __repr__(self):
        return f"Hailstone a={self.a}, b={self.b}, c={self.c} {(self.sx, self.sy, self.sz, self.vx, self.vy, self.vz)}"



with open("input24.txt") as input:
    print("hello world")
    # 300 inputs? could probably brute-force a pairwise match if have a good intersection check function...

    boundaryMin = 200000000000000
    boundaryMax = 400000000000000
    # boundaryMin = 7
    # boundaryMax = 27
    # the determinant thing wants endpoints. We know the bounds (200000000000000, 400000000000000), aka (2e14, 4e14)

    hailstones = []
    for line in input:
        line = line.strip()
        found = re.findall(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)[0]
        sx, sy, sz, vx, vy, vz = [int(a) for a in found] 
        h = Hailstone(sx, sy, sz, vx, vy, vz)
        hailstones.append(h)
    # for h in hailstones:
    #     print(h)
    # find intersections, then check if in bounds
    result = 0
    for i, hs1 in enumerate(hailstones):
        for hs2 in hailstones[i+1:]:
            a1, b1, c1 = hs1.a, hs1.b, hs1.c
            a2, b2, c2 = hs2.a, hs2.b, hs2.c
            # check for parallel (slope a1/b1 = a2/b2)
            # but cross mltiply to avoid div by 0
            if a1*b2 == a2*b1:
                # parallel, wont intersect
                continue
            # has intersection, find it
            # a1*x + b1*y + c1 = 0
            # a2*x + b2*y + c2 = 0
            # find equal = ... = 
            x = (c1*b2-c2*b1)/(a1*b2-a2*b1)
            y = (c1*a2-c2*a1)/(b1*a2-b2*a1)
            # print(x, y)
            # now that have intersection, check boundary
            if boundaryMin<=x<=boundaryMax and boundaryMin<=y<=boundaryMax:
                # check was also in the future for both
                # using the sign of difference matches the sign of velocity
                # multiply +*+ = -*- = +; -*+ = +*- = -
                hs1Future = ((x-hs1.sx)*hs1.vx >= 0) and ((y-hs1.sy)*hs1.vy >= 0) 
                hs2Future = ((x-hs2.sx)*hs2.vx >= 0) and ((y-hs2.sy)*hs2.vy >= 0)
                if hs1Future and hs2Future:
                    result += 1
                #     print(f"crossed in future")
                # else:
                #     print(f"crossed in past")
    print(result)


print("goodbye world")