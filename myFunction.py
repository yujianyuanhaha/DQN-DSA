#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 02:57:37 2018

@author: Jet
"""

# functions
import numpy as np
from dumbNodes.legacyNode  import legacyNode
from dumbNodes.hoppingNode import hoppingNode
from dumbNodes.dsaNode     import dsaNode 
from dumbNodes.imNode      import imNode 
from stochasticNodes.poissonNode import poissonNode  



def update(nodes, numChans, actions, collisions, collisionTally, absent):
    numNodes = len(nodes)
    observedStates = np.zeros((numNodes,numChans))

    for n in range(0,numNodes):
        collisions[n] = 0
        
        for nn in range(0,numNodes):
            if nn != n:
                # case 1, duplex collision
                if nodes[nn].hiddenDuplexCollision[n]:
                    if  np.sum( actions[n,:] + actions[nn,:])> 1:
                        collisions[n]         = 1
                        collisionTally[n,nn] += 1
                        observedStates[n,:]   = np.ones(numChans)   # all illegal 
                        # take duplex col node as "full channel user", only have to is wait
                        # print "duplex collision"                                  
                else:
                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)  
                        
                # case 2, same channel collision                        
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
                  and not nodes[nn].exposedSpatialReuse[n]:    # if nodes[nn].exposedSpatialReuse[n] == 0
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                    
                    
    # calculate absent - environment got slot while learning node choose to wait                
    priUser = 0
    learnNodeIndex = [ ]                
    for n in range(0,numNodes):
        if nodes[n].hyperType == "learning":  #
            learnNodeIndex.append(n)
        else:            
            priUser  += actions[n,:]
    if len(learnNodeIndex) > 1:
        pass
#        print "multi-agent ! Absent metric fail"
    learnNodeIndex = learnNodeIndex[0]
    
    openSlot  = ( np.sum(priUser) < numChans )  
    learnWait = ( np.sum(actions[learnNodeIndex])  == 0 )   #
    if openSlot and learnWait:   # a bit redundency but 
        absent += 1
 
    return collisions, absent, collisionTally, observedStates
    


# noise to random flip bit of observation
def noise(observation, noiseErrorProb, noiseFlipNum):
    
    temp = observation
    if random.random() < noiseErrorProb:
        for k in range(noiseFlipNum):   # 0, 1
            ind =  random.randint(0, len(observation)-1)
            temp[ind] = 1- temp[ind]
    observation = temp
    
    return observation


# FIFO, blend new observation into observations
def updateStack(observationS, observation):
    
    temp = observationS
    temp2 = len(observation)
    M = len(observationS)/ len(observation)
    observationS[ (M-1)*temp2 : ] = observation
    observationS[ : (M-1)*temp2 ] = temp[ : (M-1)*temp2 ]
    
    return observationS


def partialPad(observation, t, poStepNum, poBlockNum, padValue):
    
    temp = observation
    numChans = len(observation)
    rollInd = t * poStepNum % numChans
    for i in range(poBlockNum):
        temp[(rollInd+i)%numChans] = padValue       
    observation = temp
    
    return observation
            


def partialObserve(observation, t, poStepNum, poSeeNum):
    import numpy as np
    temp = np.zeros(poSeeNum)
    numChans = len(observation)
    rollInd = t * poStepNum % numChans
    for i in range(poSeeNum):
        temp[i] = observation[(rollInd+i)%numChans]       
    partialObservation = temp
    
    return partialObservation


"with action, other unseen pad as value TWO"
def partialObserveAction(observation, t, poStepNum, poSeeNum, action):
    import numpy as np
    padValue = 2   #
    numChans = len(observation)
    temp = observation
    rollInd = t * (poStepNum+1) % numChans 
    for i in range(numChans-poSeeNum):
        temp[(rollInd+i)%numChans] = padValue

    if np.sum(action):
        indexAction = int(np.where(action==1)[0])   # ugly
        temp[indexAction] = 1
            
    partialObservation = temp
    
    # for list, copy changes, original also change!!    
#    print("full observation %s " % observation)
#    print("action %s" % action)
#    print("partial observation %s" % partialObservation)
    
    return partialObservation


# [~,stateIndex] = ismember(self.stateHist[stepNum-1,:], self.states,'rows') 

def ismember(a,B):
    t = 0           
    for j in range(0, np.shape(B)[0]):
        if all(a == B[j,:]):
            t = j
            break
    return t

# if no match, return 0
# possible one line function    
                    
def channelAssignment(nodeTypes, hoppingWidth, numChans):        
    # random assign channel or choose example set
    # hopping is kind of combination of imNode, legecy also a special kind of legacy   
    # first sort a copy of input NodeTye array, legacy/im first; hoppingNext
    nodeTypes_ = nodeTypes
    nodeTypes_.sort()
#    print nodeTypes_
    
    numNodes       = len(nodeTypes_)
    legacyNodeNum  = 0
    hoppingNodeNum = 0
    imNodeNum      = 0    
    availChanList = range(numChans)
    legacyChanList = [ ]
    imChanList = [ ]
  
    # Assign Legacy and Intermittent
    for k in range(0,numNodes):
        if   nodeTypes_[k] == 0:
            legacyNodeNum        += 1
            index = random.randint(0,len(availChanList)-1)
            legacyChanList.append(availChanList[index])
            del availChanList[index]
        elif nodeTypes_[k] == 1:
            hoppingNodeNum       += 1

        elif nodeTypes_[k] == 6:
            imNodeNum            += 1
            index = random.randint(0,len(availChanList)-1)
            imChanList.append(availChanList[index])
            del availChanList[index]
        else:
            print "nodeTypes from 0 - 6"
            
    assert len(hoppingWidth) == hoppingNodeNum, "hopWidth array does not match num of hop node"
    
    # if hoppingWidth include 2/ 3, also collision
            
    # capacity check
    occupiedHopping = 0
    for i in range(len(hoppingWidth)):
        occupiedHopping += 1.0/hoppingWidth[i]
    occupied = legacyNodeNum + imNodeNum + occupiedHopping
    utilization = occupied * 1.0/ numChans
    assert utilization <= 1, "capacity overflow"        
    
    hoppingChanList = []    
    for i in range(hoppingNodeNum):       
        temp = generateHopPattern(availChanList,hoppingWidth[i])
        if hoppingChanList != []:  # if not empty
            while not isCollisonFree(temp, hoppingChanList):
                temp = generateHopPattern(availChanList,hoppingWidth[i])
        hoppingChanList.append(temp)
    
    return legacyChanList, imChanList, hoppingChanList, utilization
    


import random    
def generateHopPattern(availChanList, hopWidth):
    availHopChanList = availChanList
    temp = []
    for l in range(0,hopWidth):
        index = random.randint(0,len(availHopChanList)-1)
        temp.append(availHopChanList[index])
        del availHopChanList[index]
    availChanList += temp   # unknow issue, need restore   
    return temp

    
import fractions  
def isCollisonFree(hopPattern, exsitHopChanList):
    tag = True
    for i in range( len(exsitHopChanList) ):
        temp = exsitHopChanList[i]
        a = len(hopPattern)
        b = len(temp)
        lcm = a*b/fractions.gcd(a,b)
        hopPattern_ = hopPattern * (lcm/a)
        temp_ = temp * (lcm/b)        
        for j in range(lcm):
            if temp_[j] == hopPattern_[j]:
                tag = False
                break
    return tag
        


import matplotlib.pyplot as plt

def myPlotProb(learnProbHist):
    plt.plot(learnProbHist)
    plt.title( 'Exploring Ratio') 
    plt.show()


def myGetTxPackets(nodes, cumulativeCollisions):
    txPackets = [ ]
    for n in range(0,len(nodes)):
        txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T , axis=0).T ) )
    return txPackets

    
def myPlotCollision(nodes, cumulativeCollisions):

#    txPackets = [ ] 
    legendInfo = [ ]
    
    for n in range(0,len(nodes)):
        plt.plot(cumulativeCollisions[:,n])      # <<<<
        legendInfo.append( '%d %s'%(n, nodes[n].type) )
        
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Collisions')
    plt.title( 'Cumulative Collisions Per Node')  
    plt.grid(True)
    plt.savefig('../dqnFig/CumulativeCollisions.png')
    plt.savefig('../dqnFig/CumulativeCollisions.pdf')
#    return txPackets


def myPlotReward(nodes, cumulativeCollisions):

    legendInfo = [ ]
    for n in range(0,len(nodes)):
        if nodes[n].hyperType == 'learning':
            plt.plot(nodes[n].cumulativeReward)
            legendInfo.append('%d %s'%(n, nodes[n].type ))       

               
    if legendInfo:
        plt.legend(legendInfo)
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Reward')
        plt.title( 'Cumulative Reward Per Node')   
        plt.grid(True)            
    plt.savefig('../dqnFig/CumulativeReward.png')
    plt.savefig('../dqnFig/CumulativeReward.pdf')  
    
    
def myPlotAction(nodes, numChans):
    split = np.ceil( len(nodes)*1.0/2 )    
    for n in range(0,len(nodes)):      
        plt.subplot(split,2,n+1)        
        plt.plot( nodes[n].actionHistInd-1,'bo' ,fillstyle= 'none')
        plt.ylim(0,numChans)   # -1 for WAIT
        plt.xlabel('Step Number')
        plt.ylabel('Action Number')
        
        
        titleLabel = 'Action Taken by Node %d %s'%(n,nodes[n].type )
        plt.title(titleLabel)
                    
    plt.savefig('../dqnFig/Actions.png')
    plt.savefig('../dqnFig/Actions.pdf')    
 
    
def myPlotOccupiedEnd(nodes, numChans, plotPeriod):

    legendInfo = [ ]
    for n in range(0,len(nodes)):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        tempPeriod = np.zeros(plotPeriod)
        x = range(length-plotPeriod,length)
        for m in x:
            tempPeriod[m - (length-plotPeriod)] = temp[m]
            
        plt.scatter( tempPeriod, x)
        legendInfo.append(nodes[n].type)
          
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(length-plotPeriod,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation of last %s steps'%(plotPeriod))
    plt.savefig('../dqnFig/Occupied.png')
    plt.savefig('../dqnFig/Occupied.pdf')


def myPlotOccupiedAll(nodes, numChans):
    
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        x = range(0,length)
                
        plt.scatter(  temp, x)
        legendInfo.append(nodes[n].type)
                    
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(0,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation')
    plt.savefig('../dqnFig/Occupied-full.png')
    plt.savefig('../dqnFig/Occupied-full.pdf')     



def myCalculatePER(nodes, numSteps, txPackets, cumulativeCollisions):

    timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                                 1,len(nodes) )  
    txPackets = np.array(txPackets).T
    PER =  cumulativeCollisions / txPackets
    PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots # NOT ABSOLUTE FAIR, prefer throughput
    return PER, PLR


def myCalculatePFR(nodes, numSteps, cumulativeCollisions, cumulativeAbsents):

    timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                                 1,len(nodes) )  
#    txPackets = np.array(txPackets).T
    PCR =  cumulativeCollisions / timeSlots
    PAR =  cumulativeAbsents    /timeSlots # NOT ABSOLUTE FAIR, prefer throughput
    PFR = PCR + PAR
    return PFR, PCR, PAR    
    
def myPlotPER(nodes, PER):
    
    legendInfo = [ ]
    for i in range(len(nodes)):
        plt.semilogy( PER[:,i] )
        legendInfo.append( '%d %s'%(i,nodes[i].type) )
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Error Rate')
    plt.title( 'Cumulative Packet Error Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PER.png')
    plt.savefig('../dqnFig/PER.pdf') 



def myPlotPLR(nodes, PLR):

    legendInfo = [ ]
    for i in range(len(nodes)):
            plt.semilogy( PLR[:,i] )
            legendInfo.append( '%d %s'%(i, nodes[i].type) )

    if legendInfo:
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Packet Loss Rate')
        plt.title( 'Cumulative Packet Loss Rate') 
        plt.grid(True)                     
        plt.show() 
    plt.savefig('../dqnFig/PLR.png')
    plt.savefig('../dqnFig/PLR.pdf')  
    
    
def myPlotPFR(nodes, PFR):
    
    legendInfo = [ ]
    for i in range(len(nodes)):
        plt.semilogy( PFR[:,i] )
        legendInfo.append( '%d %s'%(i,nodes[i].type) )
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Failure Rate')
    plt.title( 'Cumulative Packet Failure Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PFR.png')
    plt.savefig('../dqnFig/PFR.pdf') 
    
def myPlotPCR(nodes, PCR):
    
    legendInfo = [ ]
    for i in range(len(nodes)):
        plt.semilogy( PCR[:,i] )
        legendInfo.append( '%d %s'%(i,nodes[i].type) )
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Collision Rate')
    plt.title( 'Cumulative Packet Collision Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PCR.png')
    plt.savefig('../dqnFig/PCR.pdf') 

    
    
    
def myPlotPAR(nodes, PAR):
    
    legendInfo = [ ]
    for i in range(len(nodes)):
        plt.semilogy( PAR[:,i] )
        legendInfo.append( '%d %s'%(i,nodes[i].type) )
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Absent Rate')
    plt.title( 'Cumulative Packet Absent Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PAR.png')
    plt.savefig('../dqnFig/PAR.pdf') 
    
    
    
def myPlotPFCAR(learningNodeIndex, PFR, PCR, PAR):
    
    legendInfo = [ ]
    plt.semilogy( PFR[:,learningNodeIndex] )
    legendInfo.append("Failure Rate")
    plt.semilogy( PCR[:,learningNodeIndex] )
    legendInfo.append("Collision Rate")
    plt.semilogy( PAR[:,learningNodeIndex] )
    legendInfo.append("Absent Rate")
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Rate')
    plt.title( 'Cumulative Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PFCAR.png')
    plt.savefig('../dqnFig/PFCAR.pdf') 
    
    
def myPlotThroughput(nodes, cumulativeCollisions, txPackets, optimalTP, numSteps):

    legendInfo = [ ]
    Throughput = ( txPackets - cumulativeCollisions.T ).sum(axis = 0) * 1.0 / (optimalTP * numSteps)
    for i in range(len(nodes)):
        plt.semilogy(Throughput )
        legendInfo.append( '%d %s'%(i, nodes[i].type) )
    if legendInfo:
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Througput')
        plt.title( 'Cumulative Throughput') 
        plt.grid(True)                     
        plt.show() 
    plt.savefig('../dqnFig/TP.png')
    plt.savefig('../dqnFig/TP.pdf')
    
    return Throughput
    
    
def myPlotCost(nodes):
    from learningNodes.dqnNode     import dqnNode
    legendInfo = [ ]
    for i in range(len(nodes)):
        if isinstance(nodes[i],dqnNode): 
            plt.plot( nodes[i].dqn_.cost_his )
            legendInfo.append( '%d %s'%(i, nodes[i].type) )
    if legendInfo:
        plt.xlabel('Step Number')
        plt.ylabel('Cost')
        plt.title( 'Cost') 
        plt.grid(True)                     
        plt.show() 
    plt.savefig('../dqnFig/cost.png')
    plt.savefig('../dqnFig/cost.pdf')  
    
    

'''####################### Test Unit ############################################ '''
if __name__ == '__main__':
#    t = generateHopPattern([3,8,4,5], 2)
#    print t
#    t2 = isCollisonFree([2,3], [[1,4],[5,6,7]])  # True
#    print t2
#    t3 = isCollisonFree([2,3], [[1,4],[3,5,6]])  #False
#    print t3
#     t4 = isCollisonFree([1,2], [[3,2,1]])  #False
#     print t4
    
#    a,b,c,d = channelAssignment([0,0,6,1], [2],5)
#    print a,b,c,d  #0.7
#    a,b,c,d = channelAssignment([0,0,6,1,1], [2,2],5)
#    print a,b,c,d  #0.8
    a,b,c,d = channelAssignment([0,0,6,1,1], [3,3],8)
    # even-odd rule,  crazy
    print a,b,c,d  #5/6


