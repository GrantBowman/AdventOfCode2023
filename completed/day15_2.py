import re
# https://regex101.com/r/nH4nD3/3

def getLabelIndex(box, label):
    for i in range(0,len(box)):
        if label == box[i][0]:
            return i
    return -1

with open("input15.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True

    i = 0
    line = input.readline()
    sequences = line.split(",")
    # print(sequences)
    boxes = [[] for x in range(0, 256)]

    for seq in sequences:
        hashVal = 0
        label, operation, foundPower = re.match(r"^(\w+)([-=])(\d+)?$", seq).groups()
        # label = foundLabel.group(1)
        # foundPower = re.match(r"^\w+=(\d+)$", seq)
        power = -1
        if foundPower:
            power = int(foundPower)
        # print(f"{label}:{power} | ", end="")
        # print(f"{label}, {operation}, {power}")
        label = label
        for char in label:
            hashVal += ord(char)
            hashVal *= 17
            hashVal %= 256
        #     print(f"{char}:{hashVal} | ", end="")
        # print(f"{seq} , {hashVal} | ", end="")
        sum += hashVal
        box = boxes[hashVal]
        # box logic
        if operation == "-":
            index = getLabelIndex(box, label)
            if index != -1:
                boxes[hashVal].pop(index)
        if operation == "=":
            index = getLabelIndex(box, label)
            if index != -1:
                boxes[hashVal][index] = (label, power)
            else:
                boxes[hashVal].append((label, power))
    
    # check boxes
    # for i in range(0,len(boxes)):
    #     if boxes[i] != []:
    #         print(f"{i}: {boxes[i]}")

    # do the maths
    sum = 0
    for i in range(0,len(boxes)):
        box = boxes[i]
        for j in range(0, len(box)):
            power = box[j][1]
            sum += (i+1)*(j+1)*(power)


# print()
print(sum)
print("goodbye world")


# 505533 not right