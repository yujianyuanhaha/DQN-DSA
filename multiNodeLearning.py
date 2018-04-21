#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:54:27 2018

@author: Jet

jianyuan@vt.edu

April,2018

The main script to run

---------------------------
Github url:
       https://github.com/yujianyuanhaha/DQN-DSA 




---------------------------
File Achitecture:

    multiNodeLearning.py -- myFunction.py
                         -- legacyNode.py
                         -- hoppingNode.py
                         -- dsaNode.py
                         -- mdpNode.py      -- mdp.py
                         -- dqnNode.py      -- dqn.py
                         -- stateSpaceCreate.py
                         -- scenario.py
                     
----------------------------                     
Main Configuration:  
    assignment of "array nodeTypes"
                       



"""


import numpy as np
import math

from stateSpaceCreate import stateSpaceCreate
#from radioNode   import radioNode
from legacyNode  import legacyNode
from mdpNode     import mdpNode
from hoppingNode import hoppingNode
from dqnNode     import dqnNode   #
from dsaNode     import dsaNode 

from scenario    import scenario
import matplotlib.pyplot as plt
from myFunction  import tic
from myFunction  import toc

#import myPlot


tic()

 
##################### Network Setup & Simulation Parameters #######################################
numSteps = 30000    # 10000 as minimum for MDP 
numChans = 8
############################################
nodeTypes = np.array( [0,0,2,5])    ########
############################################
# The type of each node 
# 0 - Legacy (Dumb) Node 
# 1 - Hopping Node
# 2 - MDP Node
# 3 - DSA node (just avoids)         
# 4 - Adv. MDP Node
# 5 - DQN Node

# !!! capacity check

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



# !!! ToDo Flexiable nodeType
# LegacyChanIndex and HoppingChanIndex
LegacyChanIndex = [0,1,2,3]
HoppingChanIndex = [ [2,3],[3,2]]  # due so far
CountLegacyChanIndex = 0
CountHoppingChanIndex = 0



##################### Construct diff Type of Nodes #######################################
for k in range(0,numNodes):
    if nodeTypes[k] == 0:
        t = legacyNode(numChans,numSteps,legacyTxProb,LegacyChanIndex[CountLegacyChanIndex])
        CountLegacyChanIndex += 1        
    elif nodeTypes[k] == 1:
        t = hoppingNode(numChans,numSteps,HoppingChanIndex[CountHoppingChanIndex])
        CountHoppingChanIndex += 1
    elif nodeTypes[k] == 2:
        t = mdpNode(numChans,states,numSteps)     
    elif nodeTypes[k] == 3:
#        t = dsaNode(numChans,numSteps,legacyTxProb)
        pass
    elif nodeTypes[k] == 4:
        pass
    else:
        t = dqnNode(numChans,states,numSteps)      # dqnNode
        pass
    t.hidden = hiddenNodes[k]
    t.exposed = exposedNodes[k] 
    nodes.append(t)
        
nodes[0].goodChans = np.array( [1,1,0,0] )        
nodes[1].goodChans = np.array( [0,1,1,0] )          
#nodes[2].goodChans = np.array( [0,0,1,1] )    

simulationScenario = scenario(numSteps,'fixed',3)  

# Vector and Matrix Initializations
actions              = np.zeros((numNodes,numChans))
collisions           = np.zeros(numNodes)
collisionTally       = np.zeros((numNodes,numNodes))  #TODO
collisionHist        = np.zeros((numSteps,numNodes))
cumulativeCollisions = np.zeros((numSteps,numNodes)) 


##################### MAIN LOOP BEGIN ############################################
toc
print "Starting Main Loop"

legacyNodeIndicies = []
for n in range(0,numNodes):
    if isinstance(nodes[n],legacyNode):
        legacyNodeIndicies.append(n)
        
if (simulationScenario.scenarioType != 'fixed') and legacyNodeIndicies:
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies)  

observedStates = np.zeros((numNodes,numChans))


###  TODO LEGACY/HOPPING NODE BEFROE START #######################



countLearnHist = np.zeros(numSteps);

for s in range(0,numSteps):
    
    #Determination of next action for each node
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode):
            observation = observedStates[n,:]
            actions[n,:], actionScalar = nodes[n].getAction(s, observation)  ###########
        else:    
            actions[n,:] = nodes[n].getAction(s)
        assert not any(np.isnan(actions[n,:])), "ERROR! action is Nan"

        
        
        
    if simulationScenario.scenarioType != 'fixed':
         simulationScenario.updateScenario(nodes,legacyNodeIndicies, s)

    # Determining observations, collisions, rewards, and policies (where applicable)
    observedStates = np.zeros((numNodes,numChans))
    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if n != nn:
                if not nodes[nn].hidden:
                    
                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)   # partial obseravtion


                    # fully understand
                    # mdp - always [1 1 1 0] does it matters
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
                                and not nodes[nn].exposed:
                    # np.array( ) for robust to test np.where()
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                    
                
                    
                     
        if isinstance(nodes[n],mdpNode):
            reward = nodes[n].getReward(collisions[n],s)
            nodes[n].updateTrans(observedStates[n,:],s)
#            print observedStates[n,:]
            if not math.fmod(s,nodes[n].policyAdjustRate):
                nodes[n].updatePolicy(s)
                                
        if isinstance(nodes[n],dqnNode):
            reward = nodes[n].getReward(collisions[n],s)
#            observedStates[n,:] =  (observedStates[n,:] + actions[n,:] > 0)  #include itself ?
            observation_ = observedStates[n,:]  # update already # full already

            done = True
            
#            if s%200 == 0:  # fit size of step

#                print observation,  actionScalar, reward, observation_
            
            nodes[n].storeTransition(observation, actionScalar, 
                 reward, observation_)
            if s > 200 and s % 5 == 0:    # step 2 trade in more computation for better performance
                nodes[n].learn()
            # original  action -> step() -> observation_, reward, done
            # 1. action -> collisions
            # 2. collisions -> getReward() -> observation_, reward, done
            
            # save the count of Learn for debug
            
            countLearnHist[s] = nodes[n].dqn_.countLearn*1.0 / (s+1)

    collisionHist[s,:]        = collisions
    cumulativeCollisions[s,:] = collisions
    if s != 0:
        cumulativeCollisions[s,:] +=  cumulativeCollisions[s-1,:]
          
print "End Main Loop"
toc()   

plt.figure(1)
plt.plot(countLearnHist)
plt.title( 'Learning Ratio') 
plt.show()

#plt.figure(2)
#nodes[0].dqn_.plot_cost()

   
##################### MAIN LOOP END ###############################################



                 
################################################################################
#############################plot session#######################################

txPackets = [ ]


############### 1 cumulativeCollisions ##################
plt.figure(6)
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
    elif isinstance(nodes[n],dsaNode):
        legendInfo.append( 'Node %d (DSA)'%(n) )
    elif isinstance(nodes[n],dqnNode):
        legendInfo.append( 'Node %d (DQN)'%(n) )
    else:
        legendInfo.append( 'Node %d (Legacy)'%(n) )
    
    txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T , axis=0).T ) )
plt.legend(legendInfo)
plt.xlabel('Step Number')
plt.ylabel('Cumulative Collisions')
plt.title( 'Cumulative Collisions Per Node')                      
plt.show()
            
        
############### 2 cumulativeReward ##################
plt.figure(2)
#plt.hold()  #deprecate
#c = 1
legendInfo = [ ]
for n in range(0,numNodes):
    if isinstance(nodes[n],mdpNode):
        plt.plot(nodes[n].cumulativeReward)
        legendInfo.append('Node %d (MDP)'%(n) )
    elif isinstance(nodes[n],dqnNode):
        plt.plot(nodes[n].cumulativeReward)
        legendInfo.append('Node %d (DQN)'%(n) )
if legendInfo:
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Reward')
    plt.title( 'Cumulative Reward Per Node')   
plt.show()             
        
#np.ceil
############### 3 Actions #################################
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
    plt.plot( np.maximum(nodes[n].actionHistInd-1 ,
                         np.zeros(numSteps)),'bo' )
    plt.ylim(0,numChans+2)
    plt.xlabel('Step Number')
    plt.ylabel('Action Number')
    
    if   isinstance(nodes[n],legacyNode):
        titleLabel = 'Action Taken by Node %d (Legacy)'%(n)
    elif isinstance(nodes[n],hoppingNode):
        titleLabel = 'Action Taken by Node %d (Hopping)'%(n)
    elif isinstance(nodes[n],dsaNode):
        titleLabel = 'Action Taken by Node %d (DSA)'%(n)
    elif isinstance(nodes[n],mdpNode):
        titleLabel = 'Action Taken by Node %d (MDP)'%(n)
    else:
        titleLabel = 'Action Taken by Node %d (DQN)'%(n)   # no dsa
    plt.title(titleLabel)

    

############### 4 Packet Error Rate  #################################
timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                             1,numNodes )  
txPackets = np.array(txPackets).T
PER =  cumulativeCollisions / txPackets
PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots
    
plt.figure(4)
legendInfo = [ ]
for i in range(numNodes):
    if isinstance(nodes[i],mdpNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (MDP)'%(i) )
    elif isinstance(nodes[i],dsaNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (DSA)'%(i) )
    elif isinstance(nodes[i],dqnNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (DQN)'%(i) )
    else:
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (legacy)'%(i) )
plt.legend(legendInfo)
plt.xlabel('Step Number')
plt.ylabel('Cumulative Packet Error Rate')
plt.title( 'Cumulative Packet Error Rate')                      
plt.show()        
        

############### 5 Packet Loss Rate  #################################
plt.figure(5)
legendInfo = [ ]
for i in range(numNodes):
    if isinstance(nodes[i],mdpNode):
        plt.semilogy( PLR[:,i] )
        legendInfo.append( 'Node %d (MDP)'%(i) )
    elif isinstance(nodes[i],dqnNode):
        plt.semilogy( PLR[:,i] )
        legendInfo.append( 'Node %d (DQN)'%(i) )
if not legendInfo:
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Loss Rate')
    plt.title( 'Cumulative Packet Loss Rate')                      
    plt.show() 
    

############### END OF PLOT  ################################# 
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
