![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 


# File Topology
    multiNodeLearning.py -- setup.config
                         -- myFunction.py
                         -- legacyNode.py
                         -- hoppingNode.py
                         -- imNode.py
                         -- dsaNode.py
                         -- poissonNode.py
                         -- markovChainNode.py
                         -- mdpNode.py      -- mdp.py
                         -- dqnNode.py      -- dqn.py
                                            -- dqnDouble.py
                                            -- dqnPriReplay.py
                                            -- dqnDuel.py 
                                            -- dqnR.py
                                            -- dpq.py                                                                     
                         -- stateSpaceCreate.py
                         -- scenario.py 


--------------------------------------------------------------------------

# Node Type Overview
Table below provides a quick view.  

| string name    | numeric    | file(.py)   | description   | parameters    |
|----------|----------|----------|----------|----------|
| legacy  | 0 | legacyNode  | always occupy one channel         |  txProb|
| hopping | 1 | hoppingNode | hopping bettween several channels | hopRate hopWidth HoppingChanIndex |
| im      | 2 | imNode      | interminient                      | imPeriod dutyCycle |
| dsa     | 3 | dsaNode     | dynamic channel access alway occupy first avaiable channel   |  |
| poisson | 4 | poissonNode | arrival and service interval follow poisson distribution  | arrivalInterval serviceInterval |
| markovChain | 5 | markovChainNode | 2-state markov chain node  | alpha beta |
| | | | | |
| mdp         | 10 | mdpNode mdp          | MDP(policy iteration OR policy interation) full obervation  |  |
| dqn          | 11 | dqnNode dqn          | Deep Q network  |  |
| dqnDouble    | 12 | dqnNode dqnDouble    | double  DQN  |  |
| dqnPriReplay | 13 | dqnNode dqnPriReplay | Priority with Exprience Replay  DQN  |  |
| dqnDuel      | 14 | dqnNode dqnDuel      | Duel  DQN  |  |
| dqnRef       | 15 | dqnNode dqnRef       | Refined  DQN  |  |
| dpg          | 16 | dqnNode dpg          | deep policy gradient  |  |
| ac           | 17 | dqnNode ac          | action-critic  |  |
| ddpg(TODO)           | 18 | dqnNode ddpg          | Distributed Proximal Policy Optimization  |  |
| a3cDiscrete(TODO)    | 19 | dqnNode           | A3C discrete action  |  |
| a3cDistribute (TODO) | 20 | dqnNode          |   |  |
| a3cRNN (TODO)        | 21 | dqnNode           |   |  |
| dqnDynamic (TODO)    | 22 | dqnNode           |Dynamic DQN  |  |
| dppo (TODO)          | 23 | dqnNode           | Proximal Policy Optimal  |  |
| et (Yue, TODO)       | 24 | dqnNode           | eligiable trace  |  |
| guess (Yue, TODO)    | 25 | dqnNode           | memory with guess sample  |  |
| | | | | |
| dqnPad             | 30 | dqnNode dqn          | partial observation with unkown padding with 1/0  |  |
| dqnPo              | 31 | dqnNode dqn          | partial observation  |  |
| dqnStack           | 32 | dqnNode dqn          | stacked   partial observation|  |
| dpgStack           | 33 | dqnNode dpg          | stacked   partial observation|  |
| dqnVI (TODO)       | 34 | dqnNode vi          | Vaule Iteration  |  |
| dqnPomcp (TODO)    | 35 | dqnNode pomcp          | Partial Observation Monte-Carlo Planning   |  |
| drqn (Yue, TODO)   | 36 | dqnNode drqn          | deep recurrent policy gradient  |  |




# X-O table
This table shows the learning ability of learning nodes with other type of nodes. Where **X** for CANNOT, **O** for CAN and **N/A** for unknown.  

| string name    | legacy    | hop      | intermittent   | dsa    | mdp        | dqn       | policy        |
|----------------|-----------|----------|----------------|--------|------------|-----------|---------------|
| mdp            | O         | O        | X              |      O |      O     |      O    |      O        |
| dqn             |O         | O        | O              |      O |      O     |      O    |      O        |
| policy          |O         | O        | X              |      O |      O     |      O    |      O        |


# Detail
Quite some functionality does not provide interface, but simple noted in codes.
## random or order mini-batch sample of DQN
set ```method = random``` or ```method =order``` inside ```dqn.py``` file.


## extra-memory DQN
use ```stackDQN``` without blocking work as extra-memory.  
edit where near ```updateStack```, 
``` python
                temp2 = partialObserveAction( temp, t, poStepNum, poSeeNum,actions[n,:])
                
                observationS_               = updateStack(observationS, temp2)
```
as 
```
#                temp2 = partialObserveAction( temp, t, poStepNum, poSeeNum,actions[n,:])
                temp2 = temp
                observationS_               = updateStack(observationS, temp2)
```
Also, edit ```self.stackNum = 4``` inside ```dqn.py``` file as well as ```stackNum = 4``` in ```setup.cfg``` file(TODO buggy).