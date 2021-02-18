# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 08:43:12 2020

@author: Gebruiker
"""

import json
import csv

titlestart = 'savedata/test07-19t86400u1in1b100000d1000buff500000'

def writeCsv(data,titleend):
    
    with open(titlestart + titleend + '.txt','w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        
        for row in data:
            writer.writerow(row)
            
def writeData(data,titleend):
    
    with open(titlestart + titleend + '.txt','w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        
        writer.writerow(data)
        
def writeJson(data,titleend):
    
    with open(titlestart + titleend + '.txt','w') as file:
        json.dump(data,file)