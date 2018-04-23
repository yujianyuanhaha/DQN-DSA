
#"test call a class instance in the attribute of another class init"
#
#class cls1(object):
#    def __init__(self):
#        self.cls2Instance = cls2(self,cls1)
#        #self.cls2Instance = cls2(self,cls1)
#        
#        # need 'self', else  __init__() takes exactly 2 arguments (1 given)
#        # no cls1, else __init__() takes exactly 2 arguments (3 given)
#        
#
#   # TypeError: __init__() takes exactly 2 arguments (3 given)
#
##    def iNeedToCallThisMethod(self, funzies):
##        print funzies
#
#class cls2(object):
#    def __init__(self, cls1):
#    # if delete cls2, error "TypeError: __init__() takes exactly 1 argument (2 given)" of line 6
#       # mastermind.iNeedToCallThisMethod('funzies')
#       print "class 2"
#
#if __name__ == "__main__":
#    t = cls2(cls1)  # the name as input #also allow
#    mple = cls1()
#    
    
    
 # unit test   
# 
#import matplotlib.pyplot as plt
#"test save fig" 
#plt.plot([1,2,3,4])
#plt.savefig('../dqnFig/test.png')


#import os
#"test if Directory exist"
#if not os.path.exists('../testDir'):
#    os.makedirs('../testDir')
#"nest tic toc"
#from myFunction  import tic
#from myFunction  import toc
#tic()
#for i in range(100000):
#    pass
#tic()
#for i in range(100000):
#    pass
#toc()
#toc() 
 
 
"get value of time"
import time
start_time = time.time()
for i in range(100000):
    pass
print("--- %s seconds ---" % (time.time() - start_time))
 