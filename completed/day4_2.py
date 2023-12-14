import re

with open("input4.txt") as input:
    print("hello world")
    sum = 0
    cardWins = []
    cards = []

    i = 0
    for line in input:
        i += 1
        # if i > 20:
        #     break

        debugPrint = True
        # print(line)
        
        # only care about "# # # | # # #"
        # card #: # # # | # # #
        found = re.match(r"Card\s+(\d+):((?:\s+\d+)+)\s+\|((?:\s+\d+)+)", line)
        cardId = found.group(1)
        winNumbers = found.group(2).split()
        myNumbers = found.group(3).split()

        wins = 0
        for n in myNumbers:
            if n in winNumbers:
                wins += 1
        cards.append(1)
        cardWins.append(wins)
    if debugPrint: print (cards)
    if debugPrint: print (cardWins)
    for i in range(0, len(cards)):
        sum += cards[i]
        if debugPrint: print(f"wins:{cardWins[i]}, j=", end="")
        for j in range(0, cardWins[i]):
            if debugPrint: print(j, end=" ")
            # dont go out of bounds
            if i+j+1 >= len(cards):
                break
            cards[i+j+1] += cards[i]
        if debugPrint: print()
    if debugPrint: print (cards)

    
print(sum)
print("goodbye world")