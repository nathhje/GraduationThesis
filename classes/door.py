# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker

The door class handles the communication in the model. For each new job it looks
up where the file can be stored/retrieved from and it changes the loading speed
of all jobs if new jobs come up or old jobs close.
"""

import random

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        self.poolcounter = []
        self.everyspeed = []
        
    def getPool(self,size,file):
        thePool = choices.randomChoice(self.storage,size,file)
        
        sharedspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool and job.thetype != 'delete':
                sharedspeed.append(job)
        
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        
        for job in sharedspeed:
            job.speed = newspeed
    
        self.poolcounter.append(thePool)
        return thePool, newspeed
    
    def locatePool(self):
        thePool = random.choice(self.storage.pools)
        theFile = random.choice(thePool.files)
                
        sharedspeed = []
        loadspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool and job.thetype != 'delete':
                sharedspeed.append(job)
                if job.thetype == 'read':
                    loadspeed.append(job)
        
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        newload = thePool.memo.flushspeed / (len(loadspeed)+1)
        if thePool.memo.flushing == True:
             newload = newload / 2
        
        for job in sharedspeed:
            job.speed = newspeed
            
        for job in loadspeed:
            job.loadspeed = newload
        
        self.poolcounter.append(thePool)
        return theFile, thePool, newspeed, newload
    
    def deletePool(self):
        
        thePool = random.choice(self.storage.pools)
        file = random.choice(thePool.files)
        
        self.storage.files.remove(file)
        self.poolcounter.append(thePool)
        return file, thePool
    
    def checkDelete(self, pool):
        
        traffic = []
        
        for job in self.storage.currenttraffic:
            if job.pool == pool:
                traffic.append(job)
                
        if len(traffic) > 2:
            return False
        else:
            return True
        
    
    def closeJob(self,job):
        
        self.poolcounter.remove(job.pool)
        self.storage.currenttraffic.remove(job)
        sharedspeed = []
        
        for ajob in self.storage.currenttraffic:
            if ajob.pool == job.pool:
                sharedspeed.append(ajob)
        
        if len(sharedspeed) > 0 and job.thetype != 'delete':
            newspeed = job.pool.bandwith / len(sharedspeed)
            self.everyspeed.append(newspeed)
            
            for job in sharedspeed:
                job.speed = newspeed