import re

with open("input6.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = True


    # seeds
    line = input.readline()
    if debugPrint: print(line)
    found = re.match(r"Time:\s+((?:\s+\d+)+)",line)
    times = [int(x) for x in found.group(1).split()]
    if debugPrint: print(times)

    line = input.readline()
    if debugPrint: print(line)
    found = re.match(r"Distance:\s+((?:\s+\d+)+)",line)
    distances = [int(x) for x in found.group(1).split()]
    if debugPrint: print(distances)


    # This was solved using maths!

    # t_0 = 3
    # d_0 = 3*0, 2*1, 1*2, 0*3
    #       0,   2,   2,   0
    # d = t*(t_m-t)
    # if > d, 
    # 
    # using desmos:
    # Time:        55           99           97             93
    # Distance:   401         1485         2274           1405
    #            8.7-46.3                39.6-57.3
    #                       18.4-80.5                   18.98-74.02
    #             9-46        19-80        40-57          19-74
    #             37           61           17             55
    # OBOE
    # 38 * 64 * 18 * 56 = 2451456
    # 2,179,485 < ans < 2,451,456 
    # 2110295
    # 2374848
    # x1 = 8433453.76  ->  8433453
    # x2 = 47566339.23 -> 47566339
    # 47566339 - 8433453 = 39132886
 


print("goodbye world")