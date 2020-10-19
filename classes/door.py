# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker

The door class handles the communication in the model. For each new job it looks
up where the file can be stored/retrieved from and it changes the loading speed
of all jobs if new jobs come up or old jobs close.
"""

import random

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        self.disccounter = []
        self.everyspeed = []
        
    def getdisc(self,size,file):
        thedisc = choices.randomChoice(self.storage,size,file)
        
        sharedspeed = []
        
        for job in self.storage.currenttraffic:
            if job.disc == thedisc and job.thetype != 'delete':
                sharedspeed.append(job)
        
        newspeed = thedisc.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        
        for job in sharedspeed:
            job.speed = newspeed
    
        self.disccounter.append(thedisc)
        return thedisc, newspeed
    
    def locatedisc(self):
        thedisc = random.choice(self.storage.discs)
        theFile = random.choice(thedisc.files)
                
        sharedspeed = []
        loadspeed = []
        
        for job in self.storage.currenttraffic:
            if job.disc == thedisc and job.thetype != 'delete':
                sharedspeed.append(job)
                if job.thetype == 'read':
                    loadspeed.append(job)
        
        newspeed = thedisc.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        newload = thedisc.memo.flushspeed / (len(loadspeed)+1)
        if thedisc.memo.flushing == True:
             newload = newload / 2
        
        for job in sharedspeed:
            job.speed = newspeed
            
        for job in loadspeed:
            job.loadspeed = newload
        
        self.disccounter.append(thedisc)
        return theFile, thedisc, newspeed, newload
    
    def deletedisc(self):
        
        thedisc = random.choice(self.storage.discs)
        file = random.choice(thedisc.files)
        
        self.storage.files.remove(file)
        self.disccounter.append(thedisc)
        return file, thedisc
    
    def checkDelete(self, disc):
        
        traffic = []
        
        for job in self.storage.currenttraffic:
            if job.disc == disc:
                traffic.append(job)
                
        if len(traffic) > 2:
            return False
        else:
            return True
        
    
    def closeJob(self,job):
        
        self.disccounter.remove(job.disc)
        self.storage.currenttraffic.remove(job)
        sharedspeed = []
        
        for ajob in self.storage.currenttraffic:
            if ajob.disc == job.disc:
                sharedspeed.append(ajob)
        
        if len(sharedspeed) > 0 and job.thetype != 'delete':
            newspeed = job.disc.bandwith / len(sharedspeed)
            self.everyspeed.append(newspeed)
            
            for job in sharedspeed:
                job.speed = newspeed