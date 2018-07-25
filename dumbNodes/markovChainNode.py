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

class markovChainNode(radioNode):
    

    
    def __init__(self, numChans, numSteps, mcChanIndex, alpha, beta):
        # 0 -> 1 alpha, 1 -> 0 beta
        self.actions                  = np.zeros(numChans)  
        self.actions[ mcChanIndex ]  = 1
        # default
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.alpha                    = alpha   # alpha 0 -> 1
        self.beta                     = beta    # beta  1 -> 0
        # probability 0 - beta/(alpha+beta)     1 - alpha/(alpha+beta)
        print "2-state markov chain chanel availablity %s"%( beta/(alpha+beta) )

    
    def getAction(self, stepNum):             

        action = np.zeros(len(self.actions)) 
        
        if stepNum > 0:
            if any(self.actionHist[stepNum-1]):   # if 1-state, turn 0-state with beta prob
                if random.random() < 1.0 - self.beta:
                    action = self.actions
            else:
                if random.random() < self.alpha:
                    action = self.actions

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
          