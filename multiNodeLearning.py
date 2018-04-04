#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:54:27 2018

@author: Jet
"""


import numpy as np
import math

from stateSpaceCreate import stateSpaceCreate
#from radioNode   import radioNode
from legacyNode  import legacyNode
from mdpNode     import mdpNode
from hoppingNode import hoppingNode
from scenario    import scenario
import matplotlib.pyplot as plt
from myFunction  import tic
from myFunction  import toc


tic()

# Todo hoppingNode getAction
# coexist legacy node


# Simulation Parameters
numSteps = 30000/3   # easier one
numChans = 4
nodeTypes = np.array( [2,2,2,0])
# The type of each node 
#0 - Legacy (Dumb) Node 
#1 - Hopping Node
#2 - MDP Node
#3 - DSA node (just avoids)         
#4 - Adv. MDP Node
legacyTxProb = 1
numNodes = len(nodeTypes)
hiddenNodes = np.array( [0,0,0,0])
exposedNodes = np.array( [0,0,0,0])

if len(hiddenNodes) < numNodes:
    hiddenNodes = np.concatenate( ( hiddenNodes,\
                                   np.zeros(numNodes-len(hiddenNodes)) ), axis=0)

# Initializing Nodes, Observable States, and Possible Actions
nodes =  []
states = stateSpaceCreate(numChans)
numStates = np.shape(states)[0]


t = mdpNode(numChans,states,numSteps)     # breakpoint

for k in range(0,numNodes):
    if nodeTypes[k] == 0:
        t = legacyNode(numChans,numSteps,legacyTxProb)
        pass
    elif nodeTypes[k] == 1:
        t = hoppingNode(numChans,numSteps)
        pass
    elif nodeTypes[k] == 2:
        t = mdpNode(numChans,states,numSteps)     
        pass
    elif nodeTypes[k] == 3:
#        t = dsaNode(numChans,numSteps,legacyTxProb)
        pass
    else:
#        t = mdpNodeAdvanced(numChans,states,numSteps)
        pass
    t.hidden = hiddenNodes[k]
    t.exposed = exposedNodes[k] 
    nodes.append(t)
        
nodes[0].goodChans = np.array( [1,1,0,0] )        
nodes[1].goodChans = np.array( [0,1,1,0] )          
nodes[2].goodChans = np.array( [0,0,1,1] )    

simulationScenario = scenario(numSteps,'fixed',3)  

# Vector and Matrix Initializations
actions              = np.zeros((numNodes,numChans))
collisions           = np.zeros(numNodes)
collisionTally       = np.zeros((numNodes,numNodes))  #TODO
collisionHist        = np.zeros((numSteps,numNodes))
cumulativeCollisions = np.zeros((numSteps,numNodes)) 

# Main Loops
toc
print "Starting Main Loop"



legacyNodeIndicies = []
for n in range(0,numNodes):
    if isinstance(nodes[n],legacyNode):
        legacyNodeIndicies.append(n)
        
if (simulationScenario.scenarioType != 'fixed') and legacyNodeIndicies:
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies)  

observedStates = np.zeros((numNodes,numChans))

for s in range(0,numSteps):
    
    #Determination of next action for each node
    for n in range(0,numNodes):
        actions[n,:] = nodes[n].getAction(s)
        assert not any(np.isnan(actions[n,:])), "ERROR! action is Nan"
        # good for quick guess than step by step
        
        
        
    if simulationScenario.scenarioType != 'fixed':
         simulationScenario.updateScenario(nodes,legacyNodeIndicies, s)

    # Determining observations, collisions, rewards, and policies (where applicable)
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if n != nn:
                if not nodes[nn].hidden:
                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
                                and not nodes[nn].exposed:
                    # np.array( ) for robust to test np.where()
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                     
        if isinstance(nodes[n],mdpNode):
            reward = nodes[n].getReward(collisions[n],s)
#            print "reward is %d \n"%(reward)
            nodes[n].updateTrans(observedStates[n,:],s)
            if not math.fmod(s,nodes[n].policyAdjustRate):
                nodes[n].updatePolicy(s)
                  
                  
    collisionHist[s,:]        = collisions
    cumulativeCollisions[s,:] = collisions
    if s != 0:
        cumulativeCollisions[s,:] +=  cumulativeCollisions[s-1,:]
          
print "End Main Loop"
toc()      
                 
########################################################################
#############################plot session###############################

txPackets = [ ]


############### cumulativeCollisions ##################
plt.figure(1)
#plt.hold()
legendInfo = [ ]
for n in range(0,numNodes):
    plt.plot(cumulativeCollisions[:,n])      # <<<<
#    if isinstance(nodes[n],dsaNode):
#        legendInfo = 'Node %d (DSA)'%{n}
    if isinstance(nodes[n],hoppingNode):
        legendInfo.append( 'Node %d (Hopping)'%(n) )
    elif isinstance(nodes[n],mdpNode):
        legendInfo.append( 'Node %d (MDP)'%(n) )
    else:
        legendInfo.append( 'Node %d (Legacy)'%(n) )
    
    txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T).T ) )
plt.legend(legendInfo)
plt.xlabel('Step Number')
plt.ylabel('Cumulative Collisions')
plt.title( 'Cumulative Collisions Per Node')                      
plt.show()
            
        
############### cumulativeReward ##################
plt.figure(2)
#plt.hold()  #deprecate
c = 1
legendInfo = [ ]
for n in range(0,numNodes):
    if isinstance(nodes[n],mdpNode):
        plt.plot(nodes[n].cumulativeReward)
        legendInfo.append('Node %d (MDP)'%(n) )
if legendInfo:
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Reward')
    plt.title( 'Cumulative Reward Per Node')   
plt.show()             
        
#np.ceil
############### Actions #################################
plt.figure(3)
split = np.ceil(numNodes / 2)    
for n in range(0,numNodes):
    if n <= split:
        plt.subplot(split,2,n+1)
    else:
        plt.subplot(split,2,n+1)
        
    if isinstance(nodes,mdpNode):
        offset = 1
    else:
        offset = 0
    plt.plot( np.maximum(nodes[n].actionHistInd-1 , np.zeros(numSteps)),'bo' )
    plt.ylim(0,numChans+2)
    plt.xlabel('Step Number')
    plt.ylabel('Action Number')
    
    if isinstance(nodes[n],legacyNode):
        titleLabel = 'Action Taken by Node %d (Legacy)'%(n)
    elif isinstance(nodes[n],hoppingNode):
        titleLabel = 'Action Taken by Node %d (Hopping)'%(n)
    else:
        titleLabel = 'Action Taken by Node %d (MDP)'%(n)   # no dsa
    plt.title(titleLabel)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
