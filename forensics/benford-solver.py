# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:20:10 2020

@author: pleoxconfusa
"""
import csv
import os
from scipy.stats import chisquare

numbers = ["0","1","2","3","4","5","6","7","8","9"]

benford = [0, 0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
bfsecnd = [0.12, 0.114, 0.109, 0.104, 0.1, 0.097, 0.093, 0.09, 0.088, 0.085]
bfthird = [0.102, 0.101, 0.101, 0.101, 0.1, 0.1, 0.099, 0.099, 0.099, 0.098]


randdist = [0, 1.0/9, 1.0/9, 1.0/9, 1.0/9, 1.0/9, 1.0/9, 1.0/9, 1.0/9, 1.0/9]
randoter = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

bfall = [benford, bfsecnd, bfthird]
randl = [randdist, randoter]

challenge_folder = "Benford"




def check_finances(folder, file, distribution):
    
    chi_val = 1
    values = []
    for i in range(0,len(bfall)):
        values.append([0,0,0,0,0,0,0,0,0,0])
    with open(folder + "/" + file, 'r', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        row_count = 0.0
        
        for row in reader:
            if row and len(row)-1:
                row_count += 1.0
                values[0][int(row[1][1])] += 1.0
                values[1][int(row[1][2])] += 1.0
                values[2][int(row[1][3])] += 1.0
        
        valuesdistro = [item for sublist in values for item in sublist]
                
        chi_val = chisquare(valuesdistro[1:19:], [row_count*x for x in distribution][1:19:]).pvalue
        
        print(chi_val)
        
    return chi_val


if __name__=="__main__":
    chi_value = 1
    answer = ""
    
    bfalldistro = [item for sublist in bfall for item in sublist]
    
    for filename in os.listdir(challenge_folder):
        if ".csv" in filename:
            chi = check_finances(challenge_folder, filename, bfalldistro)
            if chi < chi_value:
                chi_value = chi
                answer = filename
               
    print(chi_value)
    print(answer)
            