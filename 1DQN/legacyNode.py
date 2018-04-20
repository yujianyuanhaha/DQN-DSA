#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:16:16 2018

@author: Jet
"""

import numpy as np
import random
from radioNode import radioNode

class legacyNode(radioNode):
    
    def __init__(self, numChans, numSteps, txProb, LegacyChanIndex):
        self.actions                  = np.zeros(numChans)   # missing ()
        self.actions[ LegacyChanIndex ] = 1
        self.numActions               = np.size(self.actions,0)   # get size; as smiliar as possible  # WARNING
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.txProbability            = txProb

    
    def getAction(self, stepNum):             
        
        if random.random()  <= self.txProbability:
            action = self.actions  # %  self.actions = zeros(1,numChans);
        else:
            action = np.zeros(len(self.actions)[0])

            
        self.actionHist[stepNum,:] = action;  # same synax with matlab   # replace () []
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1    #find
          
            
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        return action
          