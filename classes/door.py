# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker

The door class handles the communication in the model. For each new job it looks
up where the file can be stored/retrieved from and it changes the loading speed
of all jobs if new jobs come up or old jobs close.
"""

import copy
import random

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        self.disccounter = []
        self.everyspeed = [] 
        
    def getdisc(self,size,file):
        thedisc = choices.randomChoice(self.storage,size,file)
        
        newspeed = self.writeSpeed(thedisc)
        return thedisc, newspeed
    
    def locatedisc(self):
        thedisc = random.choice(self.storage.discs)
        theFile = random.choice(thedisc.files)
        
        newspeed, newload = self.readSpeed(thedisc)
        
        return theFile, thedisc, newspeed, newload
    
    def deletedisc(self):
        
        thedisc = random.choice(self.storage.discs)
        file = random.choice(thedisc.files)
        
        self.storage.files.remove(file)
        #self.disccounter.append(thedisc)
        return file, thedisc
    
    def checkDelete(self, disc):
                
        if len(disc.activejobs) > 2:
            return False
        else:
            return True
        
    def writeSpeed(self,thedisc):
        #print(thedisc.activejobs)
        
        sharedspeed = []
        
        if len(thedisc.activejobs) > 0:
            
            for job in thedisc.activejobs:
                if job.thetype == 'read' or job.thetype == 'write':
                    sharedspeed.append(job)
        
        for job in sharedspeed:
            if job.thetype == 'delete':
                sharedspeed.remove(job)
        
        newspeed = thedisc.bandwith / (len(sharedspeed)+1)
        #self.everyspeed.append(newspeed)
        
        for job in sharedspeed:
            job.speed = newspeed
    
        #self.disccounter.append(thedisc)
        #print('write',newspeed)
        return newspeed
    
    def readSpeed(self,thedisc):
        
        sharedspeed = []
        loadspeed = []
        
        if len(thedisc.activejobs) > 0:
            
            for job in thedisc.activejobs:
                if job.thetype == 'read' or job.thetype == 'write':
                    sharedspeed.append(job)
                    if job.thetype == 'read':
                        loadspeed.append(job)
        
        newspeed = thedisc.bandwith / (len(sharedspeed)+1)
        #self.everyspeed.append(newspeed)
        newload = thedisc.memo.flushspeed / (len(loadspeed)+1)
        if thedisc.memo.flushing == True:
             newload = newload / 2
        
        for job in sharedspeed:
            job.speed = newspeed
            
        for job in loadspeed:
            job.loadspeed = newload
        
        #self.disccounter.append(thedisc)
        #print('read',newspeed,newload)
        return newspeed,newload
    
    def closeJob(self,job):
        print('before', len(self.storage.currenttraffic))
        
        #self.disccounter.remove(job.disc)
        self.storage.currenttraffic.remove(job)
        '''
        print('huh', job.disc)
        
        for disc in self.storage.discs:
            if job in disc.activejobs:
                print('frustrating',disc)
        for disc in self.storage.discs:
            if disc == job.disc:
                print('ugh',disc)
                print('blrgh', job.disc.activejobs)
        print('maar het gaat ook wel goed', job)
        '''
        job.disc.activejobs.remove(job)
        #print('weird',job.disc.activejobs)
        sharedspeed = []
        loadspeed = []
        
        if len(job.disc.activejobs) > 0:
            
            for ajob in job.disc.activejobs:
                if ajob.thetype == 'read' or ajob.thetype == 'write':
                    sharedspeed.append(job)
                    if ajob.thetype == 'read':
                        loadspeed.append(ajob)
        
        newspeed =0
        newload = 0
        
        if len(sharedspeed) > 0 and job.thetype != 'delete':
            newspeed = job.disc.bandwith / len(sharedspeed)
            #self.everyspeed.append(newspeed)
            
            for ajob in sharedspeed:
                ajob.speed = newspeed
                
            if len(loadspeed) > 0 and job.thetype == 'read':
                newload = job.disc.memo.flushspeed / (len(loadspeed))
                if job.disc.memo.flushing == True:
                    newload = newload / 2
                for ajob in loadspeed:
                    ajob.loadspeed = newload
                    
        print('end',newspeed,newload)
        print('after', len(self.storage.currenttraffic))