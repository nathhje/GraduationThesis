# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker
"""

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        
    def getPool(self,size,file):
        thePool = choices.mostSpace(self.storage,size,file)
        
        sharedspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool:
                sharedspeed.append(job)
                
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        for job in sharedspeed:
            job.speed = newspeed
                
        return thePool, newspeed
    
    def locatePool(self,file):
        thePool = 0
        
        for pool in self.storage.pools:
            if file in pool.files:
                thePool = pool
        print(thePool)
        sharedspeed = []
        loadspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool:
                sharedspeed.append(job)
                if job.thetype == 'read':
                    loadspeed.append(job)
                
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        newload = thePool.memo.flushspeed / (len(loadspeed)+1)
        if thePool.memo.flushing == True:
             newload = newload / 2
            
        for job in sharedspeed:
            job.speed = newspeed
            
        for job in loadspeed:
            job.loadspeed = newload
                
        return thePool, newspeed, newload
    
    def deletePool(self, file):
        
        self.storage.files.remove(file)
        
        thePool = 0
        
        for pool in self.storage.pools:
            if file in pool.files:
                thePool = pool
                
        return thePool
    
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
        
        self.storage.currenttraffic.remove(job)
        
        sharedspeed = []
        
        for ajob in self.storage.currenttraffic:
            if ajob.pool == job.pool:
                sharedspeed.append(job)
                
        newspeed = job.pool.bandwith / (len(sharedspeed)+1)
        for job in sharedspeed:
            job.speed = newspeed
            
            