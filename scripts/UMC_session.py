from data.COMMON import * #essentials
from data import VIEWER
Header( 0.001,('UMC session data',['ses']),('',['']),[''])

def ImportModel(T,C): ses=eval(string(0)); VIEWER.Libs = ses[1] if ses[0]==1 else []
def ExportModel(T,C): String(str([1,VIEWER.Libs]))
