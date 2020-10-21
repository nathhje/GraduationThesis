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

class Model:
    
    def __init__(self):
        
        
        self.speedhistory = []
        self.times = []
        self.dischistory = []
        self.ltime = []
        self.currentlist = []
        
        self.futureSetup()
    
    def randomSetup(self):
        
        self.ndiscs = 4
        self.ndoors = 4
        
        self.storage = storage.Storage(self.ndiscs,self.ndoors)
        
        for i in range(random.randint(10,100)):
            size = random.random()*100.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        defile = file.File(size)
        choices.randomChoice(self.storage,size,defile)
        
    
    def run(self):
        
        #currentcounter =0
        
        t = 100000
        
        for i in range(t):
            print(i)
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
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
        while(len(self.storage.currenttraffic)>0):
            print(t)
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
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
            t += 1
        #print("currentcounter", currentcounter)
        self.graphs()
        self.flushgraph()
        
        for door in self.storage.doors:
            print(door.everyspeed)
            
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")
            
    def graphs(self):
        print('graph start',len(self.dischistory))
        counter = 0
        
        for disc in self.storage.discs:
        
            plt.figure()
            for i in range(len(self.times)):
                if self.dischistory[i] == disc:
                    counter +=1
                    plt.plot(self.times[i],self.speedhistory[i])
            plt.show()
            print(counter)
            plt.figure()
            plt.plot(self.ltime,disc.flushing)
            plt.show()
            
        plt.figure()
        plt.plot(self.ltime,self.currentlist)
        plt.show()
        
    def flushgraph(self):
        
        for disc in self.storage.discs:
            
            plt.figure()
            plt.plot(self.ltime,disc.memo.flushhistory)
            plt.show()
            
    def futureSetup(self):
        
        futurelist = retrieve.getJobs()
        
        disclist = retrieve.getDiscs(futurelist)
        self.ndiscs = len(disclist)
        self.ndoors = 4
        
        self.storage = storage.Storage(self.ndiscs,self.ndoors)
        self.storage.futurelist = futurelist
        
        for i in range(len(self.storage.discs)):
            
            self.storage.discs[i].name = disclist[i]