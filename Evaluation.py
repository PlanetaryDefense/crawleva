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
    p_array.append(p)
    
    # calculate the margin of error for evaluation calculation
    z_score = 1.96 # 95% desired confidence interval
    n = len(listInput) # total sample size
    
    lowerBound = (2*n*p+(z_score**2)-z_score*cmath.sqrt((z_score**2)-(1/n)+4*n*p*(1-p)+(4*p-2)).real+1) /(2*(n+z_score**2))
    upperBound = (2*n*p+(z_score**2)+z_score*cmath.sqrt((z_score**2)-(1/n)+4*n*p*(1-p)-(4*p-2)).real+1) /(2*(n+z_score**2))
    results = [str(roundMark), str(p * 100),str(lowerBound*100), str(upperBound*100), n]
    
    evaluationArray.append(results) # append results to array which will be printed to text file
    
def writeEvaluation(evalArr):
    """
    Writes the results of the crawler evaluation to CSV file in this order:
    Round Number, P-Value, Lower Bound, Upper Bound, Sample Size for Round
    
    Args:
        evalArr: array containing results of crawler evaluation per round
    """
    with open(r'C:\JG_STC_Work\crawleva\CSVresults\output.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(evalArr)

def calcAveSuccess(p_vals):
    pTotal = 0
    for i in range(0,len(p_vals)):
        pTotal += p_vals[i]
    return pTotal

data = readFile() # read in the CSV file data
evaluationArray = [] #holds crawler evaluation results per round
p_array = []

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
pNum = calcAveSuccess(p_array)
print("The overall percent of success is: " + str((pNum/len(p_array))*100))