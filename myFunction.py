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
       # print "%s collide with %s"%(hopPattern, exsitHopChanList)
    return tag
        


import matplotlib.pyplot as plt

def myPlotProb(learnProbHist):
    plt.plot(learnProbHist)
    plt.title( 'Exploring Ratio') 
    plt.show()

    
def myPlotCollision(nodes, cumulativeCollisions):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    txPackets = [ ] 
    legendInfo = [ ]
    
    for n in range(0,len(nodes)):
        plt.plot(cumulativeCollisions[:,n])      # <<<<
        if isinstance(nodes[n],legacyNode):
            legendInfo.append( 'Node %d (Legacy)'%(n) )
        elif isinstance(nodes[n],hoppingNode):
            legendInfo.append( 'Node %d (Hopping)'%(n) )
        elif isinstance(nodes[n],imNode):
            legendInfo.append( 'Node %d (Intermittent)'%(n) )
        elif isinstance(nodes[n],poissonNode):
            legendInfo.append( 'Node %d (poisson)'%(n) )
        elif isinstance(nodes[n],dsaNode):
            legendInfo.append( 'Node %d (DSA)'%(n) )
        elif isinstance(nodes[n],mdpNode):
            legendInfo.append( 'Node %d (MDP)'%(n) )
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'dqn':
                legendInfo.append( 'Node %d (DQN)'%(n) )
            elif nodes[n].type == 'dqnDouble':
                legendInfo.append( 'Node %d (DQN-double)'%(n) )
            elif nodes[n].type == 'dqnPriReplay':
                legendInfo.append( 'Node %d (DQN-pr)'%(n) )
            elif nodes[n].type == 'dqnDuel':
                legendInfo.append( 'Node %d (DQN-duel)'%(n) )
            elif nodes[n].type == 'dqnRef':
                legendInfo.append( 'Node %d (DQN-Ref)'%(n) )
            elif nodes[n].type == 'dpg':
                legendInfo.append( 'Node %d (DPG)'%(n) )
            else:
                legendInfo.append( 'Node %d (undefined)'%(n) ) 
        else:
            legendInfo.append( 'Node %d (undefined)'%(n) )     
        txPackets.append( np.cumsum(np.sum(nodes[n].actionHist.T , axis=0).T ) )
        
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Collisions')
    plt.title( 'Cumulative Collisions Per Node')  
    plt.grid(True)
    plt.savefig('../dqnFig/CumulativeCollisions.png')
    plt.savefig('../dqnFig/CumulativeCollisions.pdf')
    return txPackets


def myPlotReward(nodes, cumulativeCollisions):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    from learningNodes.acNode      import acNode
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        if isinstance(nodes[n],mdpNode):
            plt.plot(nodes[n].cumulativeReward)
            legendInfo.append('Node %d (MDP)'%(n) )
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'dqn':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN)'%(n) )
            elif nodes[n].type == 'dqnDouble':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-double)'%(n) )
            elif nodes[n].type == 'dqnPriReplay':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-pr)'%(n) )
            elif nodes[n].type == 'dqnDuel':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-duel)'%(n) )
            elif nodes[n].type == 'dqnRef':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-Ref)'%(n) )
            elif nodes[n].type == 'dpg':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DPG)'%(n) )
            else:
                pass
        elif isinstance(nodes[n], acNode):
            plt.plot(nodes[n].cumulativeReward)
            legendInfo.append('Node %d (ac)'%(n) )
        else:
            pass

                
    if legendInfo:
        plt.legend(legendInfo)
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Reward')
        plt.title( 'Cumulative Reward Per Node')   
        plt.grid(True)            
    plt.savefig('../dqnFig/CumulativeReward.png')
    plt.savefig('../dqnFig/CumulativeReward.pdf')  
    
    
def myPlotAction(nodes, numChans):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    split = np.ceil( len(nodes)*1.0/2 )    
    for n in range(0,len(nodes)):      
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
        elif   isinstance(nodes[n],poissonNode):
            titleLabel = 'Action Taken by Node %d (poisson)'%(n)
        elif isinstance(nodes[n],dsaNode):
            titleLabel = 'Action Taken by Node %d (DSA)'%(n)
        elif isinstance(nodes[n],mdpNode):
            titleLabel = 'Action Taken by Node %d (MDP)'%(n)
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'dqn':
                titleLabel = 'Action Taken by Node %d (DQN)'%(n) 
            elif nodes[n].type == 'dqnDouble':
                titleLabel = 'Action Taken by Node %d (DQN-double)'%(n) 
            elif nodes[n].type == 'dqnPriReply':
                titleLabel = 'Action Taken by Node %d (DQN-pr)'%(n) 
            elif nodes[n].type == 'dqnDuel':
                titleLabel = 'Action Taken by Node %d (DQN-duel)'%(n) 
            elif nodes[n].type == 'dqnRef':
                titleLabel = 'Action Taken by Node %d (DQN-Ref)'%(n) 
            elif nodes[n].type == 'dpg':
                titleLabel = 'Action Taken by Node %d (DPG)'%(n) 
            else:
                titleLabel = 'Action Taken by Node %d (undefined)'%(n) 
        else:
            titleLabel = 'Action Taken by Node %d (undefined)'%(n) 
            
        plt.title(titleLabel)
    plt.savefig('../dqnFig/Actions.png')
    plt.savefig('../dqnFig/Actions.pdf')    
 
    
def myPlotOccupiedEnd(nodes, numChans, plotPeriod):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        tempPeriod = np.zeros(plotPeriod)
        x = range(length-plotPeriod,length)
        for m in x:
            tempPeriod[m - (length-plotPeriod)] = temp[m]
        
        if isinstance(nodes[n],legacyNode):
            plt.plot(  tempPeriod, x,'ko' ,fillstyle= 'full')
            legendInfo.append('Legacy')
        elif isinstance(nodes[n],hoppingNode):
            plt.plot(tempPeriod, x,'co' ,fillstyle= 'full')
            legendInfo.append('Hopping')
        elif isinstance(nodes[n],imNode):
            plt.plot(tempPeriod, x,'mo' ,fillstyle= 'full')
            legendInfo.append('Intermittent')
        elif isinstance(nodes[n],poissonNode):
            plt.plot(tempPeriod, x,'mo' ,fillstyle= 'full')
            legendInfo.append('poisson')
        elif isinstance(nodes[n],dsaNode):
            plt.plot( tempPeriod, x,'ro' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( tempPeriod, x,'go' ,fillstyle= 'full')
            legendInfo.append('MDP')
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'dqn':
                plt.plot(tempPeriod, x,'bo' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'dqnDouble':
                plt.plot( tempPeriod,'b+' ,fillstyle= 'none') 
            elif nodes[n].type == 'dqnPriReply':
                plt.plot( tempPeriod,'b^' ,fillstyle= 'none') 
            elif nodes[n].type == 'dqnDuel':
                plt.plot( tempPeriod,'bx' ,fillstyle= 'none') 
            elif nodes[n].type == 'dqnRef':
                plt.plot( tempPeriod,'bx' ,fillstyle= 'none') 
            elif nodes[n].type == 'dpg':
                plt.plot( tempPeriod,'bx' ,fillstyle= 'none') 
            else:
                plt.plot( tempPeriod, x,'bo' ,fillstyle= 'full')
                legendInfo.append('undefined')
        else:
            plt.plot( tempPeriod, x,'bo' ,fillstyle= 'full')
            legendInfo.append('undefined')
                
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(length-plotPeriod,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation of last %s steps'%(plotPeriod))
    plt.savefig('../dqnFig/Occupied.png')
    plt.savefig('../dqnFig/Occupied.pdf')


def myPlotOccupiedAll(nodes, numChans):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        x = range(0,length)
        
        if isinstance(nodes[n],legacyNode):
            plt.plot(  temp, x,'k.' ,fillstyle= 'full')
            legendInfo.append('Legacy')
        elif isinstance(nodes[n],hoppingNode):
            plt.plot(temp, x,'c.' ,fillstyle= 'full')
            legendInfo.append('Hopping')
        elif isinstance(nodes[n],imNode):
            plt.plot(temp, x,'m.' ,fillstyle= 'full')
            legendInfo.append('Intermittent')
        elif isinstance(nodes[n],poissonNode):
            plt.plot(temp, x,'m.' ,fillstyle= 'full')
            legendInfo.append('poisson')
        elif isinstance(nodes[n],dsaNode):
            plt.plot(temp, x,'r.' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( temp, x,'g.' ,fillstyle= 'full')
            legendInfo.append('MDP')
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'dqn':
                plt.plot(temp, x,'b.' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'dqnDouble':
                plt.plot( temp,'b+' ,fillstyle= 'none') 
                legendInfo.append('DQN-double')
            elif nodes[n].type == 'dqnPriReply':
                plt.plot( temp,'b^' ,fillstyle= 'none')
                legendInfo.append('DQN-PR')
            elif nodes[n].type == 'dqnDuel':
                plt.plot( temp,'bx' ,fillstyle= 'none') 
                legendInfo.append('DQN-Duel')
            elif nodes[n].type == 'dqnRef':
                plt.plot( temp,'bx' ,fillstyle= 'none') 
                legendInfo.append('DQN-Ref')
            elif nodes[n].type == 'dpg':
                plt.plot( temp,'bx' ,fillstyle= 'none') 
                legendInfo.append('DPG')
            else:
                plt.plot( temp,'bx' ,fillstyle= 'none') 
                legendInfo.append('undefined')
        else:
             plt.plot( temp,'bx' ,fillstyle= 'none') 
             legendInfo.append('undefined')
            
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(0,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation')
    plt.savefig('../dqnFig/Occupied-full.png')
    plt.savefig('../dqnFig/Occupied-full.pdf')     

    
def myPlotPER(nodes, numSteps, txPackets, cumulativeCollisions):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                                 1,len(nodes) )  
    txPackets = np.array(txPackets).T
    PER =  cumulativeCollisions / txPackets
    PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots    
    legendInfo = [ ]
    for i in range(len(nodes)):
        if isinstance(nodes[i],legacyNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (Legacy)'%(i) )
        elif isinstance(nodes[i],hoppingNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (Hopping)'%(i) )
        elif isinstance(nodes[i],imNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (Intermittent)'%(i) )
        elif isinstance(nodes[i],poissonNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (poisson)'%(i) )
        elif isinstance(nodes[i],dsaNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (DSA)'%(i) )
        elif isinstance(nodes[i],mdpNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (MDP)'%(i) )
        elif isinstance(nodes[i],dqnNode):
            if nodes[i].type == 'dqn':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN)'%(i) )
            elif nodes[i].type == 'dqnDouble':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-double)'%(i) )
            elif nodes[i].type == 'dqnPriReplay':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-pr)'%(i) )
            elif nodes[i].type == 'dqnDuel':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-duel)'%(i) )
            elif nodes[i].type == 'dqnRef':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-Ref)'%(i) )
            elif nodes[i].type == 'dpg':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DPG)'%(i) )
            else:
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (undefined)'%(i) )
        else:
             plt.semilogy( PER[:,i] )
             legendInfo.append( 'Node %d (undefined)'%(i) )
    
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Error Rate')
    plt.title( 'Cumulative Packet Error Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PER.png')
    plt.savefig('../dqnFig/PER.pdf') 

    return PER, PLR


def myPlotPLR(nodes, PLR):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    legendInfo = [ ]
    for i in range(len(nodes)):
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
        plt.grid(True)                     
        plt.show() 
    plt.savefig('../dqnFig/PLR.png')
    plt.savefig('../dqnFig/PLR.pdf')  
    
    
def myPlotThroughput(nodes, PLR):
    from learningNodes.dqnNode     import dqnNode
    from learningNodes.mdpNode     import mdpNode
    legendInfo = [ ]
    for i in range(len(nodes)):
        if isinstance(nodes[i],mdpNode):
            plt.semilogy( 1- PLR[:,i] )
            legendInfo.append( 'Node %d (MDP)'%(i) )
        elif isinstance(nodes[i],dqnNode):
            plt.semilogy( 1- PLR[:,i] )
            legendInfo.append( 'Node %d (DQN)'%(i) )
    if legendInfo:
        plt.xlabel('Step Number')
        plt.ylabel('Cumulative Througput')
        plt.title( 'Cumulative Throughput') 
        plt.grid(True)                     
        plt.show() 
    plt.savefig('../dqnFig/TP.png')
    plt.savefig('../dqnFig/TP.pdf')  
    
    
def myPlotCost(nodes):
    from learningNodes.dqnNode     import dqnNode
    legendInfo = [ ]
    for i in range(len(nodes)):
        if isinstance(nodes[i],dqnNode): 
            plt.plot( nodes[i].dqn_.cost_his )
            legendInfo.append( 'Node %d (DQN)'%(i) )
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


