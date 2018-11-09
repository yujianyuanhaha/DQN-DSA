![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 



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
![](/README_fig/dsa.png)  
<!-- <img align="left" width="" height="150" src="/README_fig/dsa.png">  -->
Notice DSA do perfect when make action based on current state, while would __fail by making action based on previous state__. It is reactive, not predict or learn.


# Model
![](/README_fig/model.png)
<!-- <img align="left" width="" height="200" src="/README_fig/model.png">  -->