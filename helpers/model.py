# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker

This file contains the core of the model. The storage is created and filled
with files. Then a time loop is started where in each time step, a check is
done and if passed, a new job is created. After this, all open jobs make
progress and they are closed if finished. Each time step ends with making a 
check if the data in the memory has to be flushed to disc.
Also contains the graphs.
"""

import random
import matplotlib.pyplot as plt

import classes.storage as storage
import classes.file as file
import helpers.choices as choices
import classes.job as job
import helpers.newjob as newjob
import helpers.retrieve as retrieve
import numpy as np
import helpers.savedata as savedata

class Model:
    
    def __init__(self):
        
        
        self.speedhistory = []
        self.times = []
        self.dischistory = []
        self.ltime = []
        self.currentlist = []
        self.durations = []
        self.useddurations = []
        self.usedjobs = []
        
        self.futureSetup()
    
    def randomSetup(self):
        
        self.ndiscs = 200
        self.ndoors = 4
        
        self.storage = storage.Storage(self.ndiscs,self.ndoors)
        
        for i in range(random.randint(1000,10000)):
            size = random.random()*1000000.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        defile = file.File(size)
        choices.randomChoice(self.storage,size,defile)
        
    
    def run(self):
        
        #currentcounter =0
        
        t = 20000
        
        for i in range(t):
            #print(i)
            if i%100 == 0:
                print(i)
                print(len(self.storage.currenttraffic))
            '''print('new',self.storage.currenttraffic)
            for disc in self.storage.discs:
                print(disc.activejobs)'''
            self.ltime.append(i)
            self.currentlist.append(len(self.storage.currenttraffic))
            for disc in self.storage.discs:
                if disc.memo.flushing == True:
                    disc.flushing.append(1)
                else:
                    disc.flushing.append(0)
            
            newjob.futureJob(self,i)
            
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                ajob.time.append(i)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    #print('at least something ends')
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    
                    self.storage.futurelist[ajob.id]['actualduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
                    
                
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
        while(len(self.storage.currenttraffic)>0):
            print(t)
            if t%100 == 0:
                print('traffic',len(self.storage.currenttraffic))
            if t>30000:
                print('yeah, it went there')
                break
            self.ltime.append(t)
            self.currentlist.append(len(self.storage.currenttraffic))
            for disc in self.storage.discs:
                if disc.memo.flushing == True:
                    disc.flushing.append(1)
                else:
                    disc.flushing.append(0)
                    
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                ajob.time.append(t)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    #print('at least something ends')
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    #print('maar hier kom ik toch wel')
                    self.durations.append(ajob.time[-1]-ajob.time[0])
                    
                    self.storage.futurelist[ajob.id]['actualduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
                    
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
            t += 1
        print('whats left',len(self.storage.currenttraffic))
        #print("currentcounter", currentcounter)
        '''self.durationcompare()
        self.graphs()
        self.flushgraph()
        self.lengthhist()
        self.durationgraph()'''
        
        savedata.writeData(self.ltime, 'ltime')
        savedata.writeData(self.currentlist, 'currentlist')
        savedata.writeData(self.durations, 'durations')
        savedata.writeData(self.useddurations, 'useddurations')
        #print(self.usedjobs)
        
        for usedjob in self.usedjobs:
            del usedjob['domain']
        data = {}
        data['jobs'] = self.usedjobs
        savedata.writeJson(data, 'usedjobs')
        savedata.writeCsv(self.times, 'times')
        
        flushhistory = []
        
        for i in range(len(self.storage.discs)):
            flushhistory.append(self.storage.discs[i].memo.flushhistory)
            
        savedata.writeCsv(flushhistory, 'flushhistory')
        
        #for door in self.storage.doors:
            #print(door.everyspeed)
            
    def durationgraph(self):
        
        plt.figure()
        plt.hist(self.durations)
        plt.show()
        
        plt.figure()
        plt.hist(self.durations, bins = range(0,10000,10))
        plt.show()
        
        plt.figure()
        plt.hist(self.durations, bins = range(0,100000,100))
        plt.show()
        
        
            
    def durationcompare(self):
        print('wnat hier blijkbaar niet',len(self.usedjobs))
        for ajob in self.usedjobs:
            print('next duration')
            print(ajob['duration'])
            print(ajob['actualduration'])
            print(ajob['size'])
            
        differences = []
        fractions = []
        
        for ajob in self.usedjobs:
            differences.append(ajob['duration']-ajob['actualduration'])
            
            if ajob['duration'] != 0:
                fractions.append((ajob['duration']-ajob['actualduration'])/ajob['duration'])
            
        plt.figure()
        plt.hist(differences)
        plt.xscale('log')
        plt.show()
        
        plt.figure()
        plt.hist(differences, bins = range(0,1000,1))
        plt.xscale('log')
        plt.show()
        
        plt.figure()
        plt.hist(fractions, bins = np.arange(-5,3,0.1))
        plt.show()
        #print(fractions)
    
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")
            
    def lengthhist(self):
        
        difference = []
        xlist = []
        
        step = 1
        
        for i in np.arange(0,30,step):
            
            k=0
            l=0
            
            for atime in self.times:
                if i<atime[-1]-atime[0]<(i+step):
                    k += 1
                    
            for adur in self.useddurations:
                if i<adur<(i+step):
                    l+= 1
            
            difference.append(k-l)
            xlist.append(i)
            
        plt.figure()
        plt.plot(xlist,difference)
        plt.show()
                    
        lengthlist = []
        
        for atime in self.times:
            if atime[-1]-atime[0]<100000:
                lengthlist.append(atime[-1]-atime[0])
            
        plt.figure()
        plt.hist(lengthlist, bins = range(0,20000,10))
        plt.ylim(0,100)
        plt.plot()
        
        plt.figure()
        plt.hist(lengthlist, bins = range(0,20000,10))
        plt.ylim(0,1000)
        plt.plot()
        
        print('length lengthlist',len(lengthlist))
            
    def graphs(self):
        print('graph start',len(self.dischistory))
        counter = 0
        print(len(self.storage.discs))
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
        plt.plot(self.ltime,self.currentlist)
        plt.show()
        
    def flushgraph(self):
        counter = 0
        plt.figure()
        for disc in self.storage.discs:
            counter += 1
            
            plt.plot(self.ltime,disc.memo.flushhistory)
        
        plt.title('The current amount of data being flushed on each disc')
        plt.show()
        print('should be number of discs either way', counter)
            
    def futureSetup(self):
        
        futurelist, self.durations = retrieve.getJobs()
        
        disclist = retrieve.getDiscs(futurelist)
        self.ndiscs = len(disclist)
        self.ndoors = 4
        
        self.storage = storage.Storage(self.ndiscs,self.ndoors)
        self.storage.futurelist = futurelist
        
        print(len(futurelist))
        curious = 0
        
        for i in range(len(self.storage.discs)):
            
            self.storage.discs[i].name = disclist[i]
            
            for futurejob in futurelist:
                if futurejob['domain'] == disclist[i]:
                    futurejob['disc'] = futurejob['domain']
                    futurejob['domain'] = self.storage.discs[i]
                    curious += 1
                    
        print(curious)