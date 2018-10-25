![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 


# Related Files:
1. The [Result Demo of DQN-DCA](https://drive.google.com/open?id=1Tl5y8Ov_P_Fwqt1SpoRLuaAqaTlG20mImVx5o15VUsY) of Google Slides, 
and figure come from VT Google Folder [qdnFig](https://drive.google.com/open?id=1hQxplvCs_hSfgr9rrJ-rywutUkHWwnxP) of .png .pdf 
figure autosave by python, notice we SEPERATE figure from github to avoid too frequent update git folder.
2. The [technic report](https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB) and 
the [latex folder](https://drive.google.com/open?id=1GeqjxzAroWrWHcM8LnwumbAo0h-ZYItX).
3. A backup of Chris(Dr. Headley) MDP codes of [MDP solver](https://drive.google.com/open?id=1rddetimeRR8MECEsv0KRfdV1uLvd-4ZQ).




# Reference:  
[1] Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning." Nature 518.7540 (2015): 529-533.  
[2] Wang, Shangxing, et al. "Deep Reinforcement Learning for Dynamic Multichannel Access in Wireless Networks." IEEE Transactions on Cognitive Communications and Networking (2018)  
[3] Yu, Yiding, Taotao Wang, and Soung Chang Liew. "Deep-Reinforcement Learning Multiple Access for Heterogeneous Wireless Networks." arXiv preprint arXiv:1712.00162 (2017).  
[4] https://github.com/sawcordwell/pymdptoolbox  
[5] https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5_Deep_Q_Network   
[7] https://drive.google.com/open?id=1X-I2D4Dk_Z1IXAt19XUnlWHUvkxn42EB  


# Tutorial of Deep Reinforcement Learning
[1]. http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html  by Dr. Silver, lecturers video are in open access in  youtube as well.  
[2]. https://icml.cc/2016/tutorials/deep_rl_tutorial.pdf  a brief tutorial by Dr. Silver 


# Ongoing Work - POMDP
We are attempt to implement four method as solver
* stack-DQN
* Vaule Itervation
* POMCP
* Deep Recurrent Q network (DRQN)  

[1] [summary of current POMDP solver](https://bayesgroup.github.io/bmml_sem/2018/Shvechikov_Partially%20Observable%20Markov%20Decision%20Process%20in%20Reinforcement%20Learning.pdf)  
[2] [the vi+pomcp solver source code.](https://github.com/pemami4911/POMDPy)  
[3] POMCP - Silver, David, and Joel Veness. "Monte-Carlo planning in large POMDPs." Advances in neural information processing systems. 2010.  
[4] UCT, kenerl of POMCP - L. Kocsis and C. Szepesvari. Bandit based Monte-Carlo planning.  In 15th European Conference on Machine Learning, pages 282–293, 2006.  
[5] [slides of CMU](https://www.cs.cmu.edu/~ggordon/780-fall07/lectures/POMDP_lecture.pdf)  
[6] [slides of techfak](https://www.techfak.uni-bielefeld.de/~skopp/Lehre/STdKI.../POMDP_tutorial.pdf)   
[7] [pomdp alg website](http://www.pomdp.org/)  
[8] [DRQN blog](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-6-partial-observability-and-deep-recurrent-q-68463e9aeefc)  
[9] DRQN paper - Hausknecht, Matthew, and Peter Stone. "Deep recurrent q-learning for partially observable mdps." CoRR, abs/1507.06527 (2015).  
