# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:15:51 2021

@author: Gebruiker
"""

import json
import math
import matplotlib.pyplot as plt

date = '07.19.json'

def getJobs():
    
    # centiseconds
    factor = 100
    secondsperday = 86400
    
    file = open('data/importanttransfers2020.' + date,'r')
    
    transfers = json.load(file)['jobs']
    counter = 0
    joblist = []
    
    file.close()
    
    for i in range(0,len(transfers),1):
        
        '''if i %1000 == 0:
            print(i,'eerste')'''
        job = transfers[i]
        job['id'] = counter
        stamp = job['timestamp']
        hour = int(stamp[11:13])
        minute = int(stamp[14:16])
        second= float(stamp[17:23])
        
        if i < 30:
            print(stamp)
        
        time = (hour * 3600 + minute * 60 + second)*factor
        job['time'] = time
        counter += 1
        
        joblist.append(job)
        
    timelist = [i/factor for i in range(factor*secondsperday)]
    completetimelist = [i/factor for i in range(0,factor*secondsperday,10000)]
    print(len(completetimelist))
    print(completetimelist[0:30])
    
    activelist = [0 for i in range(factor*secondsperday)]
    readactive = [0 for i in range(factor*secondsperday)]
    writeactive = [0 for i in range(factor*secondsperday)]
    completelist = [0 for i in range(0,factor*secondsperday,10000)]
    counter = 0
    
    readcounter = 0
    writecounter = 0
    
    
    for job in joblist:
        
        if counter %1000 == 0:
            print(counter,'tweede')
            
        counter += 1
        
        starttime = math.floor(job['time']-job['duration']*factor/1000)
        
        if starttime < 0:
            starttime = 0
        
        endtime = math.floor(job['time'])
        completeendtime = math.floor(job['time']/10000)
        #print(job['time'])
        #print(completeendtime)
        completelist[completeendtime] += 1
        
        if job['isWrite'] == 'write':
            writecounter += 1
            for i in range(starttime,endtime+1):
            
                activelist[i] += 1
                writeactive[i] += 1
                
        elif job['isWrite'] == 'read':
            readcounter += 1
            for i in range(starttime,endtime+1):
            
                activelist[i] += 1
                readactive[i] += 1
                
        else:
            print('incorrect something')
                
            
    plt.figure()
    plt.plot(timelist,activelist)
    plt.xlabel('time (s)')
    plt.title('number of jobs active each timestep')
    plt.show()
    
    plt.figure()
    plt.plot(timelist,writeactive)
    plt.xlabel('time (s)')
    plt.title('number of write jobs active each timestep')
    plt.show()
    
    plt.figure()
    plt.plot(timelist,readactive)
    plt.xlabel('time (s)')
    plt.title('number of read jobs active each timestep')
    plt.show()
    
    plt.figure()
    plt.plot(completetimelist,completelist)
    plt.xlabel('time (s)')
    plt.title('number of jobs completed each timestep')
    plt.show()
    
    print('write counter', writecounter)
    print('read counter', readcounter)
        
if __name__ == '__main__':
    getJobs()