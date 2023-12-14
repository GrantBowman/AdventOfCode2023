import re
# https://regex101.com/r/nH4nD3/3

with open("input8.txt") as input:
    print("hello world")
    step = 0
    debugPrint = True

    i = 0
    directions = input.readline()[:-1]
    if debugPrint: print(f"directions = \'{directions}\'")
    # eat the separator
    input.readline()

    nodes = {}
    for line in input:
        # (?:(\w+)+)
        found = re.match(r"(\w+) = \(((?:(?:\w+)+(?:, )?)+)\)", line)
        label = found.group(1)
        paths = found.group(2).split(", ")
        nodes[label] = paths
        pass

    for n in nodes.items():
        if debugPrint: print(n)


    # i think we are getting into some big loops perhaps? so keep track of where each starting point gets caught?
    # path : start --> loop <-> end
    # indices are keep, so maybe a note of somthing like
    #   reached @ i = ?
    #          loop = n
    # then set the spot in the curNodes to a dummy value like None
    # dont be greedy with finishLoops, could be between multiple Z's eg (1a 2z 3a 4a 5z)
    # so save per slot the Z found, and then if that Z is not in loops, subtract cur iter from first find and count is 
    # but the directions could give different loops depending on the i
    #   AAA: AAA, BBB
    #   BBB: BBB, ZZZ
    #   ZZZ: ZZZ, AAA
    #   from ZZZ: oRLLLLLLRR vs. oLRLRLR 
    # so save the [node, i] as the key. finishLines and finishLoops as dict?
    # so... when are they done? when (per node) everything in finishLines is in finishLoops


    # if was after having it run for 30+ seconds that i knew something was up and resorted to maths...
    # i ran `python3 .\day8_2.py > output8.txt` for ~10 seconds (i think 3 wouldve been fine)
    # debug messages showed current node set, i value (pos in directions), and step value
    # extract step values for Z+i keys to find loops, and LCM to find where they all meet.
    '''
    all Z's land at i=0, and the other spots are changing, so its possible?
    [ZZZ, 	HXZ,	GHZ,	FQZ,	TPZ,	PVZ]
    [21883,	13019, 11911, 16897, 19667, 18559] <- first seen
    [43766,	26038, 23822, 33794, 39334, 37118] <- second seen (to extract loop info v v v)
    [21883,	13019, 11911, 16897, 19667, 18559] <- loop length

    consult a LCM calculator online, feeding it these 6 numbers, and we get....
    LCM ==> 12,833,235,391,111 aka 12833235391111
    https://www.calculatorsoup.com/calculators/math/lcm.php
    ...wow
    '''

    curNodes = []
    finishLines = [{} for n in curNodes]
    finishLoops = [{} for n in curNodes]
    # get starting set
    for n in nodes.keys():
        if n[-1] == "A":
            curNodes.append(n)
    # traverse
    while True:
        if debugPrint: print(f"currently at: {curNodes}, i={i}, step={step}")
        # check end
        isDone = True
        for a in range(0,len(curNodes)):
            if debugPrint: print(f"checking {curNodes[a]}: {curNodes[a][-1]}")
            if curNodes[a][-1] != "Z":
                isDone = False
                break
                    # # has looped back
                    # if ((n[a]. i) in finishLines[a]) and (n[a]. i) not in finishLoops[a]:
                    #     finishLoops[a][(n[a], i)] =
                    # # first time
                    # if (n[a]. i) not in finishLines[a]:
                    #     pass
        if isDone:
            break

        # get directions (same for all)
        rl = 0 if directions[i] == "L"  else 1
        i += 1
        if i >= len(directions):
            i = 0

        # loop through all spots, appending to nextNodes
        nextNodes = []
        step +=1
        for n in curNodes:
            if not n:
                nextNodes.append(n)
            # loop over directions
            nextNodes.append(nodes[n][rl])
        curNodes = nextNodes
print(step)
print("goodbye world")