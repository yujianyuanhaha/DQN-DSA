![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 
 

-------------------------------------------------------------------------
# News
* (Sun Jun 24) some new features 
    * add in possion node, model under M/M/1 theory, with arrival rate & service rate configurable 
    * add in policy gradient learning node, namely deep policy gradient (dpg) node 
    * rename, adapt string name, dumb node under 9, learning node start with 10 or more 




--------------------------------------------------------------------------
# To Do List
* Capacity & Robust
    * learn possion node  
    * learn legacy node with fixed baised tx prob 
    * learn long im node under limited memory and steps 
    * dynamic environment 
    * learn to greedy occupied all available channel 
    * efficient multiple dsa node coexist 
    * multiple dqn node coexist 
    * merge yue's guess item & eligiable trace dqn node  
* POMDP 



--------------------------------------------------------------------------
# Notice
1. When assign new number of channels and DQN node exist, need to restart the IPython console, exist pop size umatch error. While would not happen in raw terminal.
2. mdpNode would meet compuation constraint when number of channel over 10, result in dead loop (stuck at stateSpaceCreate).


--------------------------------------------------------------------------
# Bugs
1. We assume all nodes detect and make decision at same time, hence the multiple dsaNode may collide  (T.B.D.).
2. Unstable performance when multiple dqnNode works (T.B.D.).




--------------------------------------------------------------------------
# Related Files:
1. The [Result Demo of DQN-DCA](https://drive.google.com/open?id=1Tl5y8Ov_P_Fwqt1SpoRLuaAqaTlG20mImVx5o15VUsY) of Google Slides, 
and figure come from VT Google Folder [qdnFig](https://drive.google.com/open?id=1hQxplvCs_hSfgr9rrJ-rywutUkHWwnxP) of .png .pdf 
figure autosave by python, notice we SEPERATE figure from github to avoid too frequent update git folder.
2. The [technic report](https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB) and 
the [latex folder](https://drive.google.com/open?id=1GeqjxzAroWrWHcM8LnwumbAo0h-ZYItX).
3. A backup of Chris(Dr. Headley) MDP codes of [MDP solver](https://drive.google.com/open?id=1rddetimeRR8MECEsv0KRfdV1uLvd-4ZQ).

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



# Reference:  
[1] Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning." Nature 518.7540 (2015): 529-533.  
[2] Wang, Shangxing, et al. "Deep Reinforcement Learning for Dynamic Multichannel Access in Wireless Networks." IEEE Transactions on Cognitive Communications and Networking (2018)  
[3] Yu, Yiding, Taotao Wang, and Soung Chang Liew. "Deep-Reinforcement Learning Multiple Access for Heterogeneous Wireless Networks." arXiv preprint arXiv:1712.00162 (2017).  
[4] https://github.com/sawcordwell/pymdptoolbox  
[5] https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5_Deep_Q_Network   
[7] https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB  


# Tutorial of Deep Reinforcement Learning
[1]. http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html  by Dr. Silver, lecturers video are in open access in  youtube as well
[2]. https://icml.cc/2016/tutorials/deep_rl_tutorial.pdf  a brief tutorial by Dr. Silver 


# Ongoing Work - POMDP
[1] [the solver source code.](https://github.com/pemami4911/POMDPy)
[2] Silver, David, and Joel Veness. "Monte-Carlo planning in large POMDPs." Advances in neural information processing systems. 2010.
[3] L. Kocsis and C. Szepesvari. Bandit based Monte-Carlo planning. In 15th European Conference on Machine Learning, pages 282–293, 2006.
[4] [slides of CMU](https://www.cs.cmu.edu/~ggordon/780-fall07/lectures/POMDP_lecture.pdf)  
[5] [slides of techfak](https://www.techfak.uni-bielefeld.de/~skopp/Lehre/STdKI.../POMDP_tutorial.pdf) 
[6] [website](http://www.pomdp.org/) 


--------------------------------------------------------------------------
# Configuration  
We run codes on **Spyder** GUI under Anaconda(**version 2**), **tensorflow** is required as well as related tensorboard setup.  
For batch test, we run codes on ARC VT. 
1. Python version 2.7, tensorflow version **1.6.0**. Notice tensorflow 1.5.0 is suggest on Linux OS else "keneral died, restart" error may appear.


--------------------------------------------------------------------------
# File Topology
    multiNodeLearning.py -- setup.config
                         -- myFunction.py
                         -- legacyNode.py
                         -- hoppingNode.py
                         -- imNode.py
                         -- dsaNode.py
                         -- poissonNode.py
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
# How to run the codes?  
Paramter all configurable at header part of ```multiNodeLearning.py``` OR ```setup.config``` file. Table below provide a quick view. 
| string name | numeric  | file(.py) | description | parameters  |
|----------|----------|----------|----------|----------|
| legacy  | 0 | legacyNode  | always occupy one channel         |  txProb|
| hopping | 1 | hoppingNode | hopping bettween several channels | hopRate hopWidth HoppingChanIndex |
| im      | 2 | imNode      | interminient                      | imPeriod dutyCycle |
| dsa     | 3 | dsaNode     | dynamic channel access alway occupy first avaiable channel   |  |
| poisson | 4 | poissonNode | arrival and service interval follow poisson distribution  | arrivalRate serviceRate |
| | | | | |
| mpd          | 10 | mdpNode mdp          | MDP full obervation  |  |
| dqn          | 11 | dqnNode dqn          | Deep Q network  |  |
| dqnDouble    | 12 | dqnNode dqnDouble    | double  DQN  |  |
| dqnPriReplay | 13 | dqnNode dqnPriReplay | Priority with Exprience Replay  DQN  |  |
| dqnDuel      | 14 | dqnNode dqnDuel      | Duel  DQN  |  |
| dqnRef       | 15 | dqnNode dqnRef       | Refined  DQN  |  |
| dpg          | 16 | dqnNode dpg          | deep policy gradient  |  |



In terminal run:  
```
python multiNodeLearning.py
```
:sunglasses:





