# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker
"""

import random
import matplotlib.pyplot as plt

import classes.storage as storage
import classes.file as file
import helpers.choices as choices
import classes.job as job

class Model:
    
    def __init__(self):
        
        self.npools = 4
        self.ndoors = 4
        self.queue = []
        
        self.storage = storage.Storage(self.npools,self.ndoors)
        self.jobs = []
        self.speedhistory = []
        self.times = []
        self.poolhistory = []
        self.ltime = []
        self.currentlist = []
        
        self.setup()
    
    def setup(self):
        
        for i in range(random.randint(10,100)):
            size = random.random()*100.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        defile = file.File(size)
        choices.randomChoice(self.storage,size,defile)
        
    
    def run(self):
        
        currentcounter =0
        
        t = 1000
        
        for i in range(t):
            print(i)
            self.ltime.append(i)
            self.currentlist.append(len(self.storage.currenttraffic))
            for pool in self.storage.pools:
                if pool.memo.flushing == True:
                    pool.flushing.append(1)
                else:
                    pool.flushing.append(0)
            #print(i,len(self.storage.currenttraffic))
            '''for door in self.storage.doors:
                print(door.storage.currenttraffic)
            
            print('actual traffic',self.storage.currenttraffic)'''
            
            if random.random() < 0.3:
                
                thedoor = random.choice(self.storage.doors)
                thetype = self.action()
                #print('thetype', thetype)
                #if thetype == 'delete':
                    #print('again')
                    #for ljob in self.storage.currenttraffic:
                        #print(ljob.speed)
                
                thejob = job.Job(thedoor,thetype)
                self.storage.currenttraffic.append(thejob)
                currentcounter += 1
                thejob.time.append(i)
                thejob.speedhistory.append(thejob.speed)
                '''if thetype == 'delete':
                    print('end')
                    for ljob in self.storage.currenttraffic:
                        print(ljob.speed)'''
            #print(self.storage.pools[0].filled)
            #print(self.storage.filled)
            
            for ajob in self.storage.currenttraffic:
                '''print(ajob.thetype)
                print('complete',ajob.complete)
                print('size', ajob.size)'''
                #print('before',ajob.thetype, ajob.speed)
                ajob.Continue()
                #print('after',ajob.thetype, ajob.speed)
                ajob.time.append(i)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.poolhistory.append(ajob.pool)
                    #print(ajob.thetype,ajob.speedhistory)
                
            for pool in self.storage.pools:
                
                pool.memo.flushCheck(self.storage.currenttraffic)
            
            #print('traffic', len(self.storage.currenttraffic))
                
        while(len(self.storage.currenttraffic)>0):
            print(t)
            self.ltime.append(t)
            self.currentlist.append(len(self.storage.currenttraffic))
            for pool in self.storage.pools:
                if pool.memo.flushing == True:
                    pool.flushing.append(1)
                else:
                    pool.flushing.append(0)
            #print(t,len(self.storage.currenttraffic))
            '''for door in self.storage.doors:
                print(door.storage.currenttraffic)
            
            print('actual traffic',self.storage.currenttraffic)'''
            #print('traffic', len(self.storage.currenttraffic))
            for ajob in self.storage.currenttraffic:
                #print('speeds', ajob.speed)
                #print('pool', ajob.pool)
                '''print(ajob.thetype)
                print('complete',ajob.complete)
                print('size', ajob.size)'''
                ajob.Continue()
                ajob.time.append(t)
                ajob.speedhistory.append(ajob.speed)
                if ajob.ended == True:
                    self.speedhistory.append(ajob.speedhistory)
                    self.times.append(ajob.time)
                    self.poolhistory.append(ajob.pool)
                    #print(ajob.thetype,ajob.speedhistory)
                
            for pool in self.storage.pools:
                
                pool.memo.flushCheck(self.storage.currenttraffic)
                
            t += 1
        print("currentcounter", currentcounter)
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
        print('graph start',len(self.poolhistory))
        counter = 0
        
        for pool in self.storage.pools:
        
            plt.figure()
            for i in range(len(self.times)):
                if self.poolhistory[i] == pool:
                    counter +=1
                    #print(self.speedhistory[i])
                    plt.plot(self.times[i],self.speedhistory[i])
                    #plt.xlim(600,1000)
                #plt.show()
                #plt.figure()
            plt.show()
            print(counter)
            plt.figure()
            plt.plot(self.ltime,pool.flushing)
            plt.show()
            
        plt.figure()
        plt.plot(self.ltime,self.currentlist)
        plt.show()
        
    def flushgraph(self):
        
        for pool in self.storage.pools:
            
            plt.figure()
            plt.plot(self.ltime,pool.memo.flushhistory)
            plt.show()