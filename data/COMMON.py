#1
#v 0.001

import sys,os; sys.path.append('libs')
#import numpy as __np, scipy as __sp #need a portable version
global _Scripts; _Scripts=[[[],[]],[[],[]],[[],[]]] #[Model,Anim,Image]

#for scripts:
from FORMAT import *
from ERROR import *
from WIDGETS import *

#from ERROR import _ERROR #why the above line doesn't work, I'll never know
from LOGGING import LABEL, LOG as __LOG
def _Warning(msg): print msg
def _Notice(msg,win): print msg

#from array import array
from math import sin, asin, cos, acos, tan, atan, atan2, pi

global __TOGGLE_LOGGING; __TOGGLE_LOGGING=True
__o__=None

#___________________________________________________________________________________________

global Mod; Mod=None #Updated by UMC before Header() is called

def __CleanScripts(): #delete the pyc files in the scripts directory
    global _Scripts
    modnames = []
    for SF in (_Scripts[0]+_Scripts[1]+_Scripts[2]):
        for script in SF:
            try: modnames.index(script[0])
            except: modnames += [script[0]]
    for modname in modnames:
        try: os.remove('scripts/%s.pyc'%modname)
        except: pass
    #print modnames

#model/anim scripts
global __functions; __functions=[0,0,0,0]
def Header(Version=0.001,Model=('',[]),Anim=('',[]),Libs=[],IMGs=[]):
    global _Scripts,Mod,__functions
    #append this script to it's job-slots (it's functions define which job-slots to use)
    if __functions[0]: _Scripts[0][0]+=[[Mod,[Version,Model,Libs],IMGs]] #ImportModel
    if __functions[1]: _Scripts[0][1]+=[[Mod,[Version,Model,Libs],IMGs]] #ExportModel
    if __functions[2]: _Scripts[1][0]+=[[Mod,[Version,Anim,Libs],IMGs]] #ImportAnim
    if __functions[3]: _Scripts[1][1]+=[[Mod,[Version,Anim,Libs],IMGs]] #ExportAnim
    #animations aren't yet handled (not until the GUI is done)
    
    #check for anything to be included with this script
    if sum(__functions): #doesn't append if __functions==[0,0,0,0]
        for Lib in Libs:
            if Lib!='':
                try: #make sure the required library is safe
                    __import__(Lib)
                    sys.modules[Mod].__dict__.update(sys.modules[Lib].__dict__)
                    #^update the current module with the required lib's dictionary
                    
                except: pass #the library is either nonexistant or contains an error
                #continue using the script just in case there are local functions defined in the script
                #if not, an exception will disrupt the import process, skipping the import.
        
        #image handlers will be tested and executed once import/export processing is called
        #this is to prevent an invalid module error caused from trying to load an image handler loaded after this script


#image handling scripts
global __imgfunctions; __imgfunctions=[0,0]
def imgHeader(Version=0.001,Image=('',[]),Libs=[]):
    global _Scripts,Mod,__imgfunctions
    if __imgfunctions[0]: _Scripts[2][0]+=[[Mod,[Version,Image,Libs]]] #DecodeImage
    if __imgfunctions[1]: _Scripts[2][1]+=[[Mod,[Version,Image,Libs]]] #EncodeImage
    
    if sum(__functions): #doesn't append if __functions==[0,0,0,0]
        for Lib in Libs: #include libraries with COMMON
            if Lib!='':
                try: #make sure the required library is safe
                    __import__(Lib)
                    sys.modules[Mod].__dict__.update(sys.modules[Lib].__dict__)
                    #^update the current module with the required lib's dictionary
                    
                except: pass #the library is either nonexistant or contains an error


#sys.modules['data.COMMON'].__dict__.update(sys.modules[Lib].__dict__)
#looks like a memory overflow issue right?
#look again:

#>>> d = {'O1':0}       #d == sys.modules['data.COMMON']
#>>> d.update({'O2':1}) #sys.modules['data.COMMON'].__dict__.update(sys.modules[Lib].__dict__)
#>>> d
#{'O2': 1, 'O1': 0}
#>>> d.update({'O2':1}) #update passed again
#>>> d
#{'O2': 1, 'O1': 0}
#>>> #nothing changed

#TODO: update COMMON with the libs using this function (no re-importing COMMON)
#re-importing the module with libs should work w/o problem in future implementations ;)
    
#___________________________________________________________________________________________

__f={} #file data(s) {'Name':[data]} (data stored as u8())
__d={} #file Directory ('Name':'Directory')
__o={} #file offset {'Name':offset}
#dictionaries are faster than lists
__n=[] #file Names (used for ordering) (__f[__n[index]])
__c='' #current file Name

FileError=0 #if there was a file error during the import/export process,
#any reads/writes following the invalid file index will be skipped

def __GetDir0(): global __d,__n; return __d[__n[0]]
#^called during the import operation to remember the directory for the export operation
def __ClearFiles(): global __f,__d,__o,__n,__c; __f,__d,__o,__n,__c={},{},{},[],''
def __WriteFiles():
    global __f,__d,__n

    for n in __n:
        if __d[n]=='': pass #Temp file
        else:
            try: os.makedirs(__d[n])
            except: pass
            F=open(__d[n]+n,'wb')
            l=len(__f[n])-1

            PrP,sec=0,(1.0/(l-1))*100
            for i,d in enumerate(__f[n]):
                F.write(chr(d)); P=int(sec*i)
                if P!=PrP: sys.stdout.write(' \rexporting %s %i%s'%(__c,P,'%')); PrP=P
            sys.stdout.write(' \rexporting %s %s\n'%(__c,'100%'))
            F.close()

    __ClearFiles()
    
__hx__={0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '0A', 11: '0B', 12: '0C', 13: '0D', 14: '0E', 15: '0F', 16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16', 23: '17', 24: '18', 25: '19', 26: '1A', 27: '1B', 28: '1C', 29: '1D', 30: '1E', 31: '1F', 32: '20', 33: '21', 34: '22', 35: '23', 36: '24', 37: '25', 38: '26', 39: '27', 40: '28', 41: '29', 42: '2A', 43: '2B', 44: '2C', 45: '2D', 46: '2E', 47: '2F', 48: '30', 49: '31', 50: '32', 51: '33', 52: '34', 53: '35', 54: '36', 55: '37', 56: '38', 57: '39', 58: '3A', 59: '3B', 60: '3C', 61: '3D', 62: '3E', 63: '3F', 64: '40', 65: '41', 66: '42', 67: '43', 68: '44', 69: '45', 70: '46', 71: '47', 72: '48', 73: '49', 74: '4A', 75: '4B', 76: '4C', 77: '4D', 78: '4E', 79: '4F', 80: '50', 81: '51', 82: '52', 83: '53', 84: '54', 85: '55', 86: '56', 87: '57', 88: '58', 89: '59', 90: '5A', 91: '5B', 92: '5C', 93: '5D', 94: '5E', 95: '5F', 96: '60', 97: '61', 98: '62', 99: '63', 100: '64', 101: '65', 102: '66', 103: '67', 104: '68', 105: '69', 106: '6A', 107: '6B', 108: '6C', 109: '6D', 110: '6E', 111: '6F', 112: '70', 113: '71', 114: '72', 115: '73', 116: '74', 117: '75', 118: '76', 119: '77', 120: '78', 121: '79', 122: '7A', 123: '7B', 124: '7C', 125: '7D', 126: '7E', 127: '7F', 128: '80', 129: '81', 130: '82', 131: '83', 132: '84', 133: '85', 134: '86', 135: '87', 136: '88', 137: '89', 138: '8A', 139: '8B', 140: '8C', 141: '8D', 142: '8E', 143: '8F', 144: '90', 145: '91', 146: '92', 147: '93', 148: '94', 149: '95', 150: '96', 151: '97', 152: '98', 153: '99', 154: '9A', 155: '9B', 156: '9C', 157: '9D', 158: '9E', 159: '9F', 160: 'A0', 161: 'A1', 162: 'A2', 163: 'A3', 164: 'A4', 165: 'A5', 166: 'A6', 167: 'A7', 168: 'A8', 169: 'A9', 170: 'AA', 171: 'AB', 172: 'AC', 173: 'AD', 174: 'AE', 175: 'AF', 176: 'B0', 177: 'B1', 178: 'B2', 179: 'B3', 180: 'B4', 181: 'B5', 182: 'B6', 183: 'B7', 184: 'B8', 185: 'B9', 186: 'BA', 187: 'BB', 188: 'BC', 189: 'BD', 190: 'BE', 191: 'BF', 192: 'C0', 193: 'C1', 194: 'C2', 195: 'C3', 196: 'C4', 197: 'C5', 198: 'C6', 199: 'C7', 200: 'C8', 201: 'C9', 202: 'CA', 203: 'CB', 204: 'CC', 205: 'CD', 206: 'CE', 207: 'CF', 208: 'D0', 209: 'D1', 210: 'D2', 211: 'D3', 212: 'D4', 213: 'D5', 214: 'D6', 215: 'D7', 216: 'D8', 217: 'D9', 218: 'DA', 219: 'DB', 220: 'DC', 221: 'DD', 222: 'DE', 223: 'DF', 224: 'E0', 225: 'E1', 226: 'E2', 227: 'E3', 228: 'E4', 229: 'E5', 230: 'E6', 231: 'E7', 232: 'E8', 233: 'E9', 234: 'EA', 235: 'EB', 236: 'EC', 237: 'ED', 238: 'EE', 239: 'EF', 240: 'F0', 241: 'F1', 242: 'F2', 243: 'F3', 244: 'F4', 245: 'F5', 246: 'F6', 247: 'F7', 248: 'F8', 249: 'F9', 250: 'FA', 251: 'FB', 252: 'FC', 253: 'FD', 254: 'FE', 255: 'FF',
        'BD': 189, 'BE': 190, 'BF': 191, 'BA': 186, 'BB': 187, 'BC': 188, 'FB': 251, '5E': 94, '5D': 93, '5F': 95, '5A': 90, '5C': 92, '5B': 91, '24': 36, '25': 37, '26': 38, '27': 39, '20': 32, '21': 33, '22': 34, '23': 35, '28': 40, '29': 41, 'F1': 241, 'A4': 164, '87': 135, 'F0': 240, '6A': 106, '6B': 107, '2D': 45, '2E': 46, '2F': 47, '6C': 108, '2A': 42, '2B': 43, '2C': 44, '6D': 109, '6E': 110, '60': 96, '59': 89, '58': 88, 'FA': 250, '55': 85, '54': 84, '57': 87, '56': 86, '51': 81, '50': 80, '53': 83, '52': 82, 'B4': 180, 'B5': 181, 'B6': 182, '63': 99, 'B0': 176, 'B1': 177, 'B2': 178, 'B3': 179, '64': 100, 'B8': 184, 'B9': 185, '65': 101, 'FF': 255, 'F4': 244, '67': 103, 'DD': 221, '88': 136, '89': 137, '3C': 60, '3B': 59, '3A': 58, '81': 129, '86': 134, '3F': 63, '3E': 62, '3D': 61, '02': 2, '03': 3, '00': 0, '01': 1, '06': 6, '07': 7, '04': 4, '05': 5, '08': 8, '09': 9, 'B7': 183, 'E9': 233, 'E8': 232, 'E5': 229, 'E4': 228, 'E7': 231, 'E6': 230, 'E1': 225, 'E0': 224, 'E3': 227, 'E2': 226, 'F6': 246, 'EE': 238, 'ED': 237, 'EF': 239, 'EA': 234, 'EC': 236, 'EB': 235, '0B': 11, '0C': 12, '0A': 10, '0F': 15, '0D': 13, '0E': 14, '39': 57, '38': 56, '33': 51, '32': 50, '31': 49, '30': 48, '37': 55, '36': 54, '35': 53, '34': 52, 'F2': 242, 'F8': 248, 'FC': 252, 'F5': 245, '1A': 26, '61': 97, '1C': 28, '1B': 27, '1E': 30, '1D': 29, '66': 102, '1F': 31, '68': 104, '69': 105, 'F9': 249, 'FD': 253, '9A': 154, '9C': 156, '9B': 155, '9E': 158, '9D': 157, '9F': 159, 'C9': 201, 'C8': 200, 'C3': 195, 'C2': 194, 'C1': 193, '78': 120, 'C7': 199, 'C6': 198, 'C5': 197, 'C4': 196, 'FE': 254, 'CC': 204, 'CB': 203, 'CA': 202, 'CF': 207, 'CE': 206, 'CD': 205, '99': 153, '98': 152, '6F': 111, 'C0': 192, '91': 145, '90': 144, '93': 147, '92': 146, '95': 149, '94': 148, '97': 151, '96': 150, '11': 17, '10': 16, '13': 19, '12': 18, '15': 21, '14': 20, '17': 23, '16': 22, '19': 25, '18': 24, '8B': 139, '8C': 140, '8A': 138, 'DF': 223, '8F': 143, '62': 98, 'DE': 222, 'DB': 219, 'DC': 220, 'F3': 243, 'DA': 218, '82': 130, '8D': 141, '83': 131, '8E': 142, '80': 128, '7F': 127, '7E': 126, '7D': 125, '7C': 124, '7B': 123, '48': 72, '49': 73, '46': 70, '47': 71, '44': 68, '45': 69, '42': 66, '43': 67, '40': 64, '41': 65, 'A1': 161, 'A0': 160, 'A3': 163, 'A2': 162, 'A5': 165, '84': 132, 'A7': 167, 'A6': 166, 'A9': 169, 'A8': 168, '85': 133, 'AA': 170, 'AC': 172, 'AB': 171, 'AE': 174, 'AD': 173, 'AF': 175, '77': 119, '76': 118, '75': 117, '74': 116, '73': 115, '72': 114, '71': 113, '70': 112, '4F': 79, '4D': 77, '4E': 78, '4B': 75, '4C': 76, '79': 121, '4A': 74, '7A': 122, 'F7': 247, 'D8': 216, 'D9': 217, 'D6': 214, 'D7': 215, 'D4': 212, 'D5': 213, 'D2': 210, 'D3': 211, 'D0': 208, 'D1': 209}
def ImportFile(Name,RaiseError=0):
    #creates a file data space and fills it with the file data
    global __f,__d,__o,__n,__c,FileError

    D=(__d[__n[0]] if len(__n) else '')
    #the first file is specified by the Tkinter open dialog,
    #and will always have a directory
    
    try:
        FileError=0
        #try to open the file
        F=open('%s%s'%(D,Name),'rb')
        #continue if successful
        
        l=len(F.read()); F.seek(0,0)
        
        __c=Name.split('/')[-1]
        
        __f[__c] = [255]*l
        __d[__c] = '%s%s'%(D,Name.replace(__c,''))
        __o[__c] = 0
        __n+=[__c] #keep the index for switching files by index
        
        PrP,sec=0,(1.0/(l-1))*100
        for i in range(l): #fill the data space
            __f[__c][i]=ord(F.read(1)); P=int(sec*i)
            if P!=PrP: sys.stdout.write(' \rimporting %s %i%s'%(__c,P,'%')); PrP=P
        sys.stdout.write(' \rimporting %s %s\n'%(__c,'100%'))
        F.close()
        
    except IOError:
        print "ERROR: '%s' file not found!"%Name
        __LOG("\nERROR: ImportFile('%s') file not found!"%Name)
        __LOG("Please check the directory to make sure the file exists.\n")
        if RaiseError: raise IOError #cancel the import/export operation
        else: FileError=1 #skip the file and continue the import/export operation

def ExportFile(Name):
    #creates a file data space to be filled
    global __f,__d,__o,__n,__c

    D=(__d[__n[0]] if len(__n) else '')
    #the first file is specified by the Tkinter saveas dialog,
    #and will always have a directory
    
    __c=Name.split('/')[-1]
    
    __f[__c] = []
    __d[__c] = '%s%s'%(D,Name.replace(__c,''))
    __o[__c] = 0
    __n+=[__c] #keep the index for switching files by index
    
    __LOG("\n-- created export file: '%s' --\n"%Name)

def TempFile(Name):
    #creates a file data space to be filled
    global __f,__d,__o,__n,__c

    D=(__d[__n[0]] if len(__n) else '')
    #the first file is specified by the Tkinter saveas dialog,
    #and will always have a directory
    
    __c=Name
    
    __f[__c] = []
    __d[__c] = ''
    __o[__c] = 0
    __n+=[__c] #keep the index for switching files by index
    
    __LOG("\n-- created temporary file: '%s' --\n"%Name)
    
def SwitchFile(Name=0,RaiseError=0):
    global __f,__n,__c,FileError
    if type(Name)==str:
        try:
            FileError=0
            __f[Name]
            __c=Name
            __LOG("\n-- switched to file: '%s' --\n"%Name)
        except:
            print "ERROR: SwitchFile('%s') file does not exist!"%Name
            __LOG("\nERROR: SwitchFile('%s') file does not exist!"%Name)
            __LOG("Please make sure you've imported the file first with NewFile('%s')"%Name)
            __LOG("Or check to make sure you've included the file's extension.\n")
            if RaiseError: raise IndexError #cancel the import/export operation
            else: FileError=1 #skip the file and continue the import/export operation
    elif type(Name)==int:
        try:
            FileError=0
            __c=__n[Name]
            __LOG("\n-- switched to file: '%s' --\n"%__n[Name])
        except:
            print "ERROR: SwitchFile('%i') invalid file index!"%Name
            __LOG("\nERROR: SwitchFile('%i') invalid file index!"%Name)
            __LOG("Please make sure you've imported the file first with NewFile(*Directory*)")
            __LOG("Or check to make sure the index is valid. (0 is the first file)\n")
            if RaiseError: raise IndexError #cancel the import/export operation
            else: FileError=1 #skip the file and continue the import/export operation
            

#for logging:
def __POS(): global __o,__c; HO=(hex(__o[__c]).replace('0x','')).upper(); return '0x%s%s'%(''.join(['0']*(10-len(HO))),HO)

def __UDF(DL,val=0): return __UDF(DL[1:],(val<<8)|DL[0]) if len(DL) else val
def __HDF(DL,val=''): global __hx__; return __HDF(DL[1:],'%s%s'%(val,__hx__[DL[0]])) if len(DL) else val

def __BIT(big,bit_format,byte_size,value,label=''):
    global __f,__o,__c,FileError
    if not FileError:
        p=__POS() #get file position
        if type(value)==str: #credit to Gribouillis for various speedups:
            if (__o[__c]+byte_size)<=len(__f[__c]): #check for EOF (better than recieving an indexing error)
                DATA= __f[__c][ __o[__c] : __o[__c]+byte_size ]
                val = __UDF(DATA if big else list(reversed(DATA))) #multi-int -> single-int (flipped if little endian)
                if bit_format == 1: val=(val-(1<<(byte_size<<3)) if val>(1<<(byte_size<<3))/2 else val) #signed int
                if bit_format == 2: #float (IEEE 754)
                    #credit to pyTony for simplifying the formula of 'e' and fixing the return values
                    e=((byte_size*8)-1)//(byte_size+1)+(byte_size>2)*byte_size//2; m,b=[((byte_size*8)-(1+e)), ~(~0 << e-1)]
                    S,E,M=[(val>>((byte_size*8)-1))&1,(val>>m)&~(~0 << e),val&~(~0 << m)] #<- added brackets (faster processing)
                    if E == int(''.join(['1']*e),2): val=(float('NaN') if M!=0 else (float('+inf') if S else float('-inf')))
                    else: val=((pow(-1,S)*(2**(E-b-m)*((1<<m)+M))) if E else pow(-1,S)*(2**(1-b-m)*M))
                    #I personally don't entirely understand this, but it works more than perfectly. XD
                if bit_format == 3: pass #float (IBM)
                if bit_format == 4: pass #float (Borland)
                __o[__c]+=byte_size #modify the file offset
                __LOG('%s: read 0x%s as %s%s'%(p,__HDF(DATA),str(val),label))
                return val
            
            else: #EOF (End Of File)
                __LOG("\nERROR: End of File reached")
                raise EOFError #this will cancel the import operation
            
        elif type(value)==int: #write int
            if bit_format==1: value=(value+pow(256,byte_size) if value<0 else value) #signed int
            Bytes=[(value>>((byte_size-i)*8))&255 if big else (value>>(8*i))&255 for i in range(byte_size)] # single-int -> multi-int (could be faster)
            __f[__c]+=Bytes; __o[__c]+=byte_size
            __LOG("%s: wrote '%i' as 0x%s%s" % (p,value,Bytes,label))
            
        elif type(value)==float: #write float
            e=((byte_size*8)-1)//(byte_size+1)+(byte_size>2)*byte_size//2; m,b=[((byte_size*8)-(1+e)), ~(~0 << e-1)] #pytony's formula
            
            #----------------------------------------
            #TODO: need float2hex conversion aglorithm (currently writes f32 and f64 only)
            from struct import pack
            if byte_size==4: __f[__c]+= pack(('>f' if big else '<f'), value)[0:4]; __o[__c]+=byte_size
            if byte_size==8: __f[__c]+= pack(('>d' if big else '<d'), value)[0:8]; __o[__c]+=byte_size #fixed
            #----------------------------------------
            
            __LOG("%s: wrote '%s' as 0x%s%s" % (p,value,'',label))
            
        elif type(value)==list: return list(__BIT(big,bit_format,byte_size,Lval) for Lval in value)
        elif type(value)==tuple: return tuple(__BIT(big,bit_format,byte_size,Tval) for Tval in value)
        elif type(value)==bool: return __BIT(big,bit_format,byte_size,int(value)) #Flag
    else: pass #skip the bad file
    
def __Hex(big,value,label=''):
    global __f,__a
    p=__POS()
    if type(value)==int: #read (bytes)
        DATA=__f[__c][__o[__c]:__o[__c]+value]
        __o[__c]+=value
        val = __HDF(DATA if big else list(reversed(DATA)))
        __LOG("%s: read 0x%s as '%s'%s" % (p,__HDF(DATA),val,label))
        return val
    
    elif type(value)==str: #write
        value=((value.replace('0x','')).replace(' ','')).upper() #'0x08f0'/'08 F0' -> '08F0'
        if str(len(value)/2.).split('.')[1]=='5': value='%s%s'%('0',value) #'30F' -> '030F'
            
        Bytes = [__hx__[value[l*2:(l+1)*2]] for l in range(len(value)/2)]
        if not big: Bytes=list(reversed(Bytes))
        __f[__c]+=Bytes; __o[__c]+=len(Bytes)
        __LOG("%s: wrote '%s' as 0x%s%s" % (p,value,Bytes,label))

    elif type(value)==list: return list(__Hex(big,Lval) for Lval in value)
    elif type(value)==tuple: return tuple(__Hex(big,Tval) for Tval in value)
    elif type(value)==bool: return __Hex(big,int(value))
    
#I/O user functions
def   u8(value='',label='',big=0): return __BIT(big,0,1,value,label)
def  u16(value='',label='',big=0): return __BIT(big,0,2,value,label)
def  u24(value='',label='',big=0): return __BIT(big,0,3,value,label)
def  u32(value='',label='',big=0): return __BIT(big,0,4,value,label)
def  u64(value='',label='',big=0): return __BIT(big,0,8,value,label)
def   s8(value='',label='',big=0): return __BIT(big,1,1,value,label)
def  s16(value='',label='',big=0): return __BIT(big,1,2,value,label)
def  s24(value='',label='',big=0): return __BIT(big,1,3,value,label)
def  s32(value='',label='',big=0): return __BIT(big,1,4,value,label)
def  s64(value='',label='',big=0): return __BIT(big,1,8,value,label)
def  f32(value='',label='',big=0): return __BIT(big,2,4,value,label)
def  f64(value='',label='',big=0): return __BIT(big,2,8,value,label)

def   h8(value='',label='',big=0): return __Hex(big,value if type(value)==str and value!='' else 1,label)
def  h16(value='',label='',big=0): return __Hex(big,value if type(value)==str and value!='' else 2,label)
def  h24(value='',label='',big=0): return __Hex(big,value if type(value)==str and value!='' else 3,label)
def  h32(value='',label='',big=0): return __Hex(big,value if type(value)==str and value!='' else 4,label)
def  h64(value='',label='',big=0): return __Hex(big,value if type(value)==str and value!='' else 8,label)

def  bu8(value='',label=''): return __BIT(1,0,1,value,label)
def bu16(value='',label=''): return __BIT(1,0,2,value,label)
def bu24(value='',label=''): return __BIT(1,0,3,value,label)
def bu32(value='',label=''): return __BIT(1,0,4,value,label)
def bu64(value='',label=''): return __BIT(1,0,8,value,label)
def  bs8(value='',label=''): return __BIT(1,1,1,value,label)
def bs16(value='',label=''): return __BIT(1,1,2,value,label)
def bs24(value='',label=''): return __BIT(1,1,3,value,label)
def bs32(value='',label=''): return __BIT(1,1,4,value,label)
def bs64(value='',label=''): return __BIT(1,1,8,value,label)
def bf32(value='',label=''): return __BIT(1,2,4,value,label)
def bf64(value='',label=''): return __BIT(1,2,8,value,label)

def  bh8(value='',label=''): return __Hex(1,value if type(value)==str and value!='' else 1,label)
def bh16(value='',label=''): return __Hex(1,value if type(value)==str and value!='' else 2,label)
def bh24(value='',label=''): return __Hex(1,value if type(value)==str and value!='' else 3,label)
def bh32(value='',label=''): return __Hex(1,value if type(value)==str and value!='' else 4,label)
def bh64(value='',label=''): return __Hex(1,value if type(value)==str and value!='' else 8,label)

def   u_(length,value='',label='',big=0): return __BIT(big,0,length,value,label)
def   s_(length,value='',label='',big=0): return __BIT(big,1,length,value,label)
def   f_(length,value='',Format=0,label='',big=0): return __BIT(big,2,length,value,label) #TODO: support multiple formats (including Nintendo)
def   h_(value,label='',big=0): return __Hex(big,value,label)

def  bu_(length,value='',label=''): return __BIT(1,0,length,value,label)
def  bs_(length,value='',label=''): return __BIT(1,1,length,value,label)
def  bf_(length,value='',Format=0,label=''): return __BIT(1,2,length,value,label) #TODO: support multiple formats (including Nintendo)
def  bh_(value,label=''): return __Hex(1,value,label)

#TODO: allow for a much looser input range with extra operations using __BIT() instead of eval()
def __Term(Term,Value,label=''): return eval(str(Term).lower()+"('"+Value+"')" if type(Value)==str else str(Term).lower()+'('+str(Value)+')')


#usage:
#Field( [1,7,15]        ,255) #int representation...
#Field( ['1','3','4']   ,255) #bit representation...
#>>> [1,7,15]

#Field(['1','3','4'],[1,7,15])
#>>> 255

def __BTV(TV):
    if type(TV)==str: return int(''.join(['1']*int(TV)),2),int(TV) ### slow ###
    if type(TV)==int: return TV,len(bin(TV).replace('0b',''))

def __UBDF(DL,TL,V=0):
    if len(TL): i,l=__BTV(TL[0])
    return __UBDF(DL[1:],TL[1:] if len(TL)>1 else [],(V<<l)|(DL[0]&i)) if len(TL) else V #field(['1','3','4'],[1,7,15]) -> 255

def __UBDL(V,TL,VL=[]):
    if len(TL): i,l=__BTV(TL[-1])
    return __UBDL(V>>l,TL[:-1] if len(TL)>1 else [],VL+[V&i]) if len(TL) else list(reversed(VL)) #field([1,7,15],254) -> [1,7,14]

def Field(Template,value):
    #if Template==[]: template=[len(bin(value))]
    if type(value)==int: #return list
        if value<0:
            ### need to log this in the session info ###
            raise ValueError #"only unsigned (positive) ints can be used as bit fields"
        else: return __UBDL(value,Template)
    if type(value)==list: #return int
        if len(Template)==len(value): #value-list must equal the template
            return __UBDF(value,Template)
        else:
            ### need to log this in the session info ###
            raise ValueError #"the template length must match the value length"
    else:
        ### need to log this in the session info ###
        raise ValueError #"please specify a list or an unsigned (positive) int for the function value"
#provided for conveinence:
def field(Template,value): return Field(Template,value)

#usage:
#value = 3
    
#switch(value)
#if case(0): pass
#if case(1): pass
#if case(2,3): pass
#if case(4): pass

__sw='__UMC_COMMON_NULL__'
def Switch(value): global __sw; __sw=value
def Case(*compair): global __sw; return any([__sw in list(compair),__sw==compair])
#provided for conveinence:
switch = Switch
case = Case

#file handlers
def Skip(length, label=''):
    #TODO: length must be a positive int
    global __f,__o,__c
    if __o[__c]==len(__f[__c])-1: #are we at the end?
        __LOG('%s: wrote %i pad bytes%s'%(__POS(),length,label))
        __f[__c]+=[chr(0)]*length; __o[__c]+=length
    else:
        __LOG('%s: skipped %i bytes%s'%(__POS(),length,label))
        v = __f[__c][__o[__c]:__o[__c]+length]; __o[__c]+=length
        return v

#provided for conveinence:
def skip(length, label=''): return Skip(length,label)
def pad(length, label=''): return Skip(length,label)
    
def Jump(offset, location=0, position=0, label=''):
    #TODO: make sure we aren't jumping past the end of the file
    global __o,__c; l=__POS(); p=__o[__c]; __o[__c]=offset+location+(__o[__c] if position else 0)
    __LOG('%s: jumping to: %s from %s%s'%(l,__POS(),('current position' if position else 'start of file'),label))
    return p

#provided for conveinence:
def jump(offset, location=0, position=0, label=''): return Jump(offset, location, position, label)

#readmode:
#String() #read until chr(0)
#String(8) #read 8 characters
#--String(u8()) #read a string of length u8()

#String([]) #return the files lines as a list
#String([None]) #read until chr(0) for each list entry
#String([4]) #read 4 characters for the current list entry
#--String([u8()]) #read a string of length u8() for each list entry
#--(should work the same as [ String(u8()), String(u8()) ] )

#String(()) #read a single line from the file
#(if the tuple contains any values, it's treated as a list, but returns a tuple)
#NOTE: ^this may change later, so it's reccomended you not use tuples

#String(0) #return a string of the entire file
#!!!for advanced usage only!!!

    
#writemode:
#String('Hello!') #write a string to the file
#String(['string_1\n','string_2']) #write a list of strings (or lines) to the file

#NOTE: due to different formatting variations, only the string itself is written.
#       (use string( S+chr(0) ) or u8(len(S)); string(S) if your formatting calls for it)

__ch__=[chr(i) for i in range(256)] #direct indexing is faster than referencing, I do believe
#although a character array would be slightly faster >_>
def __STR(L,VL=[]): global __ch__; return __STR(L[1:],VL+[__ch__[L[0]]]) if len(L) else ''.join(VL)

def pString(value=None, start='', stop=chr(0), recursive=True, code=None, label=''):
    global __o__,__f,__c,__o; p=__POS()
    pos=__o[__c] #get the current offset in the file
    maxfilelen = len(__f[__c])-1
    if value==None: #read string to stop character or 0x00
        STRING=''

        # set the stop character chr(0) if '' or None
        if stop == None or stop == '': stop=0
        else: stop=ord(stop)

        _start=0
        if start!='': _start = ord(start)

        read = (start==None)
        r=0 #recursion depth
        try:
            while True or pos<=maxfilelen:
                if read:
                    c=__f[__c][pos]; pos+=1 #maintain the internal offset
                    if recursive:
                       if c==_start: r+=1
                       if c==stop:
                           if r>0: r-=1
                           else: break
                    elif c==stop: break
                    else: STRING='%s%s'%(STRING,chr(c)) #return what's read

                else: #once read is True, it can't be set False
                    c=__f[__c][pos]; pos+=1 #maintain the internal offset
                    if start=='':
                        if c not in [0,10,32]: read = True; STRING='%s%s'%(STRING,chr(c))
                    elif c==_start: read = True
                    
                if pos>maxfilelen: #EOF test
                    if STRING=='': return None
                    else: break
        except:
            import sys,traceback
            typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
            print
            traceback.print_exception(
                typ,val,tb#,
                #limit=2,
                #file=sys.stdout
                )
            print
            raw_input('press enter to exit.')
        
        if start==None: startchr = ''
        elif start=='': 
            STRING = STRING.lstrip()
            startchr = 'from whitespace '
        else: startchr = "from '%s' "%start.replace('\n','\\n')

        if code!=None: 
            STRING = STRING.decode(code)
            strcode = '%s encoded '%code
        else: strcode = ''

        if __o__!=None: __o__[__c]=pos; mode=''
        else: mode='pre'
        
        __LOG("%s: %sread %sstring '%s' %sto '%s'%s"%(p,mode,strcode,STRING,startchr,chr(stop).replace('\n','\\n'),label))
        return STRING
    
    elif type(value)==int:
        if value==0: #read entire file
            STRING=[chr(i) for i in __f[__c]]
            __LOG("%s: read file as string"%p)
            #__LOG(''.join(STRING))
            return ''.join(STRING)
        elif pos+value<=maxfilelen: #read length, EOF?
            STRING=''.join(chr(c) for c in __f[__c][pos:pos+value])

            if code!=None: 
                STRING = STRING.decode(code)
                strcode = '%s encoded '%code
            else: strcode = ''

            if __o__!=None: __o__[__c]+=value; mode=''
            else: mode='pre'

            __LOG("%s: %sread %sstring '%s' of length %i%s"%(p,mode,strcode,STRING,value,label))
            return STRING
    
    elif type(value)==str: #write string
        if code!=None:
            value = value.encode(code)
            strcode = '%s encoded '%code
        else: strcode = ''

        __f[__c]+=[ord(c) for c in value]
        if __o__!=None: __o__[__c]+=len(value)

        __LOG("%s: wrote %sstring '%s'%s"%(p,strcode,value,label))
    
    elif type(value)==list:
        if len(value)==0: #readlines
            lines=String(0).split('\n')
            __LOG("%s: read '%i' lines"%(p,len(lines)))
            return lines
        else: #write strings (lines if '\n' added)
            __LOG("%s: wrote list of strings:"%p)
            for Lval in value: String(Lval,code)
            
def String(value=None, start='', stop=chr(0), recursive=False, code=None, label=''):
    global __o__,__o; __o__=__o
    STRING=pString(value, start, stop, recursive, code, label)
    __o__=None; return STRING

#provided for conveinence:
global string, pstring; string,pstring = String,pString

#I can work on the matrix section once I implament numpy

#readmode:
# Matrix(3,4,'bf32')
#>>> [[1,0,0,0],[0,1,0,0],[0,0,1,0]]

# Matrix(3,4,'bf32',flatten=True)
#>>> [1,0,0,0,0,1,0,0,0,0,1,0]

#writemode:
# Matrix(2,2,'u16',[312,200,840,380])
# Matrix(2,2,'u16',[[312,200],[840,380])


##will be made public later:
def __MTX44(): return [[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]]

def Matrix(Rows,Cols,Term,List='',flatten=False,label=''):
    if List == '':
        if __TOGGLE_LOGGING: __LOG('%s: reading %ix%i matrix%s'%(__POS(),Rows,Cols,label))
        return list([[__Term(Term,'',label=' -- [%i][%i]'%(r,c)) for c in range(Cols)] for r in range(Rows)] if not flatten else [
                    __Term(Term,'',label=' -- [%i]'%i) for i in range(Cols*Rows)])
    if type(List)==list:
        if len(List)==Rows: #2D list
            for col in List:
                for Value in col: __Term(Term,Value)
        elif len(List)==(Cols*Rows): #1D list
            for Value in List: __Term(Term,Value)
        else: pass

def MtxTranspose(Mtx): return [
        [Mtx[0][0],Mtx[1][0],Mtx[2][0],Mtx[3][0]],
        [Mtx[0][1],Mtx[1][1],Mtx[2][1],Mtx[3][1]],
        [Mtx[0][2],Mtx[1][2],Mtx[2][2],Mtx[3][2]],
        [Mtx[0][3],Mtx[1][3],Mtx[2][3],Mtx[3][3]]]

def MtxInvert(Mtx):
    det  =  Mtx[0][3]*Mtx[1][2]*Mtx[2][1]*Mtx[3][0] - Mtx[0][2]*Mtx[1][3]*Mtx[2][1]*Mtx[3][0] - \
            Mtx[0][3]*Mtx[1][1]*Mtx[2][2]*Mtx[3][0] + Mtx[0][1]*Mtx[1][3]*Mtx[2][2]*Mtx[3][0] + \
            Mtx[0][2]*Mtx[1][1]*Mtx[2][3]*Mtx[3][0] - Mtx[0][1]*Mtx[1][2]*Mtx[2][3]*Mtx[3][0] - \
            Mtx[0][3]*Mtx[1][2]*Mtx[2][0]*Mtx[3][1] + Mtx[0][2]*Mtx[1][3]*Mtx[2][0]*Mtx[3][1] + \
            Mtx[0][3]*Mtx[1][0]*Mtx[2][2]*Mtx[3][1] - Mtx[0][0]*Mtx[1][3]*Mtx[2][2]*Mtx[3][1] - \
            Mtx[0][2]*Mtx[1][0]*Mtx[2][3]*Mtx[3][1] + Mtx[0][0]*Mtx[1][2]*Mtx[2][3]*Mtx[3][1] + \
            Mtx[0][3]*Mtx[1][1]*Mtx[2][0]*Mtx[3][2] - Mtx[0][1]*Mtx[1][3]*Mtx[2][0]*Mtx[3][2] - \
            Mtx[0][3]*Mtx[1][0]*Mtx[2][1]*Mtx[3][2] + Mtx[0][0]*Mtx[1][3]*Mtx[2][1]*Mtx[3][2] + \
            Mtx[0][1]*Mtx[1][0]*Mtx[2][3]*Mtx[3][2] - Mtx[0][0]*Mtx[1][1]*Mtx[2][3]*Mtx[3][2] - \
            Mtx[0][2]*Mtx[1][1]*Mtx[2][0]*Mtx[3][3] + Mtx[0][1]*Mtx[1][2]*Mtx[2][0]*Mtx[3][3] + \
            Mtx[0][2]*Mtx[1][0]*Mtx[2][1]*Mtx[3][3] - Mtx[0][0]*Mtx[1][2]*Mtx[2][1]*Mtx[3][3] - \
            Mtx[0][1]*Mtx[1][0]*Mtx[2][2]*Mtx[3][3] + Mtx[0][0]*Mtx[1][1]*Mtx[2][2]*Mtx[3][3]
        
    return[[( Mtx[1][2]*Mtx[2][3]*Mtx[3][1] - Mtx[1][3]*Mtx[2][2]*Mtx[3][1] + Mtx[1][3]*Mtx[2][1]*Mtx[3][2] - Mtx[1][1]*Mtx[2][3]*Mtx[3][2] - Mtx[1][2]*Mtx[2][1]*Mtx[3][3] + Mtx[1][1]*Mtx[2][2]*Mtx[3][3]) /det,
            ( Mtx[0][3]*Mtx[2][2]*Mtx[3][1] - Mtx[0][2]*Mtx[2][3]*Mtx[3][1] - Mtx[0][3]*Mtx[2][1]*Mtx[3][2] + Mtx[0][1]*Mtx[2][3]*Mtx[3][2] + Mtx[0][2]*Mtx[2][1]*Mtx[3][3] - Mtx[0][1]*Mtx[2][2]*Mtx[3][3]) /det,
            ( Mtx[0][2]*Mtx[1][3]*Mtx[3][1] - Mtx[0][3]*Mtx[1][2]*Mtx[3][1] + Mtx[0][3]*Mtx[1][1]*Mtx[3][2] - Mtx[0][1]*Mtx[1][3]*Mtx[3][2] - Mtx[0][2]*Mtx[1][1]*Mtx[3][3] + Mtx[0][1]*Mtx[1][2]*Mtx[3][3]) /det,
            ( Mtx[0][3]*Mtx[1][2]*Mtx[2][1] - Mtx[0][2]*Mtx[1][3]*Mtx[2][1] - Mtx[0][3]*Mtx[1][1]*Mtx[2][2] + Mtx[0][1]*Mtx[1][3]*Mtx[2][2] + Mtx[0][2]*Mtx[1][1]*Mtx[2][3] - Mtx[0][1]*Mtx[1][2]*Mtx[2][3]) /det],
           [( Mtx[1][3]*Mtx[2][2]*Mtx[3][0] - Mtx[1][2]*Mtx[2][3]*Mtx[3][0] - Mtx[1][3]*Mtx[2][0]*Mtx[3][2] + Mtx[1][0]*Mtx[2][3]*Mtx[3][2] + Mtx[1][2]*Mtx[2][0]*Mtx[3][3] - Mtx[1][0]*Mtx[2][2]*Mtx[3][3]) /det,
            ( Mtx[0][2]*Mtx[2][3]*Mtx[3][0] - Mtx[0][3]*Mtx[2][2]*Mtx[3][0] + Mtx[0][3]*Mtx[2][0]*Mtx[3][2] - Mtx[0][0]*Mtx[2][3]*Mtx[3][2] - Mtx[0][2]*Mtx[2][0]*Mtx[3][3] + Mtx[0][0]*Mtx[2][2]*Mtx[3][3]) /det,
            ( Mtx[0][3]*Mtx[1][2]*Mtx[3][0] - Mtx[0][2]*Mtx[1][3]*Mtx[3][0] - Mtx[0][3]*Mtx[1][0]*Mtx[3][2] + Mtx[0][0]*Mtx[1][3]*Mtx[3][2] + Mtx[0][2]*Mtx[1][0]*Mtx[3][3] - Mtx[0][0]*Mtx[1][2]*Mtx[3][3]) /det,
            ( Mtx[0][2]*Mtx[1][3]*Mtx[2][0] - Mtx[0][3]*Mtx[1][2]*Mtx[2][0] + Mtx[0][3]*Mtx[1][0]*Mtx[2][2] - Mtx[0][0]*Mtx[1][3]*Mtx[2][2] - Mtx[0][2]*Mtx[1][0]*Mtx[2][3] + Mtx[0][0]*Mtx[1][2]*Mtx[2][3]) /det],
           [( Mtx[1][1]*Mtx[2][3]*Mtx[3][0] - Mtx[1][3]*Mtx[2][1]*Mtx[3][0] + Mtx[1][3]*Mtx[2][0]*Mtx[3][1] - Mtx[1][0]*Mtx[2][3]*Mtx[3][1] - Mtx[1][1]*Mtx[2][0]*Mtx[3][3] + Mtx[1][0]*Mtx[2][1]*Mtx[3][3]) /det,
            ( Mtx[0][3]*Mtx[2][1]*Mtx[3][0] - Mtx[0][1]*Mtx[2][3]*Mtx[3][0] - Mtx[0][3]*Mtx[2][0]*Mtx[3][1] + Mtx[0][0]*Mtx[2][3]*Mtx[3][1] + Mtx[0][1]*Mtx[2][0]*Mtx[3][3] - Mtx[0][0]*Mtx[2][1]*Mtx[3][3]) /det,
            ( Mtx[0][1]*Mtx[1][3]*Mtx[3][0] - Mtx[0][3]*Mtx[1][1]*Mtx[3][0] + Mtx[0][3]*Mtx[1][0]*Mtx[3][1] - Mtx[0][0]*Mtx[1][3]*Mtx[3][1] - Mtx[0][1]*Mtx[1][0]*Mtx[3][3] + Mtx[0][0]*Mtx[1][1]*Mtx[3][3]) /det,
            ( Mtx[0][3]*Mtx[1][1]*Mtx[2][0] - Mtx[0][1]*Mtx[1][3]*Mtx[2][0] - Mtx[0][3]*Mtx[1][0]*Mtx[2][1] + Mtx[0][0]*Mtx[1][3]*Mtx[2][1] + Mtx[0][1]*Mtx[1][0]*Mtx[2][3] - Mtx[0][0]*Mtx[1][1]*Mtx[2][3]) /det],
           [( Mtx[1][2]*Mtx[2][1]*Mtx[3][0] - Mtx[1][1]*Mtx[2][2]*Mtx[3][0] - Mtx[1][2]*Mtx[2][0]*Mtx[3][1] + Mtx[1][0]*Mtx[2][2]*Mtx[3][1] + Mtx[1][1]*Mtx[2][0]*Mtx[3][2] - Mtx[1][0]*Mtx[2][1]*Mtx[3][2]) /det,
            ( Mtx[0][1]*Mtx[2][2]*Mtx[3][0] - Mtx[0][2]*Mtx[2][1]*Mtx[3][0] + Mtx[0][2]*Mtx[2][0]*Mtx[3][1] - Mtx[0][0]*Mtx[2][2]*Mtx[3][1] - Mtx[0][1]*Mtx[2][0]*Mtx[3][2] + Mtx[0][0]*Mtx[2][1]*Mtx[3][2]) /det,
            ( Mtx[0][2]*Mtx[1][1]*Mtx[3][0] - Mtx[0][1]*Mtx[1][2]*Mtx[3][0] - Mtx[0][2]*Mtx[1][0]*Mtx[3][1] + Mtx[0][0]*Mtx[1][2]*Mtx[3][1] + Mtx[0][1]*Mtx[1][0]*Mtx[3][2] - Mtx[0][0]*Mtx[1][1]*Mtx[3][2]) /det,
            ( Mtx[0][1]*Mtx[1][2]*Mtx[2][0] - Mtx[0][2]*Mtx[1][1]*Mtx[2][0] + Mtx[0][2]*Mtx[1][0]*Mtx[2][1] - Mtx[0][0]*Mtx[1][2]*Mtx[2][1] - Mtx[0][1]*Mtx[1][0]*Mtx[2][2] + Mtx[0][0]*Mtx[1][1]*Mtx[2][2]) /det]]

def MtxMultiply(a,b,dst=__MTX44()): #both pointer and return support
    dst[0][0] = a[0][0]*b[0][0] + a[0][1]*b[1][0] + a[0][2]*b[2][0] + a[0][3]*b[3][0]
    dst[0][1] = a[0][0]*b[0][1] + a[0][1]*b[1][1] + a[0][2]*b[2][1] + a[0][3]*b[3][1]
    dst[0][2] = a[0][0]*b[0][2] + a[0][1]*b[1][2] + a[0][2]*b[2][2] + a[0][3]*b[3][2]
    dst[0][3] = a[0][0]*b[0][3] + a[0][1]*b[1][3] + a[0][2]*b[2][3] + a[0][3]*b[3][3]
    dst[1][0] = a[1][0]*b[0][0] + a[1][1]*b[1][0] + a[1][2]*b[2][0] + a[1][3]*b[3][0]
    dst[1][1] = a[1][0]*b[0][1] + a[1][1]*b[1][1] + a[1][2]*b[2][1] + a[1][3]*b[3][1]
    dst[1][2] = a[1][0]*b[0][2] + a[1][1]*b[1][2] + a[1][2]*b[2][2] + a[1][3]*b[3][2]
    dst[1][3] = a[1][0]*b[0][3] + a[1][1]*b[1][3] + a[1][2]*b[2][3] + a[1][3]*b[3][3]
    dst[2][0] = a[2][0]*b[0][0] + a[2][1]*b[1][0] + a[2][2]*b[2][0] + a[2][3]*b[3][0]
    dst[2][1] = a[2][0]*b[0][1] + a[2][1]*b[1][1] + a[2][2]*b[2][1] + a[2][3]*b[3][1]
    dst[2][2] = a[2][0]*b[0][2] + a[2][1]*b[1][2] + a[2][2]*b[2][2] + a[2][3]*b[3][2]
    dst[2][3] = a[2][0]*b[0][3] + a[2][1]*b[1][3] + a[2][2]*b[2][3] + a[2][3]*b[3][3]
    dst[3][0] = a[3][0]*b[0][0] + a[3][1]*b[1][0] + a[3][2]*b[2][0] + a[3][3]*b[3][0]
    dst[3][1] = a[3][0]*b[0][1] + a[3][1]*b[1][1] + a[3][2]*b[2][1] + a[3][3]*b[3][1]
    dst[3][2] = a[3][0]*b[0][2] + a[3][1]*b[1][2] + a[3][2]*b[2][2] + a[3][3]*b[3][2]
    dst[3][3] = a[3][0]*b[0][3] + a[3][1]*b[1][3] + a[3][2]*b[2][3] + a[3][3]*b[3][3]
    return dst


#readmode:
#StructArr(['u32','u32']) #read until sum(Current) == 0
#   ^return: [[12645,83460],[43751,83362]] ([0,0] is not included)
#StructArr(['u32','u8','u8'],4) #read 4 structures
#   ^return: [['u32','u8','u8'],['u32','u8','u8'],['u32','u8','u8'],['u32','u8','u8']]
#StructArr(['u32','u8','u8'],['*',255,'*']) #read until StopStruct ('*' is a wild card)
#   ^return: [[0,16,0],[8060,124,30],[64032,118,0],[0,20,30]] (stopstruct == [0,255,0] or [0,255,2])

#writemode:
#StructArr('u8',[255,128,180,16]) #write the list of structures
#   Note: you don't have to use the list if using a single value. eg: StructArr('u16',436) (same as u16(436))

#TODO:
#string values [ 'string' ,'u32','u16']
#varrying structure array (a data value determines the used structure (from a set of structures) in the array)
#   ^Possible Function layout: StructArr(enm,tpl,val) (excluding writemode)
#   enm - index enumeration template and values
#   tpl - Template array (Template selected from value enumeration (1))
#   val - Value (nothing different here)
#   Note: for basic usage, just omit enm with '' ( StructArr('',Template,Value) )
#(there's still quite a bit to plan before even starting on this feature, so be patient)

def StructArr(Template,Value=''): #needs a performance boost (redo everything)
    global __f,__o,__c
    if type(Template)==tuple: Template=list(Template)
    if type(Template)!=list: Template=[Template]

    if type(Value)==tuple: Value=list(Value) #Tuples aren't really supported... yet >_>

    def RS(t):
        L=[]
        for Tm in t: #read single structure
            if type(Tm)==list: RS(Tm)
            else: R=__Term(Tm,''); L.append(0 if R==None else R) #returns 0 instead of None
        return L
    def WS(t,v): #write single structure
        for I,Tm in enumerate(t):
            if type(Tm)==list: WS(Tm,v[I]) #Template[I] == []
            else: __Term(Tm,v[I])
        
    if Value == '': #read until 0 struct
        __LOG("%s: read structures of %s reaching a 0 struct."%(__POS(),str(Template)))
        Structs=[]; cont=1
        while IWLD(cont):
            Struct = RS(Template)
            if type(Struct)==list: cont=(0 if sum(Struct)==0 else 1)
            else: cont=(0 if int(Struct)==0 else 1)
            if cont: Structs.append(Struct)
        return Structs
        
    if type(Value) == int:
        if __o[__c]==len(__f[__c])-1: #are we at the end?
             WS(Template,[Value]) #write the int value if so
             __LOG("%s: wrote 1 structure of %s"%(__POS(),str(Template)))
        else:
            __LOG('%s: read %i structures of %s'%(__POS(),Value,str(Template)))
            return [RS(Template) for v in range(Value)] #read count
            
    if type(Value) == list:
        if __o[__c]==len(__f[__c])-1: #are we at the end?
            for S in Value: #write structs
                if type(S)!=(list or tuple): S=[S]
                WS(Template,S)
            __LOG("%s: wrote %i structures of %s"%(__POS(),len(Value),str(Template)))
        else: #read until StopStruct
            __LOG("%s: read structures of %s stopping at %s"%(__POS(),str(Template),str(Value)))
            Structs=[]; cont=1
            while IWLD(cont):
                Struct = RS(Template)
                if Struct==[(Struct[I] if V=='*' else V) for I,V in enumerate(Value)]: cont=0
                else: Structs.append(Struct)
            return Structs
        
    if type(Value) == float:
        WS(Template,[Value]) #write the float value
        __LOG("%s: wrote 1 structure of %s"%(__POS(),str(Template)))
        


