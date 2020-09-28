# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:33:19 2020

@author: Gebruiker

There are different ways to choose what pool a file is written to.
randomChoice() chooses a random pools and only checks if there is 
enough space on it. mostSpace() chooses the pool with the most space 
free space.
"""

import random

def randomChoice(storage,size,defile):
    
    free = 0
    counter = 0
            
    while free < size and counter < 50:
        pool = random.choice(storage.pools)
        free = pool.space -pool.filled
        counter += 1
                
    if free > size:
            
        defile.pool = pool
        storage.files.append(defile)
        pool.files.append(defile)
        pool.filled += size
        storage.filled += size
        return pool
    else:
        print("error, file could not be saved")

def mostSpace(storage,size,defile):
    
    thePool = storage.pools[0]
    
    for i in range(1,len(storage.pools)):
        
        if storage.pools[i].filled < thePool.filled:
            thePool = storage.pools[i]
    
    free = thePool.space -thePool.filled
    
    if free > size:
        defile.pool = thePool
        storage.files.append(defile)
        thePool.files.append(defile)
        thePool.filled += size
        storage.filled += size
        
        return thePool
    else:
        print("error, file could not be saved")
        

def lowWorkload():
    
    return True

def aveWorkload():
    
    return True