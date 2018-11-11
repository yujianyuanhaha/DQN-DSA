import numpy as np
import random
from radioNode import radioNode



class dsaNode (radioNode):   
    # when come to isinstance(), both isinstance(nodes[1],dsaNode) or isinstance(nodes[1],legacyNode) is true
    
    ###################################################################
    # Defines a node with the default behavior of always using the same
    # randomly chosen channel.
    ###################################################################
    
    observedState = [ ]
    stateHist = [ ]

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, numChans, numSteps):
        
        self.actions = np.zeros((numChans+1,numChans))
        for k in range(numChans):
            self.actions[k+1,k] = 1
                                        # similiar to hopping as well
        self.numActions    = np.shape(self.actions)[0]
        self.actionTally   = np.zeros(numChans+1)
        self.actionHist    = np.zeros((numSteps,numChans))
        self.actionHistInd = np.zeros(numSteps)
        self.txProbability = 1.0     # could be modified
        self.observedState = np.zeros(numChans)
        self.stateHist     = np.zeros((numSteps+1,numChans))
        self.type          = "dsa"
        self.hyperType     = "dumb"
        
    ###################################################################
    # Determines an action from the node's possible actions
    ###################################################################
    def getAction(self,stepNum):
        
        ind = np.where(self.observedState == 0)[0]   # numpy return two set of value, cause np.zeros is treat as matrix
        if not any(ind):
            action = np.zeros(np.shape(self.actions)[1])
        else:
            # choose the first one
            if stepNum > 0 and np.where(self.actionHistInd[stepNum-1] == ind+1) == True:
                   
                    ind = self.actionHistInd[stepNum-1] - 1                  
            # STAY ORGANIZED - could not figure Chris intention of follow previous step, would it work with hopping Nodes ? 
            # first-available-channel would not work
            else:
                if random.random() <= 0.5:    # 50% politeness to avoid, but still stuck for hopping node
                    ind = ind[random.randint(0,len(ind)-1)]
                else:
                    ind = self.actionHistInd[stepNum-1] - 1    # avoid ping-pong when mutilple dsaNode
        
            ind = ind.astype(int)  
            if random.random() <= self.txProbability:
                action = self.actions[ind+1,:]  
            else:
                action = np.zeros(np.shape(self.actions)[1])
        
        self.actionHist[stepNum,:] = action
        if not np.sum(action):
            self.actionHistInd[stepNum] = 0
        else:
            self.actionHistInd[stepNum] = np.where(action == 1)[0].astype(int) + 1  
              
        if not np.sum(action):
            self.actionTally[0] += 1    
        else:
            self.actionTally[1:] = self.actionTally[1:] + action
            
        return action

    
    def updateState(self, observedState, s):
        self.observedState = observedState
        self.stateHist[s+1,:] = observedState
        
        
    
