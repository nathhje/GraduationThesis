# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:51:06 2020

@author: Gebruiker
"""

import json

date = '07.19.json'

def getJobs():
    
    file = open('data/importanttransfers2020.' + date,'r')
    
    transfers = json.load(file)['jobs']
    actualjobs = []
    durations = []
    highest = 0
    counter = 0
    
    for i in range(0,len(transfers),1):
        
        job = transfers[i]
        job['id'] = counter
        stamp = job['timestamp']
        hour = int(stamp[11:13])
        minute = int(stamp[14:16])
        second= float(stamp[17:23])
        job['size'] = job['size'] / 1000.
        
        time = hour * 3600 + minute * 60 + second
        job['time'] = time
        
        if highest < time:
            highest = time
        actualjobs.append(job)
        
        durations.append(job['duration'])
        counter += 1
    print('highest',highest)
    return actualjobs, durations

def getDiscs(joblist):
    
    poollist = []
    
    for job in joblist:
        if (job['domain'] in poollist) == False:
            poollist.append(job['domain'])
            
            
    return poollist