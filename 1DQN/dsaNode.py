import numpy as np
import random
from radioNode import radioNode
from legacyNode import legacyNode


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
    def __init__(self, numChans, numSteps,txProb):
#        self = legacyNode(numChans,numSteps,txProb)   
        # TODO what about occupied 

        
        self.actions = np.zeros((numChans+1,numChans))
        for k in range(numChans):
            self.actions[k+1,k] = 1
                                        # similiar to hopping as well
        self.numActions    = np.shape(self.actions)[0]
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        self.txProbability = txProb
        self.observedState = np.zeros(numChans)
        self.stateHist     = np.zeros((numSteps+1,numChans))
        
    ###################################################################
    # Determines an action from the node's possible actions
    ###################################################################
    def getAction(self,stepNum):
        
        ind = np.where(self.observedState == 0)[0]   # numpy return two set of value, cause np.zeros is treat as matrix
        #ind = ind(randi(length(ind)))
        
        if stepNum > 0 and np.where(self.actionHistInd[stepNum-1] == ind+1):
                # TODO ind+1 
            ind = self.actionHistInd[stepNum-1]-1            
        else:
            ind = ind[random.randint(0,len(ind)-1)]
        
        ind = ind.astype(int)  # unkown
        if random.random() <= self.txProbability:
            action = self.actions[ind+1,:]   #  self.actions = zeros(numChans+1,numChans)
        else:
            action = np.zeros(np.shape(self.actions)[1])
        
        self.actionHist[stepNum,:] = action
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0].astype(int) + 1  # convert to int  #where 
        
        
        if not np.sum(action):
            self.actionTally[0] += 1    # like a matrix, damn
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
            
        return action
        
    
    
    def updateState(self,observedState,s):
        self.observedState = observedState
        self.stateHist[s+1,:] = observedState
        
        
    
