# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:21:24 2020

@author: Gebruiker
"""
import random
import classes.job as job

def randomJob(model, time):
    if random.random() < 0.8:
                
        thedoor = random.choice(model.storage.doors)
        thetype = model.action()
                
        thejob = job.Job(thedoor,thetype)
        model.storage.currenttraffic.append(thejob)
        thejob.time.append(time)
        thejob.speedhistory.append(thejob.speed)
        #print('heh', thejob.disc.activejobs)
        thejob.disc.activejobs.append(thejob)
        #print('what the', thejob.disc.activejobs)
        '''
        found = False
        for disc in model.storage.discs:
            
            if thejob in disc.activejobs:
                print('eureka')
                found = True
        
        if found == False:
            print('oh bother')
        '''

def futureJob(model, time):
    
    readcounter = 0
    writecounter = 0
    
    for futurejob in model.storage.futurelist:
        
        if time < futurejob['time'] < (time+1):
            if futurejob['isWrite']== 'read':
                readcounter += 1
                model.databasereaddurations.append(futurejob['databaseduration'])
            elif futurejob['isWrite']== 'write':
                writecounter += 1
                model.databasewritedurations.append(futurejob['databaseduration'])
                
            thedoor = random.choice(model.storage.doors)
            #thetype = futurejob['isWrite']
            thejob = job.Job(thedoor,futurejob)
            thejob.id = futurejob['id']
            model.storage.currenttraffic.append(thejob)
            thejob.time.append(time)
            thejob.speedhistory.append(thejob.speed)
            
    model.startreadjobs.append(readcounter)
    model.startwritejobs.append(writecounter)