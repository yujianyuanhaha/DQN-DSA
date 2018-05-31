#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 02:57:37 2018

@author: Jet
"""

# functions
import numpy as np
from legacyNode  import legacyNode
#from mdpNode     import mdpNode
from hoppingNode import hoppingNode
#from dqnNode     import dqnNode   #
from dsaNode     import dsaNode 
from imNode     import imNode  




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
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
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
        elif isinstance(nodes[n],dsaNode):
            legendInfo.append( 'Node %d (DSA)'%(n) )
        elif isinstance(nodes[n],mdpNode):
            legendInfo.append( 'Node %d (MDP)'%(n) )
        if isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'raw':
                legendInfo.append( 'Node %d (DQN)'%(n) )
            elif nodes[n].type == 'double':
                legendInfo.append( 'Node %d (DQN-double)'%(n) )
            elif nodes[n].type == 'priReplay':
                legendInfo.append( 'Node %d (DQN-pr)'%(n) )
            elif nodes[n].type == 'duel':
                legendInfo.append( 'Node %d (DQN-duel)'%(n) )
            else:
                pass
        else:
            pass       
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
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        if isinstance(nodes[n],mdpNode):
            plt.plot(nodes[n].cumulativeReward)
            legendInfo.append('Node %d (MDP)'%(n) )
        elif isinstance(nodes[n],dqnNode):
            if nodes[n].type == 'raw':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN)'%(n) )
            if nodes[n].type == 'double':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-double)'%(n) )
            if nodes[n].type == 'priReplay':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-pr)'%(n) )
            if nodes[n].type == 'duel':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-duel)'%(n) )
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
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
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
        elif isinstance(nodes[n],dsaNode):
            titleLabel = 'Action Taken by Node %d (DSA)'%(n)
        elif isinstance(nodes[n],mdpNode):
            titleLabel = 'Action Taken by Node %d (MDP)'%(n)
        else:
            if nodes[n].type == 'raw':
                titleLabel = 'Action Taken by Node %d (DQN)'%(n) 
            elif nodes[n].type == 'double':
                titleLabel = 'Action Taken by Node %d (DQN-double)'%(n) 
            elif nodes[n].type == 'pr':
                titleLabel = 'Action Taken by Node %d (DQN-pr)'%(n) 
            elif nodes[n].type == 'duel':
                titleLabel = 'Action Taken by Node %d (DQN-duel)'%(n) 
            else:
                pass
            
        plt.title(titleLabel)
    plt.savefig('../dqnFig/Actions.png')
    plt.savefig('../dqnFig/Actions.pdf')    
 
    
def myPlotOccupiedEnd(nodes, numChans, plotPeriod):
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
    legendInfo = [ ]
    for n in range(0,len(nodes)):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        tempPeriod = np.zeros(plotPeriod)
        x = range(length-plotPeriod,length)
        for m in x:
            tempPeriod[m - (length-plotPeriod)] = temp[m]
        
        if isinstance(nodes[n],legacyNode):
            plt.plot(  tempPeriod, x,'k.' ,fillstyle= 'full')
            legendInfo.append('Legacy')
        elif isinstance(nodes[n],hoppingNode):
            plt.plot(tempPeriod, x,'c.' ,fillstyle= 'full')
            legendInfo.append('Hopping')
        elif isinstance(nodes[n],imNode):
            plt.plot(tempPeriod, x,'m.' ,fillstyle= 'full')
            legendInfo.append('Intermittent')
        elif isinstance(nodes[n],dsaNode):
            plt.plot( tempPeriod, x,'r.' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( tempPeriod, x,'g.' ,fillstyle= 'full')
            legendInfo.append('MDP')
        else:
            if nodes[n].type == 'raw':
                plt.plot(tempPeriod, x,'b.' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'double':
                plt.plot( tempPeriod,'b+' ,fillstyle= 'none') 
            elif nodes[n].type == 'pr':
                plt.plot( tempPeriod,'b^' ,fillstyle= 'none') 
            elif nodes[n].type == 'duel':
                plt.plot( tempPeriod,'bx' ,fillstyle= 'none') 
            else:
                pass
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(length-plotPeriod,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation of last 100 steps')
    plt.savefig('../dqnFig/Occupied.png')
    plt.savefig('../dqnFig/Occupied.pdf')


def myPlotOccupiedAll(nodes, numChans):
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
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
        elif isinstance(nodes[n],dsaNode):
            plt.plot(temp, x,'r.' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( temp, x,'g.' ,fillstyle= 'full')
            legendInfo.append('MDP')
        else:
            if nodes[n].type == 'raw':
                plt.plot(temp, x,'b.' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'double':
                plt.plot( temp,'b+' ,fillstyle= 'none') 
            elif nodes[n].type == 'pr':
                plt.plot( temp,'b^' ,fillstyle= 'none') 
            elif nodes[n].type == 'duel':
                plt.plot( temp,'bx' ,fillstyle= 'none') 
            else:
                pass
            
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(0,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
    plt.title('Channel occupation')
    plt.savefig('../dqnFig/Occupied-full.png')
    plt.savefig('../dqnFig/Occupied-full.pdf')     

    
def myPlotPER(nodes, numSteps, txPackets, cumulativeCollisions):
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
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
        elif isinstance(nodes[i],dsaNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (DSA)'%(i) )
        elif isinstance(nodes[i],mdpNode):
            plt.semilogy( PER[:,i] )
            legendInfo.append( 'Node %d (MDP)'%(i) )
        elif isinstance(nodes[i],dqnNode):
            if nodes[i].type == 'raw':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN)'%(i) )
            elif nodes[i].type == 'double':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-double)'%(i) )
            elif nodes[i].type == 'priReplay':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-pr)'%(i) )
            if nodes[i].type == 'duel':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-duel)'%(i) )
            else:
                pass
        else:
            pass
    plt.legend(legendInfo)
    plt.xlabel('Step Number')
    plt.ylabel('Cumulative Packet Error Rate')
    plt.title( 'Cumulative Packet Error Rate')   
    plt.grid(True)      
    plt.savefig('../dqnFig/PER.png')
    plt.savefig('../dqnFig/PER.pdf') 
    return PLR


def myPlotPLR(nodes, PLR):
    from dqnNode     import dqnNode
    from mdpNode     import mdpNode
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
    

def myPlot(nodes, numChans, numSteps, learnProbHist,cumulativeCollisions):
    
    from legacyNode  import legacyNode
    from mdpNode     import mdpNode
    from hoppingNode import hoppingNode
    from dqnNode     import dqnNode   #
    from dsaNode     import dsaNode 
    from imNode     import imNode 
        
        
    plt.figure(7)
    plt.plot(learnProbHist)
    plt.title( 'Exploring Ratio') 
    plt.show()
    #
    #plt.figure(2)
    #nodes[0].dqn_.plot_cost()
    #
    #
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
    numNodes = len(nodes)
    
    
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
            if nodes[n].type == 'raw':
                legendInfo.append( 'Node %d (DQN)'%(n) )
            elif nodes[n].type == 'double':
                legendInfo.append( 'Node %d (DQN-double)'%(n) )
            elif nodes[n].type == 'priReplay':
                legendInfo.append( 'Node %d (DQN-pr)'%(n) )
            elif nodes[n].type == 'duel':
                legendInfo.append( 'Node %d (DQN-duel)'%(n) )
            else:
                pass
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
            if nodes[n].type == 'raw':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN)'%(n) )
            if nodes[n].type == 'double':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-double)'%(n) )
            if nodes[n].type == 'priReplay':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-pr)'%(n) )
            if nodes[n].type == 'duel':
                plt.plot(nodes[n].cumulativeReward)
                legendInfo.append('Node %d (DQN-duel)'%(n) )
            else:
                pass
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
            if nodes[n].type == 'raw':
                titleLabel = 'Action Taken by Node %d (DQN)'%(n) 
            elif nodes[n].type == 'double':
                titleLabel = 'Action Taken by Node %d (DQN-double)'%(n) 
            elif nodes[n].type == 'pr':
                titleLabel = 'Action Taken by Node %d (DQN-pr)'%(n) 
            elif nodes[n].type == 'duel':
                titleLabel = 'Action Taken by Node %d (DQN-duel)'%(n) 
            else:
                pass
            
        plt.title(titleLabel)
        
    
    #plt.show() 
    plt.savefig('../dqnFig/Actions.png')
    plt.savefig('../dqnFig/Actions.pdf')
    
    
    
        ############### 3-B  Occupied #################################
    plt.figure(4)
    plotPeriod = 100
    split = np.ceil(numNodes*1.0/2)
    legendInfo = [ ]
    for n in range(0,numNodes):
        temp = nodes[n].actionHistInd-1
        length = len(temp) 
        tempPeriod = np.zeros(plotPeriod)
        x = range(length-plotPeriod,length)
        for m in x:
            tempPeriod[m%100] += temp[m]
        
        if isinstance(nodes[n],legacyNode):
            plt.plot(  tempPeriod, x,'k.' ,fillstyle= 'full')
            legendInfo.append('Legacy')
        elif isinstance(nodes[n],hoppingNode):
            plt.plot(tempPeriod, x,'c.' ,fillstyle= 'full')
            legendInfo.append('Hopping')
        elif isinstance(nodes[n],imNode):
            plt.plot(tempPeriod, x,'m.' ,fillstyle= 'full')
            legendInfo.append('Intermittent')
        elif isinstance(nodes[n],dsaNode):
            plt.plot( tempPeriod, x,'r.' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( tempPeriod, x,'g.' ,fillstyle= 'full')
            legendInfo.append('MDP')
        else:
            if nodes[n].type == 'raw':
                plt.plot(tempPeriod, x,'b.' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'double':
                plt.plot( tempPeriod,'b+' ,fillstyle= 'none') 
            elif nodes[n].type == 'pr':
                plt.plot( tempPeriod,'b^' ,fillstyle= 'none') 
            elif nodes[n].type == 'duel':
                plt.plot( tempPeriod,'bx' ,fillstyle= 'none') 
            else:
                pass
            
       # plt.title(titleLabel)
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(length-plotPeriod,length)
    plt.xlabel('time slot')
    plt.ylabel('channel selection')
        
    
    #plt.show() 
    plt.savefig('../dqnFig/Occupied.png')
    plt.savefig('../dqnFig/Occupied.pdf')
    
    
            ############### 3-C  Occupied Full #################################
    plt.figure(5)

    legendInfo = [ ]
    for n in range(0,numNodes):
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
        elif isinstance(nodes[n],dsaNode):
            plt.plot(temp, x,'r.' ,fillstyle= 'full')
            legendInfo.append('DSA')
        elif isinstance(nodes[n],mdpNode):
            plt.plot( temp, x,'g.' ,fillstyle= 'full')
            legendInfo.append('MDP')
        else:
            if nodes[n].type == 'raw':
                plt.plot(temp, x,'b.' ,fillstyle= 'full')
                legendInfo.append('DQN')
            elif nodes[n].type == 'double':
                plt.plot( temp,'b+' ,fillstyle= 'none') 
            elif nodes[n].type == 'pr':
                plt.plot( temp,'b^' ,fillstyle= 'none') 
            elif nodes[n].type == 'duel':
                plt.plot( temp,'bx' ,fillstyle= 'none') 
            else:
                pass
            
       # plt.title(titleLabel)
    plt.legend(legendInfo,loc='upper right', prop={'size': 9})
    plt.xlim(0, numChans+1)   # -1 for WAIT
    plt.ylim(0,length)
    plt.xlabel('channel selection')
    plt.ylabel('time slot')
        
    
    #plt.show() 
    plt.savefig('../dqnFig/Occupied-full.png')
    plt.savefig('../dqnFig/Occupied-full.pdf')
        
    
    ############### 5 Packet Error Rate  #################################
    timeSlots = np.matlib.repmat( np.arange(1,numSteps+1)[np.newaxis].T  ,
                                 1,numNodes )  
    txPackets = np.array(txPackets).T
    PER =  cumulativeCollisions / txPackets
    PLR = (cumulativeCollisions + timeSlots - txPackets) /timeSlots
        
    plt.figure(6)
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
            if nodes[n].type == 'raw':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN)'%(i) )
            elif nodes[n].type == 'double':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-double)'%(i) )
            elif nodes[n].type == 'priReplay':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-pr)'%(i) )
            if nodes[n].type == 'duel':
                plt.semilogy( PER[:,i] )
                legendInfo.append( 'Node %d (DQN-duel)'%(i) )
            else:
                pass
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
    
    ############### 6 Packet Loss Rate  #################################
    plt.figure(7)
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
        plt.grid(True)                     
        plt.show() 
        
    
    #plt.show() 
    plt.savefig('../dqnFig/PLR.png')
    plt.savefig('../dqnFig/PLR.pdf')
    ############### END OF PLOT  ################################# 
            
        
        
        
        
        
        
        
    # plot period
    plt.figure(8)
    plotPeriod = 400
    
    split = np.ceil(numNodes*1.0/2)    
    for n in range(0,numNodes):
      
        plt.subplot(split,2,n+1)        
       
        temp = nodes[n].actionHistInd-1   
        # -1 for WAIT
        length = len(temp)   
        tempPeriod = np.zeros(plotPeriod)
        
        for m in range(length-plotPeriod,length):   # last 3/4 
            tempPeriod[m%400] += temp[m]
        
        isAction  = np.ones(plotPeriod) * -2
        nonAction = np.ones(plotPeriod) * -2
        
        for i in range(0,plotPeriod):
            if tempPeriod[i] < 0:
                nonAction[i] = tempPeriod[i]
            else:
                isAction[i] = tempPeriod[i]
    
        plt.plot(isAction,'bo' ,fillstyle= 'none')
        plt.plot(nonAction,'yo' ,fillstyle= 'none')
        plt.ylim(-1,numChans)  #-1 to show WAIT
        plt.xlabel('Step Number')
        plt.ylabel('Last 400 Action Number')
    
        if   isinstance(nodes[n],legacyNode):
            titleLabel = 'Last 400 Action of Node %d (Legacy)'%(n)
        elif   isinstance(nodes[n],hoppingNode):
            titleLabel = 'Last 400 Action of Node %d (Hopping)'%(n)
        elif   isinstance(nodes[n],imNode):
            titleLabel = 'Last 400 Action of Node %d (Intermittent)'%(n)
        elif isinstance(nodes[n],dsaNode):
            titleLabel = 'Last 400 Action of Node %d (DSA)'%(n)
        elif isinstance(nodes[n],mdpNode):
            titleLabel = 'Last 400 Action of Node %d (MDP)'%(n)
        else:
            titleLabel = 'Last 400 Action of Node %d (DQN)'%(n)   # no dsa
        plt.title(titleLabel)
    
    
    #plt.show() 
    plt.savefig('../dqnFig/peroidicActions.png')
    plt.savefig('../dqnFig/peroidicActions.pdf')
    
    
    





####################### Test Unit ############################################
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


