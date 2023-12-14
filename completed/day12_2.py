import re
# https://regex101.com/r/nH4nD3/3

debugPrint = False

def isValid(springs, groups):
    curChain = 0
    foundChains = []
    # run through
    for i in range(0,len(springs)):
        s = springs[i]
        if s == "#":
            curChain += 1
        if s == ".":
            if curChain > 0:
                foundChains.append(curChain)
            curChain = 0
    # catch ending chain
    if curChain > 0:
        foundChains.append(curChain)
        curChain = 0
    
    return foundChains == groups
    
DP = {}
# key = springs, groups, (i, gi, gc)
# since springs could have previous ? modifications
# eg. (.#.?, [1, 1], 2, 1, 0)
#  vs (#..?, [1, 1], 2, 1, 0)
# from ??.?
# when really the stuff after the beginning should be the DP. so use springs[i:]
def countChoices(springs, groups, i=0, groupi=0, curChain=0):
    # springs could ave '?' replaced, so track that too
    key = (springs[i:], tuple(groups), i, groupi, curChain)
    result = 0
    # check DP:
    if key in DP:
        if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
        if debugPrint: print(f"key = {key}")
        if debugPrint: print(f"key in DP: {DP[key]}")
        return DP[key]
    # if is end, check validitity
    if i == len(springs):
        result = int(isValid(springs, groups))
        if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
        if debugPrint: print(f"key = {key}")
        if debugPrint: print(f"end of string: {result}")
        DP[key] = result
        return result
    # if "?", split and return
    # if ".", run chaining logic and prune
    if springs[i] == ".":
        if curChain > 0:
            # onto next chain group, reset counter
            # prune if this group chain count doesnt match what the next group should be
            if groupi >= len(groups) or curChain == groups[groupi]:
                result = countChoices(springs, groups, i+1, groupi+1, 0)
                DP[key] = result
                if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
                if debugPrint: print(f"key = {key}")
                if debugPrint: print(f"returning... . result = {result}")
                return result
            else:
                DP[key] = result
                if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
                if debugPrint: print(f"key = {key}")
                if debugPrint: print(f"returning... .p result = {result}")
                return result
        elif curChain == 0:
            # not currently chaining, so dont increment group
            result = countChoices(springs, groups, i+1, groupi, curChain)
            DP[key] = result
            if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
            if debugPrint: print(f"key = {key}")
            if debugPrint: print(f"returning... .0 result = {result}")
            return result
    # continue chaining
    if springs[i] == "#":
        # prune: chain too long
        if groupi >= len(groups) or curChain == groups[groupi]:
            DP[key] = result
            if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
            if debugPrint: print(f"key = {key}")
            if debugPrint: print(f"returning... #p result = {result}")
            return result
        result = countChoices(springs, groups, i+1, groupi, curChain+1)
        DP[key] = result
        if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
        if debugPrint: print(f"key = {key}")
        if debugPrint: print(f"returning... # result = {result}")
        return result
    # could be either, branch
    if springs[i] == "?":
        result = 0
        result += countChoices(springs[:i] + "." + springs[i+1:], groups, i, groupi, curChain)
        result += countChoices(springs[:i] + "#" + springs[i+1:], groups, i, groupi, curChain)
        if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
        if debugPrint: print(f"key = {key}")
        if debugPrint: print(f"returning... ? result = {result}")
        DP[key] = result
        return result
    # 
    else:
        result = countChoices(springs, groups, i+1, groupi, curChain)
        DP[key] = result
        if debugPrint: print(f"        012345678901234567890123456789012345678901234567890123456789")
        if debugPrint: print(f"key = {key}")
        if debugPrint: print(f"returning... result = {result}")
        return result


        

    

with open("input12.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False
    debugPrintInner = True

    i = 0
    for line in input:
        stretchFactor = 5
        springs, groups = line.split(" ")
        groups = [int(x) for x in groups.split(',')]

        # the part 2 modifications:
        springsBase = springs
        for i in range(0, stretchFactor-1):
            springs += "?"
            springs += springsBase
        groups = groups * stretchFactor

        DP = {}
        lineResult = 0
        lineResult = countChoices(springs, groups)
        sum += lineResult
        if debugPrintInner: print(springs, groups, end=" | ")
        if debugPrintInner: print(lineResult)

        # break
        pass

    # could be greedy and count if '#' + '?' == sum(damaged), implying only 1 way
    # -> validate, do a DP split on substrings and an array of integers
    #  eg "??#.# 2,1"
    # -> ".?#.# 2,1"
    # -> "#?#.# 2,1"
    # options to fill multiple ??? with all possible
print(sum)
print("goodbye world")

#.#.###.#.#.###.#.#.###.#.#.###.#.#.###.#.#.###
