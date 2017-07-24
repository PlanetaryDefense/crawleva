# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:53:18 2017

@author: larakamal
"""

from math import ceil
import pandas as pd
import csv

#a function that returns sample size
def get_sample_size(n, confidence_level, margin_of_error, population_proportion):
    z = get_z(confidence_level)
    x = ((z**2)* population_proportion * (1-population_proportion))/(margin_of_error**2)
    true_sample = ceil((x*n)/((x+n -1)))
    return true_sample

#get z-scores from the confidence level        
def get_z(confidence_level):
    if confidence_level == 0.90:
        return 1.645
    elif confidence_level == 0.95:
        return 1.96
    elif confidence_level == 0.98:
        return 2.33
    elif confidence_level == 0.99:
        return 2.576
    else:
        return 0    

    
#chose confidence interval of 95%, standard confidence interval in statistics 
confidence_level = 0.90
#standard margin of error in statistics is somewhere between 4%-8%
margin_of_error = 0.08
#number of webpages extracted by the crawler in every iteration 
n = 256 #1-256
#calculated populatin proportion based on previous data such as: # of success in population/total population 
population_proportion = 0.8259
#find an appropriate sample size 
x = get_sample_size(n, confidence_level, margin_of_error, population_proportion)
#print("sample size ", x)
