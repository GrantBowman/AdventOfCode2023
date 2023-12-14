
with open("input3.txt") as input:
    print("hello world")
    sum = 0

    i = 0
    map = []
    symbols = ""
    for line in input:
        row = []
        for char in line.strip():
            row.append(char)
            if char not in r"\.0123456789":
                if char not in symbols:
                    symbols += char
        map.append(row)
        pass

    numberStr = "0"
    validNumber = False
    # print the map
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            # print(map[i][j], end="")
            if map[i][j] in "0123456789":
                numberStr += map[i][j]

                # check for symbols around
                if not validNumber:
                    if map[max(0,i-1)][max(0,j-1)] in symbols:
                        validNumber = True
                    if map[i][max(0,j-1)] in symbols:
                        validNumber = True
                    if map[min(i+1,len(map)-1)][max(0,j-1)] in symbols:
                        validNumber = True
                    if map[max(0,i-1)][j] in symbols:
                        validNumber = True
                    if map[i][j] in symbols:
                        validNumber = True
                    if map[min(i+1,len(map)-1)][j] in symbols:
                        validNumber = True
                    if map[max(0,i-1)][min(j+1,len(map)-1)] in symbols:
                        validNumber = True
                    if map[i][min(j+1,len(map)-1)] in symbols:
                        validNumber = True
                    if map[min(i+1,len(map)-1)][min(j+1,len(map)-1)] in symbols:
                        validNumber = True

            else:
                # print(numberStr)
                if validNumber:
                    sum += int(numberStr)
                numberStr = "0"
                validNumber = False
        # end of row- add number if valid and reset
        # print(numberStr)
        if validNumber:
            sum += int(numberStr)
        numberStr = "0"
        validNumber = False
                # go by numbers, not symbols, since a number can neighbor 2+ symbols
        # print()
    print(symbols)
print(sum)
print("goodbye world")