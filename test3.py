
"test call a class instance in the attribute of another class init"

class cls1(object):
    def __init__(self):
        self.cls2Instance = cls2(self)

#    def iNeedToCallThisMethod(self, funzies):
#        print funzies

class cls2(object):
    def __init__(self, cls1):
    # if delete cls2, error "TypeError: __init__() takes exactly 1 argument (2 given)" of line 6
       # mastermind.iNeedToCallThisMethod('funzies')
       print "class 2"

if __name__ == "__main__":
    t = cls2()  # the name as input
    mple = cls1()