
for t in range(0,numSteps):
    
    ################ Determination of next action for each node ##############
    for n in range(0,numNodes):
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode): #or isinstance(nodes[n],ddpgNode) :
            ticDqnAction  = time.time()
            observation = observedStates[n,:]
            actions[n,:], actionScalar = nodes[n].getAction(t, observation)  ###########
#            if not np.sum(actions[n,:] ):
#                print "dqnNode WAIT"
            tocDqnAction  = time.time()
        elif isinstance(nodes[n],mdpNode):
            ticMdpAction  = time.time()
            actions[n,:] = nodes[n].getAction(t)
            tocMdpAction  = time.time()
        else:    
            actions[n,:] = nodes[n].getAction(t)
        assert not any(np.isnan(actions[n,:])), "ERROR! action is Nan"


    if simulationScenario.scenarioType != 'fixed':
         simulationScenario.updateScenario(nodes,legacyNodeIndicies, t)

    ################# Determining observations, collisions, rewards, and policies (where applicable)
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
                        # think duplex col node as "full channel user", only have to is wait
                        # print "duplex collision"                                  
                else:
                    observedStates[n,:] = (observedStates[n,:] + actions[nn,:] > 0)   # partial obseravtion
                        
                # case 2, same channel collision                        
                if np.sum(actions[n,:]) > 0 \
                  and any( np.array( actions[n,:] + actions[nn,:])> 1 ) \
                  and not nodes[nn].exposedSpatialReuse[n]:    # if nodes[nn].exposedSpatialReuse[n] == 0
                    collisions[n]         = 1
                    collisionTally[n,nn] += 1
                      
                    
        if isinstance(nodes[n],dsaNode):
            nodes[n].updateState(observedStates[n,:],t)
                    
        if isinstance(nodes[n],mdpNode):
            ticMdpLearn = time.time()
            reward = nodes[n].getReward(collisions[n],t,isWait)
            # additive noise to flip certain bit of observation
            temp = observedStates[n,:]
            if random.random() < noiseErrorProb:
                for k in range(noiseFlipNum):   # 0, 1
                    ind =  random.randint(0, numChans-1)
                    temp[ind] = 1- temp[ind]
            observedStates[n,:] = temp
            # yes, it did effect on performance under e.g. [0,1,2,4]
            
            if PartialObservation == 'rollOver':
                rollInd = t * poStepNum % numChans
                for i in range(poBlockNum):
                    temp[(rollInd+i)%numChans] = 0       
            observedStates[n,:] = temp
            # 20% PER, unbearable    
                        
            nodes[n].updateTrans(observedStates[n,:],t)
            if t % nodes[n].policyAdjustRate == 0:
                nodes[n].updatePolicy(t)
            tocMdpLearn = time.time()
                                
        if isinstance(nodes[n],dqnNode) or isinstance(nodes[n],acNode) :
                                       # or isinstance(nodes[n],ddpgNode):
            ticDqnLearn = time.time()
            reward = nodes[n].getReward(collisions[n] ,t, isWait)
            observation_ = observedStates[n,:]  # update already # full already
            # additive noise to observation_
            if random.random() < noiseErrorProb:
                for k in range(noiseFlipNum):
                    ind =  random.randint(0, numChans-1)
                    observation_[ind] = 1- observation_[ind]
            observedStates[n,:] = observation_                        
            # Todo - rolling partially observation            
            # mdp seems for robust under same noise
            # Conclusion - robust to certain level of additive noise, e.g under [0,1,2,5]
            
            temp = observedStates[n,:]
            if PartialObservation == 'True':
                rollInd = int( math.fmod(t, numChans))
                for i in range(poBlockNum):
                    temp[(rollInd+i)%numChans] = 0
            observedStates[n,:] = temp
            observation_ = observedStates[n,:]
            # better than MDP, more rubost to partial observation
            
            done = True  
            if isinstance(nodes[n],dqnNode):
                nodes[n].storeTransition(observation, actionScalar, 
                     reward, observation_)
                if t % nodes[n].policyAdjustRate == 0:    
                    nodes[n].learn()
                    
            elif isinstance(nodes[n],acNode):
                 nodes[n].learn(observation, actionScalar, 
                     reward, observation_)
                 
            elif isinstance(nodes[n],ddpgNode):
                 nodes[n].storeTransition(observation, actionScalar, 
                 reward, observation_)
                 if nodes[n].ddpg_.pointer > nodes[n].ddpg_.MEMORY_CAPACITY:
                     nodes[n].var *= .9995    # decay the action randomness
                     nodes[n].ddpg_.learn()
                 
            else:
                pass
                    
 #               learnProbHist.append( nodes[n].dqn_.exploreProb)
            tocDqnLearn = time.time()
            # original  action -> step() -> observation_, reward, done
            # 1. action -> collisions
            # 2. collisions -> getReward() -> observation_, reward, done
    collisionHist[t,:]        = collisions
    cumulativeCollisions[t,:] = collisions
    if t != 0:
        cumulativeCollisions[t,:] +=  cumulativeCollisions[t-1,:]
    
    if ticMdpAction:
        mdpLearnTime[t] = tocMdpAction - ticMdpAction + tocMdpLearn - ticMdpLearn
    if ticDqnAction:
        dqnLearnTime[t] = tocDqnAction - ticDqnAction + tocDqnLearn - ticDqnLearn
        
    # show compeleted
    if t == numSteps * 0.1:
        print( "  10% completed")
        toc =  time.time()
        print( "--- cost %t seconds ---" %(toc - tic))        
    elif t == numSteps * 0.2:
        print( "  20% completed")
    elif t == numSteps * 0.3:
        print( "  30% completed")
    elif t == numSteps * 0.4:
        print( "  40% completed")
    elif t == numSteps * 0.5:
        print( "  50% completed")
    elif t == numSteps * 0.6:
        print ("  60% completed")
    elif t == numSteps * 0.7:
        print( "  70% completed")
    elif t == numSteps * 0.8:
        print( "  80% completed")
    elif t == numSteps * 0.9:
        print( "  90% completed")
    
print( " 100% completed"  )        
print( "--- End Main Loop--- ")
toc =  time.time()
print( "--- Totally %s seconds ---" %(toc - tic))

