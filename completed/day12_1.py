import re
# https://regex101.com/r/nH4nD3/3

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
    
def countChoices(springs, groups):
    result = 0
    for i in range(0,len(springs)):
        s = springs[i]
        # if "?", split and return
        if s == "?":
            result += countChoices(springs[:i] + "." + springs[i+1:], groups)
            result += countChoices(springs[:i] + "#" + springs[i+1:], groups)
            return result
    # did not split on any "?", so no choices
    return isValid(springs, groups)


        

    

with open("input12.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    i = 0
    for line in input:
        springs, groups = line.split(" ")
        groups = [int(x) for x in groups.split(',')]
        lineResult = countChoices(springs, groups)
        sum += lineResult
        if debugPrint: print(springs, groups, end=" | ")
        if debugPrint: print(lineResult)
        pass

    # could be greedy and count if '#' + '?' == sum(damaged), implying only 1 way
    # -> validate, do a DP split on substrings and an array of integers
    #  eg "??#.# 2,1"
    # -> ".?#.# 2,1"
    # -> "#?#.# 2,1"
    # options to fill multiple ??? with all possible
print(sum)
print("goodbye world")