#1
#v 0.001

_LOG = []
# ''.join( []+[] ) is much faster than ''+''
# (believe me, I've tried it already)

def LOG(Message): global _LOG; _LOG+=['\n',Message]
    
def LABEL(Name): global _LOG; _LOG+=[Name]
    
def WRITE_LOG(mode): #write/append the log data once per import/export
    global _LOG
    
    if not mode:
        L=open('session-info.log','w')
        L.write('Universal Model Converter - Session Log')
        
    else:
        L=open('session-info.log','a')
    
    L.write('\n\n'+(''.join(_LOG).encode('utf8')))
    L.close()

    _LOG = [] #clear data for next session
