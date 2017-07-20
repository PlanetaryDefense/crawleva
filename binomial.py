# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:57:39 2017
"""
import csv 
from random import randint
from sympy.solvers import solve
from sympy import Symbol, expand, Poly
import math
from decimal import Decimal
from numpy import roots

print("Enter the total number of pages in dataset: ")
total = int(input())
print("Enter sample size: ")
sampleSize = int(input())
print("Enter trials to perform: ")
trials = int(input())

#import csv file for reading
def readFile():
    with open('C:/Users/yjiang8/Desktop/eva_2rows.txt', encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter = "\t")
        data = list(reader)
        
    return data

# calculate the relevant number of pages from sample
def calcRelevant(listInput):
    successNum = 0
    for row in range(0,sampleSize):
        if listInput[row][1] == 'Yes':
            successNum = successNum + 1
    return successNum


#create random generator and fill sampleArr from original data
def fillSampleArr(dataFile):
    sampleArr = []
    for x in range(0,sampleSize):
        sampleArr.append([])
    for i in range(0,sampleSize):
        randomNum = randint(0,total)
        sampleArr[i][:] = dataFile[randomNum][:]
    return sampleArr

# function for calculating n choose x part of equation
# INPUT: successNum - number of successes in given sample
# INPUT: sampleSize - user specified size of sample
# RETURNS: computation of N choose X
def NchooseX(total, sampleSize):
    topEquation = math.factorial(total)
    bottomEquation = Decimal((math.factorial(sampleSize)*math.factorial((total-sampleSize))))
    return Decimal(topEquation/bottomEquation)

data = readFile()
global Px
Px = 0.0
for trialNum in range(0,trials):
    tempArr = fillSampleArr(data)
    numRelevant = calcRelevant(tempArr)
    Px += float((numRelevant/sampleSize))
    
print("Px is " + str(Px))
# average P(x) calcuated to solve for p    
averagePx = Decimal(Px/trials)
print("Average P(x): " + str(averagePx))
equationLeft = averagePx/NchooseX(total, sampleSize)

# solve the equation for p
p = Symbol('p')
x = sampleSize
n = total
a = Poly((p**x)*(1-p)**(n-x) - equationLeft, p).all_coeffs()
rootArr = roots(a) # find soluition for p value
rootArr = rootArr.real #get only real solutions

# print out real roots
for arrIndex in range(0, rootArr.size):
    print(rootArr[arrIndex])