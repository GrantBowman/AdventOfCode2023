import re

with open("input_1_1") as input:
    print("hello world")
    i = 0
    sum = 0
    for line in input:
        i += 1
        
        # print(line[:-1])

        # part 1 regex:
        found = re.findall("(\d)", line)

        # part 2 regex:
        # found = re.findall("(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

        d1 = found[0]
        d2 = found[-1]

        if (d1 == "zero" or d2 == "zero" or d1 == 0 or d2 == 0):
            print(f"{d1} {d2}: {val}: {sum}:\t" + line[:-1])


        digits = ["zero", "one", "two", "three", "four" ,"five", "six", "seven", "eight", "nine"]
        if not d1.isdigit():
            d1 = str(digits.index(d1))
        if not d2.isdigit():
            d2 = str(digits.index(d2))


        val = int(d1+d2)
        sum += val

        # debug output: digits, concat, sum, line
        print(f"{i}) \'{d1}\'+\'{d2}\'={val}: sum={sum}:\t" + line[:-1],found)

        # break
        # if i > 10:
        #     break
        # continue

print("sum = " + str(sum))