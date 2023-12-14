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
    seedRanges = [int(x) for x in found.group(2).split()]
    seeds = []
    for i in range(0,len(seedRanges), 2):
        # print(f"pair {seedRanges[i]} {seedRanges[i+1]} becomes {seedRanges[i]}-{seedRanges[i]+seedRanges[i+1]}")
        seeds.append([seedRanges[i], seedRanges[i+1]])


    # seeds = [int(s) for s in found.group(2).split()]
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
    if debugPrint: print(almanac.keys())
    if debugPrint: print(almanac[("seed","soil")])

    # newSeeds
    for k in almanac.keys():
        if debugPrint: print(f"mapping: {k[0]} to {k[1]}...")
        mappings = almanac[k]
        # make copies
        newSeeds = [x for x in seeds]
        mappedSeeds = []
        '''
        for i in range(0,len(seeds)):
            s = seeds[i]
            if debugPrint: print(f"before: {seeds[0]}")
            # mapped = False
            # either is in the range, or the dif is between 0 and the range
            # break up the mappings as needed...
        '''
        
        if debugPrint: print(f"before: {seeds}")
        seedStack = [x for x in seeds]
        # loop through seed ranges (to apply mapping, splitting as needed)
        while True:
            if len(seedStack) <= 0:
                break
            s = seedStack.pop()
            if debugPrint: print(f"popped: {s}")

            isMapped = False
            for m in mappings:
                if debugPrint: print(f"looking at mapping: {m}")
                minmap = m[1]
                maxmap = m[1] + m[2]
                minseed = s[0]
                maxseed = s[0] + s[1]
                # check if need to break up the range
                # minmap <= minseed < maxseed <= maxmap
                # ^ no change needed
                # so only need to split if minmap or maxmap sits between the two, eg:
                # minmap <= minseed < maxmap < maxseed
                #            ...........|.........
                # minseed < minmap < maxseed <= maxmap
                #  ...........|.........
                # minseed < minmap < maxmap < maxseed
                #  .......|.................|.......
                #                            ...|... later? possible.
                # minmap <= minseed < maxseed <= maxmap
                #          .................
                if (minmap <= minseed) and (minseed < maxmap) and (maxmap < maxseed):
                    if debugPrint: print(f"seed range starts mid-map. splitting...")
                    frontRange = maxmap - minseed
                    backRange = maxseed - maxmap
                    if debugPrint: print(f"\tresult in {[maxmap, backRange]} unmapped, mapping {[minseed,frontRange]} to {[m[0]+(minseed-minmap), frontRange]}")
                    # apply tha mapping now while the numbers are here, ie save starting at minmap offset instead of minseed
                    mappedSeeds.append([m[0]+(minseed-minmap), frontRange])
                    seedStack.append([maxmap, backRange])
                    isMapped = True
                    break
                elif (minseed < minmap) and (minmap < maxseed) and (maxseed < maxmap):
                    if debugPrint: print(f"mapping starts mid-seed range. splitting...")
                    frontRange = minmap - minseed
                    backRange = maxseed - minmap
                    if debugPrint: print(f"\tresult in {[minseed, frontRange]} unmapped, mapping {[minmap,backRange]} to {[m[0], backRange]}")
                    seedStack.append([minseed, frontRange])
                    # apply tha mapping now while the numbers are here, ie save starting at minmap instead of minseed
                    mappedSeeds.append([m[0], backRange])
                    isMapped = True
                    break
                elif (minseed < minmap) and (minmap < maxmap) and (maxmap < maxseed):
                    if debugPrint: print(f"mapping within seed range. splitting...")
                    frontRange = minmap - minseed
                    midRange = maxmap - minmap
                    backRange = maxseed - maxmap
                    if debugPrint: print(f"\tresult in {[minseed, frontRange]} and {[maxmap, backRange]} split, mapping {[minmap,midRange]} to {[m[0], midRange]}")
                    # apply tha mapping now while the numbers are here, ie save starting at minmap instead of minseed
                    seedStack.append([minseed, frontRange])
                    mappedSeeds.append([m[0], midRange])
                    seedStack.append([maxmap, backRange])
                    isMapped = True
                    break
                elif (minmap <= minseed) and (minseed < maxseed) and (maxseed <= maxmap):
                    if debugPrint: print(f"seed range within mapping range. mapping...")
                    if debugPrint: print(f"\tresult in mapped to {[m[0]+(minseed-minmap), s[1]]}")
                    mappedSeeds.append([m[0]+(minseed-minmap), s[1]])
                    isMapped = True
                    break
            if not isMapped:
                if debugPrint: print(f"seed range not split by mapping, good as is...")
                mappedSeeds.append([s[0], s[1]])
        seeds = mappedSeeds
        if debugPrint: print(f"after: {seeds}")
    seeds.sort()
    print(seeds)




print("goodbye world")