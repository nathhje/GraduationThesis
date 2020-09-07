# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:17:45 2020

@author: Gebruiker
"""

import random

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
        
        self.setup()
    
    def setup(self):
        
        for i in range(random.randint(10,100)):
            size = random.random()/100.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        defile = file.File(size)
        choices.mostSpace(self.storage,size,defile)
        
    
    def run(self):
        
        for i in range(1000):
            if random.random() < 0.1:
                thedoor = random.choice(self.storage.doors)
                thetype = self.action()
                
                thejob = job.Job(thedoor,thetype)
                self.storage.currenttraffic.append(thejob)
            #print(self.storage.pools[0].filled)
            #print(self.storage.filled)
            
            for ajob in self.storage.currenttraffic:
                print(ajob.thetype)
                print('complete',ajob.complete)
                print('size', ajob.size)
                ajob.Continue()
                
            for pool in self.storage.pools:
                
                pool.memo.flushCheck(self.storage.currenttraffic)
                
        while(len(self.storage.currenttraffic)>0):
            for ajob in self.storage.currenttraffic:
                print(ajob.thetype)
                print('complete',ajob.complete)
                print('size', ajob.size)
                ajob.Continue()
                
            for pool in self.storage.pools:
                
                pool.memo.flushCheck(self.storage.currenttraffic)
            
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")