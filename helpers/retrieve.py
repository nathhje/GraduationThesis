# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:51:06 2020

@author: Gebruiker
"""

import json

date = '07.19.json'

def getJobs(factor, filereduction):
    
    file = open('data/importanttransfers2020.' + date,'r')
    
    transfers = json.load(file)['jobs']
    actualjobs = []
    #databasedurations = []
    highest = 0
    counter = 0
    
    file.close()
    
    for i in range(0,len(transfers),1):
        
        job = transfers[i]
        job['id'] = counter
        stamp = job['timestamp']
        hour = int(stamp[11:13])
        minute = int(stamp[14:16])
        second= float(stamp[17:23])
        job['size'] = job['size'] / filereduction
        job['databaseduration'] = job['duration']/ 1000. * factor
        
        endtime = hour * 3600 + minute * 60 + second
        job['endtime'] = endtime*factor
        job['time'] = endtime*factor - job['databaseduration']
        
        if highest < endtime:
            highest = endtime
        actualjobs.append(job)
        
        #databasedurations.append(job['databaseduration'])
        counter += 1
    print('highest',highest)
    return actualjobs#, databasedurations

def getDiscs(joblist):
    
    poollist = []
    
    for job in joblist:
        if (job['domain'] in poollist) == False:
            poollist.append(job['domain'])
            
            
    return poollist