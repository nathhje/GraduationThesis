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
        self.startjobs = []
        self.endjobs = []
        
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
        
        t = 80
        
        for i in range(t):
            #print(i)
            if i%5000 == 0:
                self.goSave()
                
            if i%1 == 0:
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
            endcounter = 0
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                print('progress',ajob.size,ajob.complete,ajob.speed)
                ajob.time.append(i)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    endcounter+= 1
                    #print('at least something ends')
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    
                    self.storage.futurelist[ajob.id]['actualduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
            self.endjobs.append(endcounter)
                
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
        while(len(self.storage.currenttraffic)>0):
            print(t)
            if t%5000 == 0:
                self.goSave()
                
            if t%100 == 0:
                print('traffic',len(self.storage.currenttraffic))
            if t>35000:
                print('yeah, it went there')
                break
            self.ltime.append(t)
            self.currentlist.append(len(self.storage.currenttraffic))
            for disc in self.storage.discs:
                if disc.memo.flushing == True:
                    disc.flushing.append(1)
                else:
                    disc.flushing.append(0)
            endcounter = 0
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                ajob.time.append(t)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    endcounter += 1
                    #print('at least something ends')
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    #print('maar hier kom ik toch wel')
                    self.durations.append(ajob.time[-1]-ajob.time[0])
                    
                    self.storage.futurelist[ajob.id]['actualduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
            self.endjobs.append(endcounter)
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
            t += 1
        print('whats left',len(self.storage.currenttraffic))
        #print("currentcounter", currentcounter)
        
        self.goSave()
            
            
    def goSave(self):
        
        savedata.writeData(self.ltime, 'ltime')
        savedata.writeData(self.currentlist, 'currentlist')
        savedata.writeData(self.startjobs, 'startjobs')
        savedata.writeData(self.endjobs, 'endjobs')
        savedata.writeData(self.durations, 'durations')
        savedata.writeData(self.useddurations, 'useddurations')
        #print(self.usedjobs)
        
        for usedjob in self.usedjobs:
            if 'domain' in usedjob:
                del usedjob['domain']
        data = {}
        data['jobs'] = self.usedjobs
        savedata.writeJson(data, 'usedjobs')
        
        actives = {}
        actives['jobs'] = []
        
        for activejob in self.storage.currenttraffic:
            savejob = activejob.sourcejob
            savejob['complete'] = activejob.complete
            savejob['inmemory'] = activejob.inmemory
            savejob.pop('domain',None)
            actives['jobs'].append(savejob)
        print(actives)
        savedata.writeJson(actives, 'currenttraffic')
        
        savedata.writeCsv(self.times, 'times')
        
        flushhistory = []
        
        for i in range(len(self.storage.discs)):
            flushhistory.append(self.storage.discs[i].memo.flushhistory)
            
        savedata.writeCsv(flushhistory, 'flushhistory')
    
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")
            
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