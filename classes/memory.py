# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:14:15 2020

@author: Gebruiker
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
                self.flushing == False
        