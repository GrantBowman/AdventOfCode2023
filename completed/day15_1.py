import re
# https://regex101.com/r/nH4nD3/3

def hashChar(char):
    return 0

with open("input15.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    line = input.readline()
    sequences = line.split(",")
    # print(sequences)

    for seq in sequences:
        hashVal = 0
        for char in seq:
            if char == "\n":
                print("NEWLINE SPOTTED")
            hashVal += ord(char)
            hashVal *= 17
            hashVal %= 256
        #     print(f"{char}:{hashVal} | ", end="")
        # print(f"{seq} , {hashVal} | ", end="")
        # sum += hashVal
print()
print(sum)
print("goodbye world")


# 505533 not right