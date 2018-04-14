import numpy as np
import random
from radioNode import radioNode





class dsaNode (legacyNode):
    # one typical of 'legacy Node'
    ###################################################################
    # Defines a node with the default behavior of always using the same
    # randomly chosen channel.
    ###################################################################
    
    observedState = [ ]
    stateHist = [ ]
  


    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self,numChans,numSteps,txProb):
        self@legacyNode(numChans,numSteps,txProb)    # @ magic 
        # https://www.mathworks.com/help/matlab/matlab_oop/calling-superclass-methods-on-subclass-selfects.html
        # subclass superclass
        
        self.actions = zeros(numChans+1,numChans)
        for k in range(numChans):
            self.actions[k+1,k] = 1
                                        # similiar to hopping as well
        self.numActions    = np.size((self.actions,1) )
        self.actionTally   = np.zeros((1,numChans+1))
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros((1,numSteps))
        self.txProbability = txProb
        self.observedState = np.zeros((1,numChans))
        self.stateHist     = np.zeros((numSteps+1,numChans))
        
    ###################################################################
    # Determines an action from the node's possible actions
    ###################################################################
    def action = getAction(self,stepNum):
        
        ind = find(self.observedState == 0)
        #ind = ind(randi(length(ind)))
        
        if stepNum > 1:
            if find(self.actionHistInd[stepNum-1] == ind+1):
                ind = self.actionHistInd[stepNum-1]-1
            else:
                ind = ind[randi[len(ind)]]
            
        else:
            ind = ind[randi[len(ind)]]
        
        
        if rand <= self.txProbability:
            action = self.actions[ind+1,:]   #  self.actions = zeros(numChans+1,numChans)
        else:
            action = np.zeros((1,np.shape(self.actions,2)))
        
        self.actionHist[stepNum,:] = action
        if ~sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = find(action == 1) + 1
        
        
        if ~sum(action):
            self.actionTally[0] = self.actionTally[0] + 1
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
        
    
    
    def updateState(self,observedState,s):
        self.observedState = observedState
        self.stateHist[s+1,:] = observedState
        
        
    
