#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 13:37:38 2018

@author: Jet
"""


import numpy as np
from myFunction import ismember
from mdp import PolicyIteration







#A = np.array([ [1,3,5,6],[2,4,6,8] ])
#B = np.array([ [2,4,6,8], [1,3,5,7], [2,4,6,8] ]  )    # result [0,0]
#B1 = np.array([ [2,2,2,2], [1,3,5,6], [2,4,6,8] ]  )   # result [1,2]
#t = ismember(A,B)
#print t
#t1 = ismember(A,B1)
#print t1
#
## test pass



#A = np.array([1,3,5,6])
#B = np.array([ [2,4,6,8], [1,3,5,7], [2,4,6,8] ]  )    # result [0,0]
#B1 = np.array([ [2,2,2,2], [1,3,5,6], [2,4,6,8] ]  )   # result [1,2]
#t = ismember(A,B)
#print t
#t1 = ismember(A,B1)
#print t1

# test pass

#def tic():
#    #Homemade version of matlab tic and toc functions
#    import time
#    global startTime_for_tictoc
#    startTime_for_tictoc = time.time()
#
#def toc():
#    import time
#    if 'startTime_for_tictoc' in globals():
#        print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
#    else:
#        print "Toc: start time not set"
#        
#        
#if __name__ == '__main__':        
#    tic()
#    # do stuff
#    s = 0
#    for i in range(10000):
#        s += i
#    toc()
#    s = 0
#    for i in range(20000):
#        s += i
#    toc()         


#class Employee:
#    'hello world'
#    empCount = 0
#    
#    def __init__(self, name, salary):
#       self.name = name
#       self.salary = salary
#       Employee.empCount += 1
#    
#    def displayCount(self):
#      print "Total Employee %d" % Employee.empCount
#    
#    def displayEmployee(self):
#       print "Name : ", self.name,  ", Salary: ", self.salary
#
#"创建 Employee 类的第一个对象"
#emp1 = Employee("Zara", 2000)
#"创建 Employee 类的第二个对象"
#emp2 = Employee("Manni", 5000)
#emp1.displayEmployee()
#emp2.displayEmployee()
#print "Total Employee %d" % Employee.empCount




#
#class Parent:        # 定义父类
#   parentAttr = 100
#   def __init__(self):
#      print "调用父类构造函数"
# 
#   def parentMethod(self):
#      print '调用父类方法'
# 
#   def setAttr(self, attr):
#      Parent.parentAttr = attr
# 
#   def getAttr(self):
#      print "父类属性 :", Parent.parentAttr
# 
#class Child(Parent): # 定义子类
#   def __init__(self):
#      print "调用子类构造方法"
# 
#   def childMethod(self):
#      print '调用子类方法'
# 
#c = Child()          # 实例化子类
#c.childMethod()      # 调用子类的方法
#c.parentMethod()     # 调用父类方法
#c.setAttr(200)       # 再次调用父类的方法 - 设置属性值
#c.getAttr()          # 再次调用父类的方法 - 获取属性值

#
#import mdptoolbox.example
#P, R = mdptoolbox.example.forest()
#vi = mdptoolbox.mdp.ValueIteration(P, R, 0.9)
#vi.run()
#vi.policy # result is (0, 0, 0)




import matplotlib.pyplot as plt
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1, 2, 3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4, 5, 6])


plt.figure(2)                # a second figure
plt.plot([4, 5, 6])          # creates a subplot(111) by default

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1, 2, 3') # subplot 211 title

