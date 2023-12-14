import re
from functools import cmp_to_key

def handCompare(a, b):
    if a[0] < b[0]:
        return -1 
    if a[0] > b[0]:
        return 1 
    ranking = "23456789TJQKA"
    for i in range(0,len(a[1])):
        ra = ranking.find(a[1][i])
        rb = ranking.find(b[1][i])
        if ra < rb:
            return -1
        if ra > rb:
            return 1
    return 0


    return 1

def rank(hand):
    # https://stackoverflow.com/questions/32816104/convert-every-character-in-a-string-to-a-dictionary-key
    cards = { char:(hand.count(char)) for char in hand }
    cardCounts = sorted(list(cards.values()), reverse=True)
    # 5 of a kind = 6
    if cardCounts[0] == 5:
        return 6
    # 4 of a kind = 5
    if cardCounts[0] == 4:
        return 5
    # full house = 4
    if cardCounts[0] == 3 and cardCounts[1] == 2:
        return 4
    # 3 of a kind = 3
    if cardCounts[0] == 3:
        return 3
    # 2 pair = 2
    if cardCounts[0] == 2 and cardCounts[1] == 2:
        return 2
    # 1 pair = 1
    if cardCounts[0] == 2:
        return 1
    # high card = 0
    return 0

with open("input7.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    handInfoList = []
    for line in input:
        
        # if debugPrint: print(line)
        found = re.match(r"(.....) (\d+)",line)
        # sorted, raw, value
        handInfo = [rank(found.group(1)), found.group(1), int(found.group(2))]
        # if debugPrint: print(handInfo)
        handInfoList.append(handInfo)

    handInfoList.sort(key=cmp_to_key(handCompare))
    for i in range(0,len(handInfoList)):
        handInfo = handInfoList[i]
        sum += handInfo[2]*(i+1)
        if debugPrint: print(handInfo, i+1)
print(sum)
print("goodbye world")