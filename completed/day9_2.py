import re
# https://regex101.com/r/nH4nD3/3
import numpy as np
from numpy.polynomial import Polynomial

with open("input9.txt") as input:
    print("hello world")
    sum = 0
    debugPrint = False

    i = 0
    for line in input:
        # i += 1
        # if i > 3:
        #     break
        numbers = [int(x) for x in line.split()]
        if debugPrint: print(f"numbers: {numbers}")
        
        deg = 0
        differences = numbers
        # find degree
        while True:
            if debugPrint: print(f"differences: {differences}, deg = {deg}")
            newDifferences = []
            allZero = True
            for j in range(1,len(differences)):
                diff = differences[j]-differences[j-1]
                newDifferences.append(differences[j]-differences[j-1])
                if allZero and diff != 0:
                    allZero = False
            differences = newDifferences
            if allZero:
                break
            else:
                deg += 1
        # fit to polynomial
        if debugPrint: print(f"differences: {differences}, deg = {deg}")
        xVals = range(0,len(numbers))
        yVals = numbers
        myPolynomial = Polynomial.fit(xVals, yVals, deg)
        if debugPrint: print(f"polynomial of deg {deg} coefs: {polynomial}")
        # extrapolate teh next value, add to sum
        nextVal = myPolynomial(-1)
        if debugPrint: print(f"next number =  {nextVal}")
        sum += nextVal
print(sum)
print("goodbye world")
