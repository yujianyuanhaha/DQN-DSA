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
        
        
        # exponential distribution -> geometric distribution
        # ON dist -OFF dist

        self.const = 150  
        self.pOn = 0.20    # for exp
        self.pOff = 0.40
        self.lamba = 4   #for possion
        self.miu = 5
        self.onDist = "const"
#        self.onDist = "exp"
#        self.onDist = "pos"
#        self.onDist = "uni"

#        self.offDist = "const"
#        self.offDist = "exp"
#        self.offDist = "pos"
        self.offDist = "uni"

        self.pattern                  = self.generateSequences(numSteps)
        
        
        
    def uniDist(self):
        # [a,b,c,d]
        # 10% 20% 30% 40%
        # 5    6   7  8
        # 0.5+1.2+2.1+3.2 = 7.0
        
        
        a = 0.10
        b = 0.30
        c = 0.60
        
        var = np.random.rand() 
        if var < a:
            l = 150
        elif var >= a and var <b:
            l = 160
        elif var >= b and var <c:
            l = 170
        else:
            l = 180
        
        # case 2
        
                # [a,b,c,d]
        # 5% 5% 10% 10%  15% 15% 20% 20%
        # 5   6   7  8   9   10   11  12
        # ..
        
        
#        a = 0.05
#        b = 0.10
#        c = 0.20
#        d = 0.30
#        e = 0.45
#        f = 0.60
#        g = 0.80
#        
##        
#        var = np.random.rand() 
#        if var < a:
#            l = 15
#        elif var >= a and var <b:
#            l = 16
#        elif var >= b and var <c:
#            l = 17
#        elif var >= c and var <d:
#            l = 18
#        elif var >= d and var <e:
#            l = 19
#        elif var >= e and var <f:
#            l = 20
#        elif var >= f and var <g:
#            l = 21
#        else:
#            l = 22
#            
        return l
            
        
        
    def generateSequences(self,numSteps):
        pattern = [ ]
        
        
        while len(pattern)<= numSteps:
           
            if self.onDist == "const":
                new = np.ones(self.const)
            elif self.onDist == "exp":
                var = np.random.geometric(self.pOn, size=1)
                new = np.ones(var[0])
            elif self.onDist == "pos":
                var = np.random.poisson(self.lamba, size=1)
                new = np.ones(var[0])
            elif self.onDist == "uni":
                var = self.uniDist()
                new = np.ones(var)
            else:
                print "error onDist"
            for i in new:
                pattern.append(i)
                
            if self.offDist == "const":
                new = np.zeros(self.const)
            elif self.offDist == "exp":
                var = np.random.geometric(self.pOff, size=1)
                new = np.zeros(var[0])
            elif self.offDist == "pos":
                var = np.random.poisson(self.miu, size=1)
                new = np.zeros(var[0])
            elif self.offDist == "uni":
                var = self.uniDist()
                new = np.zeros(var)
            else:
                print "error onDist"
            for i in new:
                pattern.append(i)


        
        return pattern[:numSteps]
        
#        print "possion M/M/1  availablity %s"%( serviceInterval*1.0/(arrivalInterval+serviceInterval+1) )


    def getAction(self, stepNum):
        temp = self.pattern[stepNum]
        if temp:
            temp2 = self.ON
        else:
            temp2 = self.OFF
            
        action = temp2
        self.actionHist[stepNum,:] = action
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1             
            
        if not np.sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
            
        return temp2
    
#    def getAction(self, stepNum):             
#
#        "--- OFF state for arrival, while ON for service time ---"
#        if stepNum <= self.indexLastArrival:
#            action = self.OFF
#        elif stepNum > self.indexLastArrival and stepNum <= self.indexLastService:
#            action = self.ON
#        else:
#            action = self.OFF
#
#            t1 = np.random.poisson(self.arrivalInterval, 1)
#            self.indexLastArrival = self.indexLastService + t1
#            t2 = np.random.poisson(self.serviceInterval, 1)  # average service time, means ON state
#            self.indexLastService = self.indexLastArrival + t2
#            # actually the interleave is NOT TRUE POSSION
#
#        self.actionHist[stepNum,:] = action
#        if not np.sum(action):
#            self.actionHistInd[stepNum] = 0
#        else:
#            self.actionHistInd[stepNum] = np.where(action == 1)[0] + 1             
#            
#        if not np.sum(action):
#            self.actionTally[0] = self.actionTally[0] + 1
#        else:
#            self.actionTally[1:] = self.actionTally[1:] + action
#        return action
#
## ToDo - easily extend to M/M/c wherer c as numServer

          
if __name__ == '__main__':
    for y in range(4,10):
        print "%s,4"%(y)
        x = poissonNode(4, 100000, 1, y ,4) # should be 0.2 available
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
    #    
        ON = 0
        for i in range(10000):
            action = x.getAction(i)
            if np.sum(action):
                ON += 1
        print ON*1.0/10000
#    
#    ON = 0
#    for i in range(100000):
#        action = x.getAction(i)
#        if np.sum(action):
#            ON += 1
#    print ON*1.0/100000
#    " test pass"   