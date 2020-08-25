# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:33:19 2020

@author: Gebruiker
"""

import random

import classes.file as file

def randomChoice(storage,size):
    
    free = 0
    counter = 0
            
    while free < size and counter < 50:
        pool = random.choice(storage.pools)
        free = pool.space -pool.filled
        counter += 1
                
    if free > size:
            
        defile = file.File(size, pool)
        storage.files.append(defile)
        pool.files.append(defile)
        pool.filled += size
        storage.filled += size
    else:
        print("error, file could not be saved")

def mostSpace(storage,size):
    
    thePool = storage.pools[0]
    
    for i in range(1,len(storage.pools)):
        
        if storage.pools[i].filled < thePool.filled:
            thePool = storage.pools[i]
    
    free = thePool.space -thePool.filled
    
    if free > size:
        defile = file.File(size,thePool)
        storage.files.append(defile)
        thePool.files.append(defile)
        thePool.filled += size
        storage.filled += size
    else:
        print("error, file could not be saved")
        

def lowWorkload():
    
    return True

def aveWorkload():
    
    return True