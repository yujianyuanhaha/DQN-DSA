![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 
 
<!--
-------------------------------------------------------------------------
-             |  -             |  -             |
:-------------------------:|:-------------------------:|:-------------------------:
![](./profile.png) Jianyuan (Jet) Yu jiayuan@vt.edu  |  ![](./profile.png) Yue Xu xuyue24@vt.edu| ![](./profile.png) R.Michael Buehrer buehrer@vt.edu


-------------------------------------------------------------------------
-             |  -             | 
:-------------------------:|:-------------------------:|
<img align="" width="" height="150" src="Matlab_Logo.png"> .m MDPtool [[Download]()]  |  <img align="" width="" height="150" src="TensorflowLogo.png">  RL open-source [[link]()]| 
![](./milcom.jpg)DQN [[paper]()] [[Slides]()]  |  ![](./milcom.jpg)DRQN [[paper]()] [[Slides]()]    |

-->

-------------------------------------------------------------------------
Table of Contents
=================
   * [Overview](#overview)
   * [News](#news)
   * [ToDoList](#todolist)
      * [Capacity_Robust](#capacity_robust)
      * [PolicyGradient](#policygradient)
      * [POMDP](#pomdp)
      * [Stochastic](#stochastic)
      * [ScaleUp](#scaleup)
      * [Doxy](#doxy)
   * [Notice](#notice)
   * [Bugs](#bugs)
   * [Related Files:](#related-files)
   * [Reference:](#reference)
   * [Tutorial of Deep Reinforcement Learning](#tutorial-of-deep-reinforcement-learning)
   * [Ongoing Work - POMDP](#ongoing-work---pomdp)
   * [Configuration](#configuration)
   * [File Topology](#file-topology)
   * [How to run](#how-to-run)

# Overview
This project work around applying **deep Q network**[1] in **dynamic channel access**.
It validate the performance of intelligent node acess channel without information exchange 
with other nodes(legacy, hopping, intermittent, dsa etc). It mainly concerns about convergency speed
 and scale issues.  
To be exact, we look into following aspects:  
1. coexsitence with other type of nodes
    * legacy
    * legacy with tx prob  
    * hopping  
    * intermittent(duty cycle)  
    * dsa (able to wait)  
    * poission (the arrival interval & service interval follow poisson distribution, i.e. M/M/1 queue model)
    * mdp
    * dqn  
2. learn to wait
3. learn to occupy more than one channels
4. learn to avoid hidden nodes
5. learn to utilize spatial reuse (exposed nodes)
6. select good channels (when several channel available, some low quality channel bring low reward).  

The inspiration comes from SC2 competition, and some papers[2][3] have start some work around it.  
  
The project transfer Chris's code of MDP-DCA Matlab simulator as the starter with MDP python solver[4], and then adapot DQN python solver[5].  
Another repository[6] maintain by Yue would merge soon, and [7] is the technical report.  


# News
* (Fri Aug 3) Multiple learning nodes coexsit fixed, starting running scale-up case.
* (Tue Jul 17) 2-state markov Chain node added
* (Fri Jun 29) stack-DQN
    * add partial observation node with shorten observation as state
    * add partial observation node with shorten observation plus padding with zero/one as full state
    * add partial observation node with stacked partial observation together as state
* (Sun Jun 24) some new features 
    * add in possion node, model under M/M/1 theory, with arrival rate & service rate configurable 
    * add in policy gradient learning node, namely deep policy gradient (dpg) node 
    * rename, adapt string name, dumb node under 9, learning node start with 10 or more 




--------------------------------------------------------------------------
# ToDoList
## Capacity_Robust
* learn possion node  
* learn legacy node with fixed baised tx prob 
* learn long im node under limited memory and steps 
* dynamic environment 
* learn to greedy occupied all available channel 
* ~~efficient multiple dsa node coexist~~ 
* ~~multiple dqn node coexist~~ 
* merge yue's guess item & eligiable trace dqn node
## PolicyGradient
* dpg
## POMDP 
* vi
* pomcp
## Stochastic
* possion
* uniform
* 2-state markovChain
## ScaleUp
## Doxy




--------------------------------------------------------------------------
# Notice
1. When assign new number of channels and DQN node exist, need to restart the IPython console, exist pop size umatch error. While would not happen in raw terminal.
2. mdpNode would meet compuation constraint when number of channel over 10, result in dead loop (stuck at stateSpaceCreate).  
3. the assigment of patrial observation is currently in *dqnNode.py* file, tho silly way.


--------------------------------------------------------------------------
# Bugs
1. ~~We assume all nodes detect and make decision at same time, hence the multiple dsaNode may collide  (T.B.D.)~~. -> create politeness to dsa nodes to avoid ping-pong effect, a ugly way.
2. ~~Unstable performance when multiple dqnNode works (T.B.D.)~~. -> assign priority to learning nodes to make them observe-action one by one, a ugly way.

<img align="right" width="150" height="150" src="vt_logo.png">



