# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:14:15 2020

@author: Gebruiker

If the previous flush is still busy when the next flush is started,
the first flush is overwritten. Not a worry for right now, but definitely a
malfunction.
"""

class Memory():
    
    def __init__(self, pool):
        self.pool = pool
        self.space = 1000.
        self.buffer = 500.
        self.filled = 0.
        self.flushing = False
        self.flushed = 0.
        self.flushspeed = 5.
        self.readused = 0.
        self.flushhistory = []
        
        
    def flushCheck(self, jobs):
        self.flushhistory.append(self.flushed)
        sharedspeed = []
        
        for job in jobs:
            if job.thetype == 'read' and job.pool == self.pool:
                sharedspeed.append(job)
        #print(self.filled)
        if self.filled > self.buffer:
            self.flushing = True
            self.flushed += self.filled
            #print(self.filled)
            self.filled = 0.
            for job in sharedspeed:
                job.loadspeed = job.loadspeed / 2
        #print(self.flushed)
        if self.flushing == True:
            #print('true')
            #print(self.flushed)
            if len(sharedspeed) == 0:
                self.flushed -= self.flushspeed
            else:
                self.flushed -= (self.flushspeed/2)
            #print(self.flushed)
            if self.flushed <= 0:
                self.flushed = 0.
                self.flushing = False
                #print('logisch')
                for job in sharedspeed:
                    job.loadspeed = job.loadspeed * 2
                
                
                