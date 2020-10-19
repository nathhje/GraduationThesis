# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:21:24 2020

@author: Gebruiker
"""
import random
import classes.job as job

def randomJob(model, time):
    if random.random() < 0.3:
                
        thedoor = random.choice(model.storage.doors)
        thetype = model.action()
                
        thejob = job.Job(thedoor,thetype)
        model.storage.currenttraffic.append(thejob)
        thejob.time.append(time)
        thejob.speedhistory.append(thejob.speed)
    

def futureJob(model, time):
    
    for futurejob in model.storage.futurelist:
        
        if futurejob['time'] == time:
            
            thedoor = random.choice(model.storage.doors)
            thetype = futurejob['isWrite']
            thejob = job.Job(thedoor,thetype)
            model.storage.currenttraffic.append(thejob)
            thejob.time.append(time)
            thejob.speedhistory.append(thejob.speed)