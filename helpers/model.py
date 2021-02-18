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
        
        self.factor = 100
        self.filereduction = 1000.
        self.readtimes = []
        self.writetimes = []
        self.readspeedhistory = []
        self.writespeedhistory = []
        self.dischistory = []
        self.ltime = []
        self.currentreadlist = []
        self.currentwritelist = []
        self.databasereaddurations = []
        self.databasewritedurations = []
        self.modelreaddurations = []
        self.modelwritedurations = []
        self.usedjobs = []
        self.startreadjobs = []
        self.startwritejobs = []
        self.endreadjobs = []
        self.endwritejobs = []
        
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
        #100 default
        #86400 default
        t = 86400
        
        for i in range(t*self.factor):
            #print(i)
            if i%500 == 0:
                self.goSave()
                
            if i%100 == 0:
                print(i)
                print(len(self.storage.currenttraffic))
            '''print('new',self.storage.currenttraffic)
            for disc in self.storage.discs:
                print(disc.activejobs)'''
            self.ltime.append(i)
            self.splitCurrent()
            for disc in self.storage.discs:
                if disc.memo.flushing == True:
                    disc.flushing.append(1)
                else:
                    disc.flushing.append(0)
            
            newjob.futureJob(self,i)
            endreadcounter = 0
            endwritecounter = 0
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                ajob.time.append(i)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    
                    if ajob.thetype == 'read':
                        endreadcounter += 1
                        self.modelreaddurations.append(ajob.time[-1]-ajob.time[0])
                        self.readspeedhistory.append(ajob.speedhistory)
                        self.readtimes.append(ajob.time)
                    elif ajob.thetype == 'write':
                        endwritecounter += 1
                        self.modelwritedurations.append(ajob.time[-1]-ajob.time[0])
                        self.writespeedhistory.append(ajob.speedhistory)
                        self.writetimes.append(ajob.time)
                    #print('at least something ends')
                    self.dischistory.append(ajob.disc)
                    print('this never happens')
                    self.storage.futurelist[ajob.id]['modelduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
            self.endreadjobs.append(endreadcounter)
            self.endwritejobs.append(endwritecounter)
                
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
        while(len(self.storage.currenttraffic)>0):
            print(t)
            if t%500 == 0:
                self.goSave()
                
            if t%100 == 0:
                print('traffic',len(self.storage.currenttraffic))
            if t>100000*self.factor:
                print('yeah, it went there')
                break
            self.ltime.append(t)
            self.splitCurrent()
            self.currentlist.append(len(self.storage.currenttraffic))
            for disc in self.storage.discs:
                if disc.memo.flushing == True:
                    disc.flushing.append(1)
                else:
                    disc.flushing.append(0)
            endreadcounter = 0
            endwritecounter = 0
            for ajob in self.storage.currenttraffic:
                ajob.Continue()
                ajob.time.append(t)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    if ajob.thetype == 'read':
                        endreadcounter += 1
                        self.modelreaddurations.append(ajob.time[-1]-ajob.time[0])
                        self.readspeedhistory.append(ajob.speedhistory)
                        self.readtimes.append(ajob.time)
                    elif ajob.thetype == 'write':
                        endwritecounter += 1
                        self.modelwritedurations.append(ajob.time[-1]-ajob.time[0])
                        self.writespeedhistory.append(ajob.speedhistory)
                        self.writetimes.append(ajob.time)
                    #print('at least something ends')
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.dischistory.append(ajob.disc)
                    #print('maar hier kom ik toch wel')
                    
                    
                    self.storage.futurelist[ajob.id]['modelduration'] = ajob.time[-1]-ajob.time[0]
                    self.usedjobs.append(self.storage.futurelist[ajob.id])
            self.endreadjobs.append(endreadcounter)
            self.endwritejobs.append(endwritecounter)
            for disc in self.storage.discs:
                
                disc.memo.flushCheck(self.storage.currenttraffic)
                
            t += 1
        print('whats left',len(self.storage.currenttraffic))
        #print("currentcounter", currentcounter)
        
        self.goSave()
        
    def splitCurrent(self):
        
        readcounter = 0
        writecounter = 0
        
        for checkjob in self.storage.currenttraffic:
            if checkjob.thetype == 'read':
                readcounter += 1
            elif checkjob.thetype =='write':
                writecounter += 1
        
        self.currentreadlist.append(readcounter)
        self.currentwritelist.append(writecounter)
        
            
    def goSave(self):
        
        savedata.writeData(self.ltime, 'ltime')
        savedata.writeData(self.currentreadlist, 'currentreadlist')
        savedata.writeData(self.currentwritelist, 'currentwritelist')
        savedata.writeData(self.startreadjobs, 'startreadjobs')
        savedata.writeData(self.startwritejobs, 'startwritejobs')
        savedata.writeData(self.endreadjobs, 'endreadjobs')
        savedata.writeData(self.endwritejobs, 'endwritejobs')
        savedata.writeData(self.modelreaddurations, 'durations')
        savedata.writeData(self.modelwritedurations, 'durations')
        savedata.writeData(self.databasereaddurations, 'durations')
        savedata.writeData(self.databasewritedurations, 'useddurations')
        #print(self.usedjobs)
        
        if len(self.usedjobs)>0:
            print(self.usedjobs[0])
        
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
        
        savedata.writeCsv(self.readtimes, 'readtimes')
        savedata.writeCsv(self.writetimes,'writetimes')
        savedata.writeCsv(self.readspeedhistory, 'readspeedhistory')
        savedata.writeCsv(self.writespeedhistory, 'writespeedhistory')
        
        filledhistory = []
        flushhistory = []
        memoryreadhistory = []
        
        for i in range(len(self.storage.discs)):
            filledhistory.append(self.storage.discs[i].memo.filledhistory)
            flushhistory.append(self.storage.discs[i].memo.flushhistory)
            memoryreadhistory.append(self.storage.discs[i].memo.readhistory)
            
        savedata.writeCsv(filledhistory, 'filledhistory')
        savedata.writeCsv(flushhistory, 'flushhistory')
        savedata.writeCsv(memoryreadhistory, 'memoryreadhistory')
    
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")
            
    def futureSetup(self):
        
        futurelist= retrieve.getJobs(self.factor, self.filereduction)
        
        disclist = retrieve.getDiscs(futurelist)
        self.ndiscs = len(disclist)
        self.ndoors = 4
        
        self.storage = storage.Storage(self.ndiscs,self.ndoors)
        self.storage.futurelist = futurelist
        
        print(len(futurelist))
        curious = 0
        
        for i in range(len(self.storage.discs)):
            
            thedisc = self.storage.discs[i]
            
            thedisc.name = disclist[i]
            thedisc.memo.flushhistory.append(thedisc.name)
            thedisc.memo.filledhistory.append(thedisc.name)
            thedisc.memo.readhistory.append(thedisc.name)
            
            for futurejob in futurelist:
                if futurejob['domain'] == thedisc.name:
                    futurejob['disc'] = futurejob['domain']
                    futurejob['domain'] = self.storage.discs[i]
                    curious += 1
                    
        print(curious)