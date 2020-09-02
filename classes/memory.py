# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:14:15 2020

@author: Gebruiker

Very important notes: right now the flushcheck does not check if a file is being read,
if it is, the flushspeed should be halved, it is also necessary that when the flush
status changes, the speeds for all reads are altered, which doesn't happen right
now. Also, if the previous flush is still busy when the next flush is started,
the first flush is overwritten. Not a worry for right now, but definitely a
malfunction.
"""

class Memory():
    
    def __init__(self):
        self.space = 0.1
        self.buffer = 0.05
        self.filled = 0.
        self.flushing = False
        self.flushed = 0.
        self.flushspeed = 0.0001
        self.readused = 0.
        
        
    def flushCheck(self):
        
        if self.filled > self.buffer:
            self.flushing = True
            self.flushed = self.filled
            self.filled = 0.
                    
        if self.flushing == True:
            self.flushed -= self.flushspeed
            if self.flushed < 0:
                self.flushed = 0.
                self.flushing == False
                