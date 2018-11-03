![Build](https://travis-ci.org/pemami4911/POMDPy.svg?branch=master) ![Python27](https://img.shields.io/badge/python-2.7-blue.svg) ![Tensorflow16](https://img.shields.io/badge/tensorflow-1.6-blue.svg)

README FILE  
Author: Jianyuan (Jet) Yu  
Affiliation: Wireless, ECE, Virginia Tech  
Email : *jianyuan@vt.edu*  
Date  : April, 2018 


# Configuration  
We run codes on **Spyder** GUI under Anaconda(**version 2**), **tensorflow** is required as well as related tensorboard setup.  
For batch test, we run codes on ARC VT. 
* Python version 2.7, tensorflow version **1.6.0**. Notice tensorflow 1.5.0 is suggested on Linux OS else "keneral died, restart" error may appear. If the version would not fit, run command 
```
conda install -c conda-forge tensorflow=1.6.0
```  
Version would never be the big issue, since Anaconda support *virtual environment* easily without bothering current version setup.
e.g. setup Python 3.6    
1. python 3.5   
```
    conda create --name py3 python=3.5
```  
2. after py3 prompt show up, install any lib missing like numpy, tensorflow, matlibplot.  
``` 
    conda install numpy
    conda install tensorflow
    conda install matlibplot
```
Notice ipython does not support virtual environment as raw terminal; you can type ```anaconda-navigator``` after virtual environment is setup to launch the GUI, to apply feature like debugging in a virtual environment.


# How to run
Parameter all configurable at header part of ```multiNodeLearning.py``` OR ```setup.config``` file. 
In terminal run below command for the import the default ```setup.config``` file. :  
```
python multiNodeLearning.py
```
 
OR
```
python multiNodeLearning.py --set setFileName.cfg
```
where ```setupFileName``` was file like ```settingCaseXX``` to save some significant progressive results.  
OR even further, if some modification is made on ```multiNodeLearning.py``` hence it is renamed as like ```multiNodeLearningCaseXX.py```, you and execute
```
python multiNodeLearningCaseXX.py --set setFileName.cfg