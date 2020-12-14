# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:14:15 2020

@author: Gebruiker

Each disc contains a temporary memory. Files that are being written are saved
in this memory, until the buffer is filled, at which point it is flushed to disc.
Files that are being read also pass through the memory, but are send on as fast
as possible rather than when the buffer is filled. This class keeps track of
how much memory is used and checks whether flushing is happening and progresses
the flushing.
"""

class Memory():
    
    def __init__(self, disc):
        self.disc = disc
        self.space = 10000000000.
        self.buffer = 5000000.
        self.filled = 0.
        self.flushing = False
        self.flushed = 0.
        self.flushspeed = 1000000.
        self.readused = 0.
        self.flushhistory = []
        
        
    def flushCheck(self, jobs):
        self.flushhistory.append(self.flushed)
        sharedspeed = []
        
        for job in jobs:
            if job.thetype == 'read' and job.disc == self.disc:
                sharedspeed.append(job)
        
        if self.filled > self.buffer:
            self.flushing = True
            self.flushed += self.filled
            self.filled = 0.
            for job in sharedspeed:
                job.loadspeed = job.loadspeed / 2
        
        if self.flushing == True:
            if len(sharedspeed) == 0:
                self.flushed -= self.flushspeed
            else:
                self.flushed -= (self.flushspeed/2)
            
            if self.flushed <= 0:
                self.flushed = 0.
                self.flushing = False
                
                for job in sharedspeed:
                    job.loadspeed = job.loadspeed * 2
                
                
                