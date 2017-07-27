# -*- coding: utf-8 -*-
"""
Program takes in webcrawler dataset and outputs a new dataset comprised of
random samples of each round, arranged by the round.  The output dataset is
put into another program in order to calculate the accuracy of the webcrawler for
each round after the output dataset is manually evaluated

@author: Joseph George
"""

import csv
from tkinter import filedialog
from tkinter import *
from random import randint

def readFile():
    """
    Reads in CSV file using tkinter GUI
            
    Returns: 
        Dataset containing rows extracted from CSV file
    """
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files",".csv"),("all files","*.*")))

    with open(root.filename, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter = ",")
        data = list(reader)
        
    root.destroy() # close the file picker 
    return data


def writeSamples(crawlRoundArray):
    """
    Takes random samples from specific round and appends samples to 
    an array which will be eventually written to new CSV file    
    
    Args:
        crawlRoundArray: array containing all crawls from same round
    """
    sampleSize = int(len(crawlRoundArray) * .10) # sample size is 10% of total population
    for i in  range(0, sampleSize):
        randomNum = randint(0,len(crawlRoundArray)-1)
        sampleArr.append(crawlRoundArray[randomNum][:])
        
def writeSampleCSV(sampleArray):
    """
    Writes array full of samples from each round to a new CSV file
    
    Args:
        sampleArray: array containing random samples from each round of the crawler
    """
    # make sure there is a blank "output.csv" file in working directory to save to!
    with open("output.csv", "w", newline='', encoding="utf8") as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(sampleArray)
    
data = readFile()
sampleArr = []

# csv file rows arranged by round of crawl from least to greatest,
# assuming the column containing the round is the 6th (key = 5)
data = sorted(data, key = lambda x: x[5])

rowMarker = 0
roundMarker = 1
while True:    
    roundList = []
    while (data[rowMarker][5] == data[rowMarker + 1][5]):
        roundList.append(data[rowMarker][:])
        rowMarker+=1
        if(rowMarker == len(data)-1):
            break
    roundList.append(data[rowMarker][:]) # takes care of appending final round value
    if roundMarker > 1: # skip the first round, which are seed URLs
        writeSamples(roundList) # pass specific round array for sampling
    if rowMarker == len(data) - 1:
        break
    roundMarker += 1
    rowMarker+=1
    
writeSampleCSV(sampleArr)
