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
        
        self.OFF                      = np.zeros(numChans)        
        temp                          = np.zeros(numChans)  
        temp[ mcChanIndex ]           = 1
        self.ON                       = temp
        self.actions                  = self.ON
        # default
        self.numActions               = np.size(self.actions,0)  
        self.actionTally              = np.zeros(numChans+1)
        self.actionHist               = np.zeros((numSteps,numChans))
        self.actionHistInd            = np.zeros(numSteps)
        self.alpha                    = alpha   # alpha 0 -> 1
        self.beta                     = beta    # beta  1 -> 0
        self.type                     = "markovChain"
        self.hyperType                = "stochastic"   
        "-------- probability 0 - beta/(alpha+beta)     1 - alpha/(alpha+beta) -------"
        print "2-state markov chain chanel availablity %s"%( beta/(alpha+beta) )

    
    def getAction(self, stepNum, forceFlip):             

        action = self.OFF 
        
        if stepNum > 0:
            if np.sum(self.actionHist[stepNum-1]):   # if 1-state, turn 0-state with beta prob
                if random.random() < 1.0 - self.beta:
                    action = self.ON
            else:
                if random.random() < self.alpha:
                    action = self.ON
                    
        if forceFlip:   # Yue's forceFlip
            print "flip at step %s"%(stepNum)
            if np.sum(self.actionHist[stepNum-1]):
                action = self.OFF
            else:
                action = self.ON
                
                
   
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
 
if __name__ == '__main__':
    x = markovChainNode(4, 10000, 1, 0.1, 0.9)
    ON = 0
    
    numSteps = 10000
    flipLength = 100
    forceFlip = 0
    
    states = np.zeros(numSteps)   # config
    
    for i in range(numSteps):
        action = x.getAction(i,forceFlip)
        if np.sum(action):
            ON += 1
            states[i] = 1
            
        tail_ = i
        if tail_ - flipLength < 0:
            head_ = 0
        else:
            head_ = tail_ - flipLength
        
        if tail_ >  flipLength:
            if np.sum(states[head_:tail_]) == 0 or np.sum(states[head_:tail_]) == flipLength:
                forceFlip = 1
            else:
                forceFlip = 0
            
        
            
    print ON*1.0/numSteps


# a little bit influence, never mind -> not suggest for confusing