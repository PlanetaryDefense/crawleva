# -*- coding: utf-8 -*-
"""
Program uses Simple Random Sampling and the principle of the Central Limit Theorem
to approximate the percentage of relevant pages within a confidence interval
from a randomly selected sample of all webcrawler results by the round

Results are saved to text file in working directory

@author：Joseph George

"""

# import packages
from tkinter import filedialog
from tkinter import *
import csv 
import cmath

def readFile():
    """
    Reads in CSV file containing manually evaluated samples using tkinter GUI
            
    Returns: 
        Dataset containing sampled crawler evaluations
    """
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files",".csv"),("all files","*.*")))
    
    with open(root.filename, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter = ",")
        data = list(reader)
        
    root.destroy() # close the file picker 
    return data
        
def calcRelevant(listInput, roundMark):
    """
    Calculates the relevant number of pages from a user specified sample, assuming
    the "Yes/No" evaluation selection is in the 7th column, and adds these results to the 
    evaluation array
    
    Args: 
        listInput: Dataset containing random crawler evaluations by round
        roundMark: the round of the current crawler to be evaluated 
    """
    successNum = 0
    for row in range(0,len(listInput)):
        if listInput[row][6] == 'Yes':
            successNum = successNum + 1
            
    p = successNum/len(listInput) # percentage of relevant webpages
    
    # calculate the margin of error for evaluation calculation
    z_score = 1.96 # 95% desired confidence interval
    confidenceInterval = (z_score*cmath.sqrt((p*(1-p))/(len(listInput)))).real
    lowerBound = p - confidenceInterval
    upperBound = p + confidenceInterval
    
    results = "Round " + str(roundMark) + " is around " + str(p * 100) + "% accurate with a confidence interval of (" + str(lowerBound) + ", " + str(upperBound) + ")"
    evaluationArray.append(results) # append results to array which will be printed to text file
    
def writeEvaluation(evalArr):
    """
    Writes the results of the crawler evaluation to text file
    
    Args:
        evalArr: array containing results of crawler evaluation per round
    """
    # make sure there is a blank "results.txt" file in working directory to save to!
    with open('results.txt', mode='wt', encoding='utf-8') as outFile:
        for lines in evalArr:
            outFile.write(lines)
            outFile.write('\n')

data = readFile() # read in the CSV file data
evaluationArray = [] #holds crawler evaluation results per round

rowMarker = 0
roundMarker = 2
while True:    
    roundList = []
    while (data[rowMarker][5] == data[rowMarker + 1][5]):
        roundList.append(data[rowMarker][:])
        rowMarker+=1
        if(rowMarker == len(data)-1):
            break
    roundList.append(data[rowMarker][:]) # takes care of appending final round value
    
    calcRelevant(roundList, roundMarker) # calcuate percentage for round and add to list to write
    
    if rowMarker == len(data) - 1:
        break
    roundMarker += 1
    rowMarker+=1
    
writeEvaluation(evaluationArray)