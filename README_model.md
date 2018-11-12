![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 

# Simulator Framework
``` C
Construct different Type of Nodes
for t in 1 to numberStep
    for each node
        observation <- get previous observation
        action      <- epsilon-greedy get action based on observation
    update global states
    for each node
        reward      <- get reward based on observation,action
        observation' <- get updated observation
        if nodeType is DQN
            store  [observation, action, reward, observation']
        elseif nodeType is MDP
            update Transition Matrix by observation'
        update policy
```


## Online MDP
``` C
Init transition matrix P, reward matrix R
for t in 1 to numberStep
    for each node
        observation <- get previous observation
        action      <- epsilon-greedy get action based on observation
    update global states
    for each node
        reward      <- get reward based on observation,action
        observation' <- get updated observation

        if nodeType is MDP
            update P,R by observation'
        update policy


```


## epsilon-greedy to get action
![](/README_fig/epsilonGreedy.png)
| type    | scheme    | _`exploreDecayType`_
|----------|----------|----------
| __MDP__  | NOT require `Frozen Time` | _`exp`_, _`step`_, _`perf`_ in _`updatePolicy()`_ of `mdpNode.py`
| __DQN__ |  -  | _`incre`_, _`exp`_ in _`choose_action()`_  of `dqn.py`
| __DRQN__ |  require longer explore time   |_`exp`_ in  _`choose_action()`_  of `drqn.py`     


Besides, the _`timeLearnStart`_ (default value _`1000`_) could be set at `multiNodeLearning.py`, the _`exploreDecay`_(decay rate, default value _`0.01`_),  _`exploreMin`_(default value _`0.01`_) could be set at `mdpNode.py`, `dqn.py`.



## multi-agent



# Different Type of Nodes

## dumb
### constant
![](/README_fig/constant.png)
<!-- <img align="left" width="" height="100" src="/README_fig/constant.png">  -->


### hopping
![](/README_fig/hop.png)
<!-- <img align="left" width="" height="150" src="/README_fig/hop.png">  -->

### intermittent
![](/README_fig/im.png)
<!-- <img align="left" width="" height="100" src="/README_fig/im.png">  -->

## stochastic

### G-E Model/ 2-state Markov Chain
![](/README_fig/ge.png)
<!-- <img align="left" width="" height="150" src="/README_fig/ge.png">  -->

### Possion/ M/M/1 Queue Model
![](/README_fig/mm1.png)
<!-- <img align="left" width="" height="150" src="/README_fig/mm1.png">  -->

## heuristic
### DSA 
| type    | scheme    | comment   |
|----------|----------|----------
| __preSense__  | make action based on __current__ observation | classic, __reactive__ ,perfect, require full observation, low throughput  | 
| __postSense__ |  make action based on __previous__ observation  | would fail when meet hopping or intermittent |     
![](/README_fig/dsa.png)    
<!-- <img align="left" width="" height="150" src="/README_fig/dsa.png">  -->


Notice DSA do perfect when make action based on current state, while would __fail by making action based on previous state__. It is reactive, not predict or learn.


# Model
![](/README_fig/model.png)
<!-- <img align="left" width="" height="200" src="/README_fig/model.png">  -->


# Single Agent to Multiple Agent DQN
![](/README_fig/sync.png)
![](/README_fig/async1.png)
![](/README_fig/async2.png)


# Noise
![](/README_fig/noise.png)
call function _`noise()`_ would "mess" the observation, with _`noiseErrorProb`_,  _`noiseFlipNum`_.
``` python
messedObservation = noise(observation , noiseErrorProb, noiseFlipNum) 
```  
And `Average corrputed bit = noiseErrorProb * noiseFlipNum `


# Hidden & Expore Node
TODO

# Partial Observation

## partial
```
observation <- state[m:n]
```
![](/README_fig/partial.png)


## padding
```
state[m:n] <- Nan
observation <- state
```
![](/README_fig/pad.png)

## padding with self-action
```
state[m:n] <- Nan
observation <- [state, action]
```
default observation function by __DRQN__---.
![](/README_fig/pad-act.png)


## stacked observation
```
observation2 <- state[m:n]
stack <- [observation1,observation2]
```
![](/README_fig/stack.png)