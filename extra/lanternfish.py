import re
# https://regex101.com/r/nH4nD3/3
from itertools import cycle

with open("input_lanternfish.txt") as input:
    print("hello world")
    debugPrint = True

    i = 0
    fish = [0 for i in range(0,9)]
    fishpool = cycle(fish)
    startingFish = [int(x) for x in input.readline().split(',')]
    # print(startingFish)
    for f in startingFish:
        fish[f] += 1
    print(fish)
    m = len(fish)
    for d in range(0,256):
        i = d % m
        fish[(i+6+1) % m] += fish[i]
        # fish[(i+8+1) % m] += fish[i]
        # fish[i] = 0
        # print(f"after day {d+1}: {fish} ({sum(fish)})")
        # print(f"           {' ' * len(str(d+1))}  {'   ' * i}^")
    # print(fish)
    # print(f"0{'   ' * i}^")
    print(sum(fish))

    # example result
    # exampleFish = [0 for i in range(0,9)]
    # for f in "6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8".split(","):
    #     exampleFish[int(f)] += 1
    # print(exampleFish)




print("goodbye world")