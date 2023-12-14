import re

with open("input2_1") as input:
    print("hello world")

    # given: 12 red, 13 green, 14 blue
    realBag = {"red": 12, "green": 13, "blue": 14}
    sum = 0

    i = 0
    # Game 1: 5 red, 1 green; 6 red, 3 blue; 9 red; 1 blue, 1 green, 4 red; 1 green, 2 blue; 2 blue, 1 red
    
    for line in input:
        i += 1
        gameBag = {}
        parts = line.split(r": ")
        # print(parts)
        gameId = int(re.match(r"\D*(\d+)\D*",parts[0]).group(1))
        # print(gameId)
        draws = parts[1].split("; ")
        print(f"{gameId}: {draws}")
        # draws is the collection of all amount + colour in a line, eg "1 red, 2 blue; 3 green, 4 red"
        for draw in draws:
            # draw is the collection per single group, eg "1 red, 2 blue"
            # print(draw)
            for x in draw.split(r", "):
                
                # print(x)
                count = int(re.match(r"(\d+)", x).group(1))
                # print(count +" - "+x)
                colour = re.match(r"^[^a-z]*([a-z]+)$", x).group(1)
                # print(count, "-", colour)
                if colour not in gameBag:
                    gameBag[colour] = count
                else:
                    gameBag[colour] = max(gameBag[colour], count)
        print(gameBag)
        validGame = True
        for colour in gameBag.keys():
            if gameBag[colour] > realBag.get(colour, 0):
                validGame = False
        if validGame:
            sum += gameId
            
        # if i > 3:
        #     break

print(sum)
print("goodbye world")