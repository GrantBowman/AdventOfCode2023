import re

with open("input4.txt") as input:
    print("hello world")
    sum = 0

    i = 0
    for line in input:
        i += 1
        # if i > 3:
        #     break
        # print(line)
        
        # only care about "# # # | # # #"
        # card #: # # # | # # #
        found = re.match(r"Card\s+(\d+):((?:\s+\d+)+)\s+\|((?:\s+\d+)+)", line)
        cardId = found.group(1)
        winNumbers = found.group(2).split()
        myNumbers = found.group(3).split()
        # print(cardId)
        # print(winNumbers)
        # print(myNumbers)
        val = 0
        for n in myNumbers:
            if n in winNumbers:
                if val == 0:
                    val = 1
                else:
                    val *= 2
        sum += val
print(sum)
print("goodbye world")