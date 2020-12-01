# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:54:31 2020

@author: Gebruiker
"""
import matplotlib.pyplot as plt
import numpy as np
import csv
import json

titlebase = 'firstrun2-23/02-23t20000u1in10b10000d1000buff5000000'

def readData(file):
    
    data = []
    
    with open(file,'r',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=',', quotechar='"')
        for row in reader:
            floats= []
            
            for item in row:
                floats.append(float(item))
            data.append(floats)
            
    if len(data) == 1:
        return data[0]
    else:
        return data
    
def readJson(file):
    
    with open(file,'r') as jsonfile:
        jason = json.load(jsonfile)
        
    return jason['jobs']

def durationgraph(durations):
    print('wut')
    plt.figure()
    plt.hist(durations)
    plt.title('Histogram of the duration of each job in the database')
    plt.xlabel('duration (s)')
    plt.show()
    print('am I')
    plt.figure()
    plt.hist(durations, bins = range(0,10000,10))
    plt.title('Histogram of the duration of each job in the database')
    plt.xlabel('duration (s)')
    plt.show()
    print('witnessing')
    plt.figure()
    plt.hist(durations, bins = range(0,100000,100))
    plt.title('Histogram of the duration of each job in the database')
    plt.xlabel('duration (s)')
    plt.show()
    print('now')
    
    
def durationcompare(usedjobs):
    print('wnat hier blijkbaar niet',len(usedjobs))
    '''for ajob in usedjobs:
        print('next duration')
        print(ajob['duration'])
        print(ajob['actualduration'])
        print(ajob['size'])'''
        
    differences = []
    fractions = []
    indatabase = []
    inmodel = []
    
    for ajob in usedjobs:
        indatabase.append(ajob['duration'])
        inmodel.append(ajob['actualduration'])
        differences.append(ajob['duration']-ajob['actualduration'])
        
        if ajob['duration'] != 0:
            fractions.append((ajob['duration']-ajob['actualduration'])/ajob['duration'])
    
    plt.figure()
    plt.hist(indatabase, bins = range(0,2500,10))
    plt.title('Histogram of the duration of each job in the database')
    plt.xlabel('duration (s)')
    plt.show()
    
    plt.figure()
    plt.hist(inmodel, bins = range(0,2500,10))
    plt.title('Histogram of the duration of each job in the model')
    plt.xlabel('duration (s)')
    plt.show()
    
    plt.figure()
    plt.hist(differences)
    plt.xscale('log')
    plt.title('Histogram of difference between duration in the model \n and in the database for each job')
    plt.xlabel('duration difference')
    plt.show()
    
    plt.figure()
    plt.hist(differences, bins = range(0,1000,1))
    plt.xscale('log')
    plt.title('Histogram of difference between duration in the model \n and in the database for each job')
    plt.xlabel('duration difference')
    plt.show()
    
    plt.figure()
    plt.hist(fractions, bins = np.arange(-5,3,0.1))
    plt.title('Histogram of difference between duration in the model \n and in the database for each job \n as a fraction of the duration in the database')
    plt.xlabel('fraction')
    plt.show()
    #print(fractions)
            
def lengthhist(times, useddurations):
        
    difference = []
    xlist = []
    
    step = 1
    
    for i in np.arange(0,30,step):
        
        k=0
        l=0
        
        for atime in times:
            if i<atime[-1]-atime[0]<(i+step):
                k += 1
                
        for adur in useddurations:
            if i<adur<(i+step):
                l+= 1
        
        print('k',k)
        print('l',l)
        difference.append(k-l)
        xlist.append(i)
        
    plt.figure()
    plt.plot(xlist,difference)
    plt.xlabel('length (s)')
    plt.ylabel('difference')
    plt.title('Difference between the number of jobs taking x amount in the model and in the database')
    plt.show()
    
    lengthlist = []
    
    for atime in times:
        if atime[-1]-atime[0]<100000:
            lengthlist.append(atime[-1]-atime[0])
        
    plt.figure()
    plt.hist(lengthlist, bins = range(0,20000,10))
    plt.title('Histogram of the duration of each finished job')
    plt.xlabel('duration (s)')
    plt.ylim(0,100)
    plt.plot()
    
    plt.figure()
    plt.hist(lengthlist, bins = range(0,20000,10))
    plt.title('Histogram of the duration of each finished job')
    plt.xlabel('duration (s)')
    plt.ylim(0,1000)
    plt.plot()
    
    print('length lengthlist',len(lengthlist))
    
def graphs(ltime, currentlist):
    '''
    plt.figure()
    for disc in self.storage.discs:
    
        
        for i in range(len(self.times)):
            if self.dischistory[i] == disc:
                counter +=1
                print(counter)
                plt.plot(self.times[i],self.speedhistory[i])
    plt.show()
    '''
    '''print(counter)
    plt.figure()
    plt.plot(self.ltime,disc.flushing)
    plt.show()'''
    
    plt.figure()
    plt.plot(ltime,currentlist)
    plt.title('The number of jobs active at any given time')
    plt.xlabel('time (s)')
    plt.ylabel('number of jobs')
    plt.show()
        
def flushgraph(ltime,flushhistory):
    counter = 0
    plt.figure()
    for i in range(len(flushhistory)):
        counter += 1
        
        plt.plot(ltime,flushhistory[i])
    
    plt.title('The current amount of data being flushed on each disc')
    plt.xlabel('time (s)')
    plt.ylabel('data size')
    plt.show()
    print('should be number of discs either way', counter)
    

thecurrentlist = readData(titlebase+'currentlist.txt')
print('these')
thedurations = readData(titlebase+'durations.txt')
print('are')
theflushhistory = readData(titlebase+'flushhistory.txt')
print('quite')
theltime = readData(titlebase+'ltime.txt')
print('a')
thetimes = readData(titlebase+'times.txt')
print('few')
theuseddurations = readData(titlebase+'useddurations.txt')
print('lists')
theusedjobs = readJson(titlebase+'usedjobs.txt')
print('to load')
#print(thedurations)
print(len(thedurations))
durationgraph(thedurations)
print('something else')
durationcompare(theusedjobs)
lengthhist(thetimes,theuseddurations)
graphs(theltime,thecurrentlist)
flushgraph(theltime,theflushhistory)