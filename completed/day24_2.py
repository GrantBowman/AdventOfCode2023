import re
# https://regex101.com/r/nH4nD3/3
import sympy
debugPrint = True

# a lot of maths here, used reference videos to codify it
# especially since i knew there would be libraries and known algorithms for this stuff,
# and christmas time, i really didnt want to put too much effort here.
# using the ax+by+c=0 method form HyperNeutrino:
# https://www.youtube.com/watch?v=guOyA7Ijqgk

# I started by deriving my own formulas but tbh it was a headache i didnt want, sorry!
# still learning a good amount about this type of problem tho

# for part 2, multiple guides said "yeah this is a lot more complicated" then went to use libraries like synpy or z3
# so i think im allowed to do likewise at this point.
# i really dont want to implement my own linear algebra solver / stepper

# part 2 is more intuitive to me mathematically:
# solve for 3 hailstones intersecting an unknown ax+by+c=0
# then the known values of the 3 hailstones can solve the concrete values of ax+by+c=0
# since you know the slove, add one more for the time of t=0
# add them up
# BUT also these numbers are very large and would need to plug into a computer to get that final answer anyway,
# even if solving by hand
# i see no issue using the given numbers, this process, and then the results through a solver.
# ive solved other days using pure maths, no? (day 6, various partial solves plugged in to LCM)

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

# hailstone h
# rock r
# sh + t*vh = sr + t*vr
# t = (sr-sh)/(vh-vr)
# repeat for every variable?
# + repeat for 3+ hailstones?
# -> 9 equations?
# like, boom, thats your system. mechanically reduce row-echelon form it, and you have your answer
# but, big numbers. use a solver. use code to pull values. use a library instead of a website

# this library manipulates the symbols like you do in maths irl, or so iv ebeen told
sxr, syr, szr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")
# from the 3 [x/y/z] hail_coord <-> rock_coord equations we get:
# (sr-sh)/(vh-vr) [base, for each coord]
# (sxr-sxh)/(vxh-vxr)=(syr-syh)/(vyh-vyr)
# (sxr-sxh)*(vyh-vyr)=(syr-syh)*(vxh-vxr)
# (sxr-sxh)*(vyh-vyr)-(syr-syh)*(vxh-vxr)=0
# repeat, switching (x,y)->(y,z)->(z,x)
# (syr-syh)*(vzh-vzr)-(szr-szh)*(vyh-vyr)=0
# (szr-szh)*(vxh-vxr)-(sxr-sxh)*(vzh-vzr)=0
equations = []
for hs in hailstones:
    sxh, syh, szh, vxh, vyh, vzh = hs.sx, hs.sy, hs.sz, hs.vx, hs.vy, hs.vz
    equations.append((syr-syh)*(vzh-vzr)-(szr-szh)*(vyh-vyr))
    equations.append((szr-szh)*(vxh-vxr)-(sxr-sxh)*(vzh-vzr))
answers = sympy.solve(equations)
print(answers)
ax, ay, az = answers[0][sxr], answers[0][syr], answers[0][szr]
print(ax+ay+az)


print("goodbye world")