# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:51:06 2020

@author: Gebruiker
"""

import json

date = '04.15.json'

def getJobs():
    
    file = open('data/importanttransfers2020.' + date,'r')
    
    transfers = json.load(file)['jobs']
    
    for job in transfers:
        
        stamp = job['timestamp']
        hour = int(stamp[11:13])
        minute = int(stamp[14:16])
        second= float(stamp[17:23])
        
        time = hour * 3600 + minute * 60 + second
        job['time'] = time
    
    return transfers

def getDiscs(joblist):
    
    poollist = []
    
    for job in joblist:
        if (job['domain'] in poollist) == False:
            poollist.append(job['domain'])
            
            
    return poollist