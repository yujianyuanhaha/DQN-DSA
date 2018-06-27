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
    
    def __init__(self, numChans, numSteps, poissonChanIndex, arrivalRate, serviceRate):
        self.actions                  = np.zeros(numChans)  
        self.actions[ poissonChanIndex ] = 1
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.arrivalRate              = arrivalRate   # lamda
        self.serviceRate              = serviceRate   #  miu

    
    def getAction(self, stepNum):             

        if stepNum < self.indexLastArrival:
            action = np.zeros(len(self.actions)) 
        elif stepNum >= self.indexLastArrival and stepNum < self.indexLastService:
            action = self.actions
        elif stepNum >= self.indexLastService:
            action = self.actions
            self.indexLastArrival = self.indexLastService + np.random.poisson(self.arrivalRate, 1)
            self.indexLastService = self.indexLastArrival + np.random.poisson(self.serviceRate, 1)
            
        # self check ?
   
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
          