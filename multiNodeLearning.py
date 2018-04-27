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
                         -- imNode.py
                         -- dsaNode.py
                         -- mdpNode.py      -- mdp.py
                         -- dqnNode.py      -- dqn.py
                         -- stateSpaceCreate.py
                         -- scenario.py
                     
----------------------------                     
Main Configuration:  
1. assignment of array "nodeTypes"  "legacyChanList"  "hoppingChanList"
                        



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
from imNode     import imNode 

from scenario    import scenario
import matplotlib.pyplot as plt
import time
import random
from myFunction import channelAssignment

# !!! ToDo import myPlot




# for unknown reason, terminal of Spyder would keep the old tensorflow neural network data
# when change numChans(related to neural network), REMEMBER TO SHUT OFF AND OPEN A NEW terminal
# it would not happen in raw terminal 

################################################################
#######################     Network Setup & Simulation Parameters  ############
numSteps = 30000 
numChans = 4                             
nodeTypes = np.array( [0,0,0,2,5])              
legacyChanList = [0,1,2,3,4]                      
imDutyCircleList = [0.5,0.5,0.2,0.2]           
hoppingChanList = [ [2,3]]                   
txProbability = 1.0
hoppingWidth = 2  
# The type of each node 
# 0 - Legacy (Dumb) Node 
# 1 - Hopping Node
# 2 - Intermittent Node/ im Node
# 3 - DSA node (just avoids)  
# 4 - MDP Node
# 5 - DQN Node       
# 6 - Adv. MDP Node

# the order does not matter for dsa, dqn, mdp make action
# we even allow several DSA coexsit
                                
################################################################
################################################################



ChannelAssignType = 'typeIn'
if ChannelAssignType == 'random':
    legacyChanList, imChanList, hoppingChanList, utilization =\
        channelAssignment(nodeTypes, hoppingWidth, numChans)
elif ChannelAssignType == 'case1':
    "0-2 legacy,0-2 hopping"
    legacyChanList = [0,1,2,3]
    hoppingChanList = [ [2,3],[3,2]]
elif ChannelAssignType == 'case2':
    "0-4 legacy, 0-3 hopping"
    legacyChanList = [0,1,2,3]
    hoppingChanList = [ [4,5,6],[5,6,4],[6,5,4]]
else:
    pass
        

numNodes = len(nodeTypes)
hiddenNodes = np.zeros( numChans)
exposedNodes = np.zeros( numChans)

if len(hiddenNodes) < numNodes:
    hiddenNodes = np.concatenate( ( hiddenNodes,\
                                   np.zeros(numNodes-len(hiddenNodes)) ), axis=0)

# Initializing Nodes, Observable States, and Possible Actions
nodes =  []
states = stateSpaceCreate(numChans)
numStates = np.shape(states)[0]





CountLegacyChanIndex = 0
CountHoppingChanIndex = 0
##################### Construct diff Type of Nodes #######################################
for k in range(0,numNodes):
    if   nodeTypes[k] == 0:
        t = legacyNode(numChans,numSteps, txProbability, legacyChanList[CountLegacyChanIndex]) 
        CountLegacyChanIndex += 1               
    elif nodeTypes[k] == 1:
        t = hoppingNode(numChans,numSteps,hoppingChanList[CountHoppingChanIndex])
        CountHoppingChanIndex += 1
    elif nodeTypes[k] == 2:
        t = imNode(numChans,numSteps,imDutyCircleList[CountLegacyChanIndex], legacyChanList[CountLegacyChanIndex])
        CountLegacyChanIndex += 1
    elif nodeTypes[k] == 3:
        t = dsaNode(numChans,numSteps,txProbability)    
    elif nodeTypes[k] == 4:
        t = mdpNode(numChans,states,numSteps)   
    elif nodeTypes[k] == 5:
        t = dqnNode(numChans,states,numSteps)      # dqnNode
    else:
        pass
    t.hidden = hiddenNodes[k]
#    t.exposed = exposedNodes[k] 
    nodes.append(t)
        
#nodes[0].goodChans = np.array( [1,1,0,0] )        
#nodes[1].goodChans = np.array( [0,1,1,0] )          
#nodes[2].goodChans = np.array( [0,0,1,1] )    

simulationScenario = scenario(numSteps,'fixed',3)  

# Vector and Matrix Initializations
actions              = np.zeros((numNodes,numChans))
collisions           = np.zeros(numNodes)
collisionTally       = np.zeros((numNodes,numNodes))  #TODO
collisionHist        = np.zeros((numSteps,numNodes))
cumulativeCollisions = np.zeros((numSteps,numNodes)) 



mdpLearnTime = np.zeros(numSteps)
dqnLearnTime = np.zeros(numSteps)

##################### MAIN LOOP BEGIN ############################################
tic = time.time()
ticMdpAction = [ ]
ticDqnAction = [ ]
print "Starting Main Loop"

legacyNodeIndicies = []
for n in range(0,numNodes):
    if isinstance(nodes[n],legacyNode):
        legacyNodeIndicies.append(n)
        
if (simulationScenario.scenarioType != 'fixed') and legacyNodeIndicies:
    simulationScenario.initializeScenario(nodes,legacyNodeIndicies)  



###  TODO LEGACY/HOPPING NODE BEFROE START #######################



#countLearnHist = np.zeros(numSteps);
observedStates = np.zeros((numNodes,numChans))
for s in range(0,numSteps):
    
    #Determination of next action for each node
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode):
            ticDqnAction  = time.time()
            observation = observedStates[n,:]
            actions[n,:], actionScalar = nodes[n].getAction(s, observation)  ###########
#            if not np.sum(actions[n,:] ):
#                print "dqnNode WAIT"
            tocDqnAction  = time.time()
        elif isinstance(nodes[n],mdpNode):
            ticMdpAction  = time.time()
            actions[n,:] = nodes[n].getAction(s)
            tocMdpAction  = time.time()
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
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ): #\and not nodes[nn].exposed:    
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                     
                    
        if isinstance(nodes[n],dsaNode):
            nodes[n].updateState(observedStates[n,:],s)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],s)
            nodes[n].updateTrans(observedStates[n,:],s)
            if not math.fmod(s,nodes[n].policyAdjustRate):
                nodes[n].updatePolicy(s)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n],s)
            observation_ = observedStates[n,:]  # update already # full already
            done = True            
            nodes[n].storeTransition(observation, actionScalar, 
                 reward, observation_)
            if s > 200 and s % 5 == 0:    # step 2 trade in more computation for better performance
                nodes[n].learn()
            tocDqnLearn = time.time()
            # original  action -> step() -> observation_, reward, done
            # 1. action -> collisions
            # 2. collisions -> getReward() -> observation_, reward, done
    collisionHist[s,:]        = collisions
    cumulativeCollisions[s,:] = collisions
    if s != 0:
        cumulativeCollisions[s,:] +=  cumulativeCollisions[s-1,:]
    
    if ticMdpAction:
        mdpLearnTime[s] = tocMdpAction - ticMdpAction + tocMdpLearn - ticMdpLearn
    if ticDqnAction:
        dqnLearnTime[s] = tocDqnAction - ticDqnAction + tocDqnLearn - ticDqnLearn
          
print "End Main Loop"
toc =  time.time()
print "--- %s seconds ---" %(toc - tic)
  

#plt.figure(1)
#plt.plot(countLearnHist)
#plt.title( 'Learning Ratio') 
#plt.show()

#plt.figure(2)
#nodes[0].dqn_.plot_cost()


#plt.figure(1)
#legendInfo = [ ]
#for n in range(0,numNodes):
#    if isinstance(nodes[n],mdpNode):
#        plt.plot(mdpLearnTime[400:])
#        legendInfo.append( 'Node %d (MDP)'%(n) )
#    elif isinstance(nodes[n],dqnNode):
#        plt.plot(dqnLearnTime[400:])
#        legendInfo.append( 'Node %d (DQN)'%(n) )
#plt.legend(legendInfo)
#plt.xlabel('Step Number')
#plt.ylabel('Learn Time')
#plt.title( 'Learn Time') 
#plt.show()



   
##################### MAIN LOOP END ###############################################



                 
################################################################################
#############################plot session#######################################
import os
# "test if directory ../dqnFig exist, if not create one"
if not os.path.exists('../dqnFig'):
    os.makedirs('../dqnFig')
            
txPackets = [ ]


############### 1 cumulativeCollisions ##################
plt.figure(1)
#plt.hold()
legendInfo = [ ]
for n in range(0,numNodes):
    plt.plot(cumulativeCollisions[:,n])      # <<<<
    if isinstance(nodes[n],legacyNode):
        legendInfo.append( 'Node %d (Legacy)'%(n) )
    elif isinstance(nodes[n],hoppingNode):
        legendInfo.append( 'Node %d (Hopping)'%(n) )
    elif isinstance(nodes[n],imNode):
        legendInfo.append( 'Node %d (Intermittent)'%(n) )
    elif isinstance(nodes[n],dsaNode):
        legendInfo.append( 'Node %d (DSA)'%(n) )
    elif isinstance(nodes[n],mdpNode):
        legendInfo.append( 'Node %d (MDP)'%(n) )
    if isinstance(nodes[n],dqnNode):
        legendInfo.append( 'Node %d (DQN)'%(n) )
    else:
        pass
    
    txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T , axis=0).T ) )
plt.legend(legendInfo)
plt.xlabel('Step Number')
plt.ylabel('Cumulative Collisions')
plt.title( 'Cumulative Collisions Per Node')  
plt.grid(True)
                    
#plt.show()
plt.savefig('../dqnFig/CumulativeCollisions.png')
plt.savefig('../dqnFig/CumulativeCollisions.pdf')             
        
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
    plt.grid(True)

#plt.show()             
plt.savefig('../dqnFig/CumulativeReward.png')
plt.savefig('../dqnFig/CumulativeReward.pdf')        
#np.ceil
############### 3 Actions #################################
plt.figure(3)
#plt.figure(figsize=(80,10))
split = np.ceil(numNodes*1.0/2)

for n in range(0,numNodes):
  
    plt.subplot(split,2,n+1)        
    plt.plot( nodes[n].actionHistInd-1,'bo' ,fillstyle= 'none')
    plt.ylim(0,numChans)   # -1 for WAIT
    plt.xlabel('Step Number')
    plt.ylabel('Action Number')

    if   isinstance(nodes[n],legacyNode):
        titleLabel = 'Action Taken by Node %d (Legacy)'%(n)
    elif isinstance(nodes[n],hoppingNode):
        titleLabel = 'Action Taken by Node %d (Hopping)'%(n)
    elif   isinstance(nodes[n],imNode):
        titleLabel = 'Action Taken by Node %d (Intermittent)'%(n)
    elif isinstance(nodes[n],dsaNode):
        titleLabel = 'Action Taken by Node %d (DSA)'%(n)
    elif isinstance(nodes[n],mdpNode):
        titleLabel = 'Action Taken by Node %d (MDP)'%(n)
    else:
        titleLabel = 'Action Taken by Node %d (DQN)'%(n)   # no dsa
    plt.title(titleLabel)
    

#plt.show() 
plt.savefig('../dqnFig/Actions.png')
plt.savefig('../dqnFig/Actions.pdf')






    

############### 4 Packet Error Rate  #################################
timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                             1,numNodes )  
txPackets = np.array(txPackets).T
PER =  cumulativeCollisions / txPackets
PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots
    
plt.figure(4)
legendInfo = [ ]
for i in range(numNodes):
    if isinstance(nodes[i],legacyNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (Legacy)'%(i) )
    elif isinstance(nodes[i],hoppingNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (Hopping)'%(i) )
    elif isinstance(nodes[i],imNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (Intermittent)'%(i) )
    elif isinstance(nodes[i],dsaNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (DSA)'%(i) )
    elif isinstance(nodes[i],mdpNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (MDP)'%(i) )
    elif isinstance(nodes[i],dqnNode):
        plt.semilogy( PER[:,i] )
        legendInfo.append( 'Node %d (DQN)'%(i) )
    else:
        pass
plt.legend(legendInfo)
plt.xlabel('Step Number')
plt.ylabel('Cumulative Packet Error Rate')
plt.title( 'Cumulative Packet Error Rate')   
plt.grid(True)
                   
#plt.show()        
plt.savefig('../dqnFig/PER.png')
plt.savefig('../dqnFig/PER.pdf')        

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
if legendInfo:
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Loss Rate')
    plt.title( 'Cumulative Packet Loss Rate')                      
    plt.show() 
plt.grid(True)

#plt.show() 
plt.savefig('../dqnFig/PLR.png')
plt.savefig('../dqnFig/PLR.pdf')
############### END OF PLOT  ################################# 
        
    
    
    
    
    
    
    
# plot period
plt.figure(6)
plotPeriod = 400
iteration = 0.75*numSteps/plotPeriod
split = np.ceil(numNodes*1.0/2)    
for n in range(0,numNodes):
  
    plt.subplot(split,2,n+1)        
   
    temp = nodes[n].actionHistInd-1   
    # -1 for WAIT
    length = len(temp)   
    tempPeriod = np.zeros(plotPeriod)
    
    for m in range(length/4,length):   # last 3/4 
        tempPeriod[m%400] += temp[m]   
    tempPeriod =  tempPeriod*1.0/iteration
    
    isAction  = np.ones(plotPeriod) * -2
    nonAction = np.ones(plotPeriod) * -2
    
    for i in range(0,plotPeriod):
        if tempPeriod[i] < 0:
            nonAction[i] = temp[i]
        else:
            isAction[i] = temp[i]

    plt.plot(isAction,'bo' ,fillstyle= 'none')
    plt.plot(nonAction,'yo' ,fillstyle= 'none')
    plt.ylim(-1,numChans)  #-1 to show WAIT
    plt.xlabel('Step Number')
    plt.ylabel('Periodic Action Number')

    if   isinstance(nodes[n],legacyNode):
        titleLabel = 'Periodic Action of Node %d (Legacy)'%(n)
    elif   isinstance(nodes[n],hoppingNode):
        titleLabel = 'Periodic Action of Node %d (Hopping)'%(n)
    elif   isinstance(nodes[n],imNode):
        titleLabel = 'Periodic Action of Node %d (Intermittent)'%(n)
    elif isinstance(nodes[n],dsaNode):
        titleLabel = 'Periodic Action of Node %d (DSA)'%(n)
    elif isinstance(nodes[n],mdpNode):
        titleLabel = 'Periodic Action of Node %d (MDP)'%(n)
    else:
        titleLabel = 'Periodic Action of Node %d (DQN)'%(n)   # no dsa
    plt.title(titleLabel)


plt.show() 
plt.savefig('../dqnFig/peroidicActions.png')
plt.savefig('../dqnFig/peroidicActions.pdf')
    
    
    
    
    
    
    
    
