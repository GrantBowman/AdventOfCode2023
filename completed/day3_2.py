


# reads left id delta = -1, reads right if delta =1
def readGrid(map, i, j, delta):
    # read left or right
    if delta == 0:
        return ""
    # in bounds row
    if (i < 0) or (i >= len(map)):
        return ""
    # in bounds col
    if (j < 0) or (j >= len(map[i])):
        return ""

    newNumber = ""
    k = j
    # read until edge or not digit
    while (j >= 0) and (j < len(map[i])) and (map[i][j] in "0123456789"):
        if delta < 0:
            newNumber = map[i][j] + newNumber
        if delta > 0:
            newNumber = newNumber + map[i][j]
        j += delta
    return newNumber

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
            if map[i][j] in "*":
                printFound = False
                if printFound: print(f"gear found at ({i},{j})")

                # top:
                # ... | +x.. | .x. | ..x+ | +xx. | +x.x+ | .xx+ | +xxx+
                # check middle:
                #   if number, grow string from there both sides
                #   if not number, try grow 2 separate from left and right x.x
                # same for bottom...

                numbers = []
                newNumber = ""
                # check adjacent spots for numbers
                # has a top
                if i > 0:
                    # has a left
                    if j > 0:
                        newNumber = readGrid(map, i-1, j-1, -1) + newNumber
                    # middle: continue number xx?, or record in prep for x.x case
                    if map[i-1][j] in "0123456789":
                        newNumber = newNumber + map[i-1][j]
                    else:
                        if newNumber != "":
                            numbers.append(int(newNumber))
                            if printFound: print(f"number found! {newNumber}")
                            newNumber = ""
                    # has a right
                    if j < len(map[i-1])-1:
                        newNumber = newNumber + readGrid(map, i-1, j+1, 1)
                    # append if number found
                    if newNumber != "":
                        numbers.append(int(newNumber))
                        if printFound: print(f"number found! {newNumber}")
                        newNumber = ""
                # check left
                newNumber = readGrid(map, i, j-1, -1)
                if newNumber != "":
                    numbers.append(int(newNumber))
                    if printFound: print(f"number found! {newNumber}")
                    newNumber = ""
                # check right
                newNumber = readGrid(map, i, j+1, 1)
                if newNumber != "":
                    numbers.append(int(newNumber))
                    if printFound: print(f"number found! {newNumber}")
                    newNumber = ""

                # has a bottom
                if i < len(map)-1:
                    # has a left
                    if j > 0:
                        newNumber = readGrid(map, i+1, j-1, -1) + newNumber
                    # middle: continue number xx?, or record in prep for x.x case
                    if map[i+1][j] in "0123456789":
                        newNumber = newNumber + map[i+1][j]
                    else:
                        if newNumber != "":
                            numbers.append(int(newNumber))
                            if printFound: print(f"number found! {newNumber}")
                            newNumber = ""
                    # has a right
                    if j < len(map[i])-1:
                        newNumber = newNumber + readGrid(map, i+1, j+1, 1)
                    # append if number found
                    if newNumber != "":
                        numbers.append(int(newNumber))
                        if printFound: print(f"number found! {newNumber}")
                        newNumber = ""
                # multiply and add to sum the found numbers if exactly 2 were found
                if len(numbers) == 2:
                    power = 1
                    for num in numbers:
                        power *= num
                    sum += power
                    if printFound: print(f"sum: {sum}\tpower:{power}")

                # check for symbols around
                continue
                '''
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
                '''
            '''
            else:
                # print(numberStr)
                if validNumber:
                    sum += int(numberStr)
                numberStr = "0"
                validNumber = False
            '''
            
        # end of row
    # print(symbols)
print(sum)



print("goodbye world")