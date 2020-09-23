# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:44:57 2020

@author: Gebruiker
"""

import random

import helpers.choices as choices

class Door():
    
    def __init__(self,storage):
        
        self.storage = storage
        self.poolcounter = []
        self.everyspeed = []
        
    def getPool(self,size,file):
        thePool = choices.randomChoice(self.storage,size,file)
        
        sharedspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool and job.thetype != 'delete':
                sharedspeed.append(job)
        #print('getpool')
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        #print('writespeed',len(self.storage.currenttraffic),newspeed)
        #print('new',newspeed)
        for job in sharedspeed:
            #print(job.speed)
            job.speed = newspeed
            #print('newspeed',job.speed)
    
        self.poolcounter.append(thePool)
        #print('write',self.poolcounter)
        return thePool, newspeed
    
    def locatePool(self):
        thePool = random.choice(self.storage.pools)
        theFile = random.choice(thePool.files)
                
        sharedspeed = []
        loadspeed = []
        
        for job in self.storage.currenttraffic:
            if job.pool == thePool and job.thetype != 'delete':
                sharedspeed.append(job)
                #print('speed',job.speed)
                if job.thetype == 'read':
                    loadspeed.append(job)
                    #print('loadspeed',job.loadspeed)
        
        '''print('bandwith',thePool.bandwith)
        print('amount',len(sharedspeed))
        print('other amount', len(loadspeed))'''
        newspeed = thePool.bandwith / (len(sharedspeed)+1)
        self.everyspeed.append(newspeed)
        #print('readspeed',len(self.storage.currenttraffic),newspeed)
        #print('getpool')
        #print('new',newspeed)
        newload = thePool.memo.flushspeed / (len(loadspeed)+1)
        if thePool.memo.flushing == True:
             newload = newload / 2
        
        for job in sharedspeed:
            #print(job.speed)
            job.speed = newspeed
            #print('newpspeed',job.speed)
            
        for job in loadspeed:
            job.loadspeed = newload
            #print('newload',job.loadspeed)
        #print('another one')
        
        self.poolcounter.append(thePool)
        #print('read',self.poolcounter)
        return theFile, thePool, newspeed, newload
    
    def deletePool(self):
        
        thePool = random.choice(self.storage.pools)
        file = random.choice(thePool.files)
        
        self.storage.files.remove(file)
        self.poolcounter.append(thePool)
        #print('delete',self.poolcounter)
        return file, thePool
    
    def checkDelete(self, pool):
        
        traffic = []
        
        for job in self.storage.currenttraffic:
            if job.pool == pool:
                traffic.append(job)
                
        if len(traffic) > 2:
            return False
        else:
            return True
        
    
    def closeJob(self,job):
        
        self.poolcounter.remove(job.pool)
        #print('closed',self.poolcounter)
        #print('huh what')
        #print(self.storage.currenttraffic)
        self.storage.currenttraffic.remove(job)
        #print(self.storage.currenttraffic)
        sharedspeed = []
        
        for ajob in self.storage.currenttraffic:
            if ajob.pool == job.pool:
                sharedspeed.append(ajob)
        #print('closed')
        if len(sharedspeed) > 0 and job.thetype != 'delete':
            newspeed = job.pool.bandwith / len(sharedspeed)
            self.everyspeed.append(newspeed)
            #print('closedspeed',len(self.storage.currenttraffic),newspeed)
            #print('new',newspeed)
            #print(sharedspeed)
            for job in sharedspeed:
                #print(job.speed)
                job.speed = newspeed
                #print('newspeed',job.speed)
            
            