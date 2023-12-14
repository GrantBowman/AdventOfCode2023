import re

with open("input5.txt") as input:
    print("hello world")
    debugPrint = False

    # almanac form: [from, to]: [dest, start, range]
    almanac = {}

    # seeds
    line = input.readline()
    if debugPrint: print(line)
    found = re.match(r"(\w+):((?:\s+\d+)+)",line)
    startType = found.group(1)
    seeds = [int(s) for s in found.group(2).split()]
    if debugPrint: print(f"type={startType}:", end="")
    for s in seeds:
        if debugPrint: print(s)
    
    # whitespace
    input.readline()


    # xxx-to-yyy map:
    # ### ### ###
    # ### ### ###

    # construct the almanac
    while True:
        # get the group info
        line = input.readline()
        if not line:
            break

        conversions = re.match(r"(\w+)-to-(\w+) map:", line)
        key = (conversions.group(1), conversions.group(2))
        if debugPrint: print(key)

        values = []
        while True:
            line = input.readline()
            if line.strip() == "":
                break
            numbers = [int(n) for n in line.split()]
            if debugPrint: print(numbers)
            values.append(numbers)
            # for n in numbers:
            #     print(n, end=", ")
            # print()
        almanac[key] = values
        if not line:
            break
    if 1 or debugPrint: print(almanac.keys())
    if debugPrint: print(almanac[("seed","soil")])

    # newSeeds
    for k in almanac.keys():
        if debugPrint: print(f"mapping: {k[0]} to {k[1]}...")
        mappings = almanac[k]
        # make copies
        newSeeds = [x for x in seeds]
        for i in range(0,len(newSeeds)):
            s = newSeeds[i]
            if debugPrint: print(f"before: {seeds[0]}")
            # mapped = False
            # either is in the range, or the dif is between 0 and the range
            for m in mappings:
                minmap = m[1]
                maxmap = m[1] + m[2]
                if (minmap <= s) and (s < maxmap):
                    if debugPrint: print(f"mapping using: {m}")
                    newSeeds[i] = m[0] + (s - m[1])
                    # mapped = True
                    break
        seeds = newSeeds
        if debugPrint: print(f"after: {seeds[0]}")
    seeds.sort()
    print(seeds)






print("goodbye world")