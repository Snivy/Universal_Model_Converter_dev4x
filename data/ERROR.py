#1
#v 0.001

def _ERROR(Message,Function):
    import sys,traceback
    i=sys.exc_info();T=traceback.extract_tb(i[2])[0]

    print '-----'
    print 'Recall: '+Function
    print
    print 'File: '+T[0].split('\\')[-1]+', line '+str(T[1])
    print "Code: '"+T[3]+"'"
    print traceback.format_exception_only(i[0], i[1])[0]
    print Message
    print '-----'

#other errors should be thrown before this is reached
global maxInstanceCount; maxInstanceCount = 1000000

def IncreaseRange(): #increase safety
    global maxInstanceCount; maxInstanceCount = 100000000

def DecreaseRange(): #increase speed
    global maxInstanceCount; maxInstanceCount = 10000

IWLDInstanceCount=0
def IWLD(Bool): #detect infinite while loop
    global IWLDInstanceCount,maxInstanceCount
    if not Bool: IWLDInstanceCount=0; maxInstanceCount=1000000; return False
    elif IWLDInstanceCount > maxInstanceCount:
        IWLDInstanceCount=0; maxInstanceCount=1000000; return False #stop while loop
    else: IWLDInstanceCount+=1; return True
    
def ResetIWLD(): pass #will be removed

IFLDInstanceCount=0 #detect infinite function loop
def IFLD(): global IFLDInstanceCount
def ResetIFLD(): global IFLDInstanceCount; IFLDInstanceCount=0
