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
        
        self.storage = storage.Storage(self.npools)
        self.jobs = []
        
        self.setup()
    
    def setup(self):
        
        for i in range(random.randint(10,100)):
            size = random.random()/100.
            self.placeFile(size)
                
    def placeFile(self,size):
        
        choices.mostSpace(self.storage,size)
        
    
    def run(self):
        
        for i in range(1000):
            if random.random() < 0.1:
                thedoor = random.choice(self.storage.doors)
                thetype = self.action()
                job.Job(thedoor,thetype)
            print(self.storage.pools[0].filled)
            print(self.storage.filled)
            
    def action(self):
        
        rand = random.random()
        
        if rand<0.46:
            return("read")
        elif rand<0.92:
            return("write")
        else:
            return("delete")
    '''
    def read(self):
        print("read")
        rfile = random.choice(self.storage.files)
        
    def write(self):
        print("write")
        size = random.random()/100.
        self.placeFile(size)
        
    def delete(self):
        print("delete")
        dfile = random.choice(self.storage.files)
        dfile.pool.files.remove(dfile)
        self.storage.files.remove(dfile)
        dfile.pool.filled -= dfile.size
    '''