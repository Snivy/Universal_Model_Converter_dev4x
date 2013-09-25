from data.COMMON import * #essentials
Header( 0.001,              #Script Version (for updates)
       ('Blender data file',['blend','blend1','blend2']),   #model activation
       ('',['']),   #anim activation
       [''])    #included libs
#specified Library's functions will be included with COMMON
def str_align(L,val=4):
    count=len(L)+sum(len(S) for S in L)
    size=0
    while size<count: size+=val
    return size-count
        

def ImportModel(T,C):
    version_max = 249 #don't change this
    #I have docs for 248/9, not for 26x
    #I'm still looking into the format
    
    #global header:
    magic = string(7)
    P = (4 if string(1)=='_' else 8) #pointer_size: '_' = 32bit, '-' = 64bit
    E = (0 if string(1)=='v' else 1) #endian: 'v' = little 'V' = big
    version = int(string(3))
    
    if version>version_max:
        print "your file version is too high ("+str(version)+")"
        print "this plugin supports up to version "+str(version_max)
        
    else:
        #TODO:
        ##StructArr(['' #<- no implementation for strings yet
        ##   ,('b' if E else '')+'u32'
        ##   ,('b' if E else '')+'u_'+str(P) #<- '(b)u_(8)' not implemented yet 
        ##   ,('b' if E else '')+'u32'
        ##   ,('b' if E else '')+'u32'
        ##   ,[ #internal structure values can't validate sub-structure types yet
        ##       ]],['ENDB','*','*','*','*','*'])
        #^should return a structure list in Blender's native data format

        
        #I might not scrap this code though
        #while StructArr is better at all standards,
        #all the extra implamentations makes data validation alot slower...
        #where-as the code here (being alot more complex) was designed for this particular task.
        while True: 
            #header:
            code = string(4,' -- Code')
            L=[' -- size',' -- Old_Memory_Address',' -- SDNA_Index',' -- Structure_Count']
            sz,M_A,SDNA,cnt = u32('',L[0],E),u_(P,'',L[1],E),u32('',L[2],E),u32('',L[3],E)
            switch(code)
            if case('ENDB'): break
            elif case('DNA1'):
                identifier=string(4); sz-=4 #'SDNA'
                
                Nameidentifier=string(4); sz-=4 #'NAME'
                NCount=u32('',' -- Name_Count',E); sz-=4
                Names = string([None]*NCount)
                sk=str_align(Names); skip(sk)
                sz-=(len(Names)+sum(len(S) for S in Names)+sk)
                
                Typeidentifier=string(4); sz-=4 #'TYPE'
                TCount=u32('',' -- Type_Count',E); sz-=4
                Types = string([None]*TCount)
                sk=str_align(Types); skip(sk)
                sz-=(len(Types)+sum(len(S) for S in Types)+sk)

                Lengthidentifier=string(4); sz-=4 #'TLEN'
                Lengths=u16(['']*TCount,'',E); sz-=2*TCount

                Structidentifier=string(4); sz-=4 #'STRC'
                SCount=u32('',' -- Struct_Count',E); sz-=4
                Structs = u16(['']*SCount,'',E); sz-=2*SCount

                FCount = u16('',' -- Field_Count',E)
                Fields = u16(['']*FCount,'',E); sz-=2*FCount
                
            else:
                skip(sz)
                    

        #convert Blender data to UMC data (using UMC functions)

def XExportModel(T,C): #later
    pass
