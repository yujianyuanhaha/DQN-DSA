#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:16:16 2018

@author: Jet



The arrival interval and service(occupied) interval follows poisson distribution


"""

import numpy as np
import random
from radioNode import radioNode

class poissonNode(radioNode):
    
    indexLastArrival = 1
    indexLastService = 2  # hard-code starter, does not matter
    
    def __init__(self, numChans, numSteps, poissonChanIndex, arrivalInterval, serviceInterval):
        self.OFF                      = np.zeros(numChans)        
        temp                          = np.zeros(numChans)  
        temp[poissonChanIndex]        = 1
        self.ON                       = temp
        self.actions                  = self.ON
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.arrivalInterval          = arrivalInterval   # lamda
        self.serviceInterval          = serviceInterval   #  miu
        self.type                     = "possion"
        self.hyperType                = "stochastic"   
        
        print "possion M/M/1  availablity %s"%( serviceInterval*1.0/arrivalInterval )

    
    def getAction(self, stepNum):             

        "--- OFF state for arrival, while ON for service time ---"
        if stepNum < self.indexLastArrival:
            action = self.OFF
#            print "step %s, OFF, during arrival, %s, %s"%(stepNum,self.indexLastArrival, self.indexLastService)
        elif stepNum >= self.indexLastArrival and stepNum < self.indexLastService:
            action = self.ON
#            print "step %s, ON, on service,  %s, %s" %(stepNum,self.indexLastArrival, self.indexLastService)
        else:
            action = self.OFF
#            print "step %s, OFF & update"%(stepNum)

            t1 = np.random.poisson(self.arrivalInterval, 1)
            self.indexLastArrival = self.indexLastService + t1

            t2 = np.random.poisson(self.serviceInterval, 1)   # average service time, means ON state
            self.indexLastService = self.indexLastArrival + t2
#            print ' update as %s, %s'%(self.indexLastArrival, self.indexLastService)
            
         
           

   
        self.actionHist[stepNum,:] = action
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1             
            
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        return action

# ToDo - easily extend to M/M/c wherer c as numServer

          
if __name__ == '__main__':
    x = poissonNode(4, 100000, 1, 3, 2) # should be 0.2 available
    ON = 0
    for i in range(100):
        action = x.getAction(i)
        if np.sum(action):
            ON += 1
    print ON*1.0/100
    "100 step is enough"
    
    ON = 0
    for i in range(1000):
        action = x.getAction(i)
        if np.sum(action):
            ON += 1
    print ON*1.0/1000
    
    ON = 0
    for i in range(10000):
        action = x.getAction(i)
        if np.sum(action):
            ON += 1
    print ON*1.0/10000
    
    ON = 0
    for i in range(100000):
        action = x.getAction(i)
        if np.sum(action):
            ON += 1
    print ON*1.0/100000
    " test pass"   