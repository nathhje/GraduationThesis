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
    
    def closeJob(self,job):
        
        self.storage.currenttraffic.remove(job)
        
        sharedspeed = []
        
        for ajob in self.storage.currenttraffic:
            if ajob.pool == job.pool:
                sharedspeed.append(job)
                
        newspeed = job.pool.bandwith / (len(sharedspeed)+1)
        for job in sharedspeed:
            job.speed = newspeed
            
            