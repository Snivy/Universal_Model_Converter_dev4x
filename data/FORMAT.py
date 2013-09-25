#1
#v 0.001

from ERROR import *
from LOGGING import LOG as __LOG

"""

- SetMaterial(): TODO
###
at this moment, the current data standards don't allow for proper materials.
I'm already working on resolving this.
current plans include:
#1 - set the active object's type to 'mesh' (if not already)
#2 - create a new active material in the data library, or index a material from the data library
#3 - set the material index in the Mesh-type Object
(values for the Shader will be integrated within the Material)

- SetMatNode(): TODO
###
these are extremely complicated and will take quite a while to solve
(this means no color animations, ramps or special effects unachievable bt the shader alone)
---
(a material must be active in a Mesh-type Object for this to take affect)

- SetLight(): TODO
###
I have to learn about these a little more :P


"""
#global public usage variables:
global UMC_POINTS,UMC_LINES,UMC_LINESTRIP,UMC_LINELOOP,UMC_TRIANGLES,UMC_TRIANGLESTRIP,UMC_TRIANGLEFAN,UMC_QUADS,UMC_QUADSTRIP,UMC_POLYGON
UMC_POINTS,UMC_LINES,UMC_LINESTRIP,UMC_LINELOOP,UMC_TRIANGLES,UMC_TRIANGLESTRIP,UMC_TRIANGLEFAN,UMC_QUADS,UMC_QUADSTRIP,UMC_POLYGON = range(10)

#global defaults (bypassing re-definition from functions (speedup))
DLRS=[0.0,0.0,0.0, 0.0,0.0,0.0, 1.0,1.0,1.0]
DM=[[1.0,0.0,0.0,0.0], [0.0,1.0,0.0,0.0], [0.0,0.0,1.0,0.0], [0.0,0.0,0.0,1.0]]
#___________________________________________________________________________________________

#[Materials,Nodes,Scenes,Objects]
import VIEWER

#Active Data:
ActiveScene = 0
ActiveObject = None
ActiveMaterial = None
ActivePrimitive = 0 #in active object

def __GetOID(N): #check for specified object name/ID
    ID=''
    if type(N)==int: ID=('' if N>len(VIEWER.Libs[3]) else N) #N=1
    else: #N="Object1"
        ###need a faster indexing method here
        ###VIEWER.Libs[3].index(N) won't work as VIEWER.Libs[3] values are lists with random internal datas
        for I,O in enumerate(VIEWER.Libs[3]): #TODO: use a while loop (stop the loop if found)
            if O[0]==N: ID=I
    return ID #return int() if found
    
#___________________________________________________________________________________________

SceneCount = 0
#create a new scene, or activate the specified scene
def SetScene( Name="Scene0" ):
    global SceneCount,ActiveScene
    if SceneCount==0: #change the default scene name
        VIEWER.Libs[2][0][0]=(Name if type(Name)==str else "Scene"+str(SceneCount))
        SceneCount+=1
    else: #user defined scenes already exist
        SceneIndex = None
        #TODO: usa a while loop
        for Index,Scene in enumerate(VIEWER.Libs[2]): #check for specified scene name/index
            if Scene[0]==Name or Index==Name: SceneIndex=Index
        if SceneIndex == None: #create a new scene
            VIEWER.Libs[2]+=[Name if type(Name)==str else "Scene"+str(SceneCount)]
            ActiveScene=len(VIEWER.Libs[2]) #set the active scene index to the newly added scene
            SceneCount+=1
        else: ActiveScene=SceneIndex #set the active scene index to the specified scene
    __LOG('---FORMAT---: created Scene: %s'%Name)
    SetScene.func_defaults=( "Scene"+str(SceneCount), )

#TODO:
#- active scene rename: SetScene( [('Name' or Index), "NewName"] )
#^this will rename the scene while setting it to active
    
#___________________________________________________________________________________________

ObjectSceneID = [] #the indexed object's scene index
#create a new object in the active scene, or activate and change the data in a specified object
#(if a specified object exists in another scene, that object's scene will be set as active)
def SetObject( Name="Object0", Viewport=0, LocRotSca=[], Sub_Name='', ParentName='' ):
    global ActiveScene,ActiveObject,ObjectSceneID,DLRS
    ObjectLib=VIEWER.Libs[3]
    #Verify Data: (use Defaults if neccesary)
    N  = (ObjectLib[Name][0] if (type(Name)==int and Name>-1 and Name<(len(ObjectLib)+1) #get the name of the specified object
                                 ) else (Name if type(Name)==str else "Object"+str(len(ObjectLib)))) #N must be a string
    VP = (Viewport if (Viewport>0 and Viewport<25) else 1) #must be 1 to 24
    LRS= (DLRS if len(LocRotSca)!=9 else LocRotSca) #TODO: advanced LRS verification
    SD = ["",(N if (Sub_Name=='' or type(Sub_Name)!=str) else Sub_Name),[],[]]
    P  = (__GetOID(ParentName) if ParentName!=('__REMOVE__' or '') else ParentName)
    
    OID=__GetOID(N) if len(VIEWER.Libs[3])>0 else '' #try to get an active object index
    if OID=='': #if this is a new object:
        VIEWER.Libs[3].append([N,VP,LRS,SD,(P if len(VIEWER.Libs[3])>0 else '')]) #ignore parent index if this is the first object
        VIEWER.Libs[2][ActiveScene][1]+=[len(VIEWER.Libs[3])-1]
        ObjectSceneID+=[ActiveScene]
        ActiveObject=len(VIEWER.Libs[3])-1
    else: #set the active object to the specicified object and change it's data
        ActiveObject,ActiveScene = OID,ObjectSceneID[OID]; AO=ObjectLib[OID]
        VIEWER.Libs[3][OID]=[ AO[0], #reset the object's data:
            ((VP if Viewport!=0 else AO[1]) if AO[1]!=VP else AO[1]),
            ((LRS if LRS!=DLRS else AO[2]) if AO[2]!=LRS else AO[2]),
            [AO[3][0],(AO[3][1] if Sub_Name=='' else SD[1]),AO[3][2],AO[3][3]], #reset sub data name (not data)
            ((P if ObjectLib[OID][4]!=P else ObjectLib[OID][4]) if P!='__REMOVE__' else '')]
            
    __LOG('---FORMAT---: created Object: %s'%Name)
    SetObject.func_defaults=( "Object"+str(len(VIEWER.Libs[3])), 0, [], '', '' )

#TODO:
#- verify the object doesn't have multiple parents (important)

#- active object rename: SetObject( [('Name' or Index), "NewName"], ... )
#^this will rename the specified object while setting it active and editing it's data

#___________________________________________________________________________________________

#set the active object's type to Rig and create a new bone within it, or change the data of an existing bone
#(you will recieve an error if used on another Object type)
#(you will also recieve an error if no object is defined)
def SetBone( Name="Bone0", Viewport=0, LocRotSca=[], BindMtx=[], ParentName='', PreviousName='' ):
    global ActiveObject,BoneLib,N,VP,LRS,BM,PA,PR,DLRS
    BoneLib=VIEWER.Libs[3][ActiveObject][3][3]

    def GetID(S): #check for specified bone name/ID
        global BoneLib
        ID=''
        if type(S)==int: ID=('' if S>len(BoneLib) else S) #S=1
        else: #S="Bone1"
            ###need a faster indexing method here
            ###BoneLib.index(N) won't work as BoneLib values are lists with random internal datas
            for I,B in enumerate(BoneLib):
                if B[0]==S: ID=I
        return ID
    
    #Verify Data: (use Defaults if neccesary)
    N  = (Name if type(Name)==str else "Bone"+str(len(BoneLib)))
    VP = (Viewport if (Viewport>0 and Viewport<25) else 1)
    LRS= (DLRS if len(LocRotSca)!=9 else LocRotSca) #TODO: advanced LRS verification
    BM = (DM if len(BindMtx)!=4 else BindMtx) #TODO: advanced matrix verification
    PA = (GetID(ParentName) if ParentName!=('__REMOVE__' or '') else '')
    PR = (GetID(PreviousName) if PreviousName!='' else '')

    def Set():
        global ActiveObject,N,VP,LRS,BM,PA,PR,BoneLib
        #manage the bone data:
        BID= GetID(N) if len(BoneLib)>0 else '' #try to get an active object index
        if BID=='': VIEWER.Libs[3][ActiveObject][3][3]+=[[N,VP,LRS,BM,PA,PR]] #add a new bone
        else: VIEWER.Libs[3][ActiveObject][3][3][BID]=[BoneLib[BID][0], #edit the specified bone
            ((VP if Viewport!=0 else BoneLib[BID][1]) if BoneLib[BID][1]!=VP else BoneLib[BID][1]),
            ((LRS if LRS!=DLRS else BoneLib[BID][2]) if BoneLib[BID][2]!=LRS else BoneLib[BID][2]),
            ((BM if BM!=DM44 else BoneLib[BID][3]) if BoneLib[BID][3]!=BM else BoneLib[BID][3]),
            ((PA if ParentName!='' else BoneLib[BID][4]) if BoneLib[BID][4]!=PA else BoneLib[BID][4]),
            ((PR if ParentName!='' else BoneLib[BID][5]) if BoneLib[BID][5]!=PR else BoneLib[BID][5])]
            #^- need to check for previous bone looping (in case of user error)
        __LOG('---FORMAT---: created Bone: %s'%Name)
        
    #validate the active object
    if len(VIEWER.Libs[3])>0:
        if VIEWER.Libs[3][ActiveObject][3][0]=="": VIEWER.Libs[3][ActiveObject][3][0]="_Rig";Set() #set to "_Rig" and append a bone
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Rig": Set() #append a bone
        else: print 'Unable to append Bone to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    SetBone.func_defaults=( "Bone"+str(len(VIEWER.Libs[3][ActiveObject][3][3])), 0, [], [], '', '' )

#TODO:
#- instead of ignoring the invalid bone's data, create a new rig object to append it to
#^you will then be able to parent the "ignored" bones to their proper object using a 3D editor
#NOTE: only 1 object will be created to be the place-holder for the ignored bones (instead of 1 object for each ignored bone)
    
#- rename bone: SetBone( [('Name' or Index), "NewName"], ... )
#^this will rename the specified bone while also editing it's data
    
#___________________________________________________________________________________________

#set the active object's type to Mesh and append a primitive in it's data
#(you will recieve an error if used on another Object type)
#(you will also recieve an error if no object is defined)

def SetPrimitive( Name=UMC_TRIANGLES ):
    #TODO: figure out how to get the var itself to display (not it's value)
    if len(VIEWER.Libs[3])>0: #validate the active object
        if VIEWER.Libs[3][ActiveObject][3][0]=="":
            VIEWER.Libs[3][ActiveObject][3][0]="_Mesh"
            VIEWER.Libs[3][ActiveObject][3][3]=[[],[],[[],[]],[[],[],[],[],[],[],[],[]],[],[]]
            VIEWER.Libs[3][ActiveObject][3][3][5]+=[[Name,[]]] #set to "_Mesh" and append a primitive
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh":
            VIEWER.Libs[3][ActiveObject][3][3][5]+=[[Name,[]]] #append a primitive
        else: #return error
            print 'Unable to append Primitive to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    
    SetPrimitive.func_defaults=( Name, )
    
#TODO:
#- index the proper primitive to add facepoints to
#^(I personally havn't seen a format you'd need this option for, but the possibility of it still lies about)

#___________________________________________________________________________________________

#set the active object's type to Mesh and append a valid Vector List to it's data
#(you will recieve an error if used on another Object type)
#(you will also recieve an error if no object is defined)
def SetVerts( List=[] ):
    global ActiveObject
    if len(VIEWER.Libs[3])>0:
        if VIEWER.Libs[3][ActiveObject][3][0]=="":
            VIEWER.Libs[3][ActiveObject][3][0]="_Mesh"
            VIEWER.Libs[3][ActiveObject][3][3]=[List,[],[[],[]],[[],[],[],[],[],[],[],[]],[],[]]
            __LOG('---FORMAT---: set Vert List with %i verts'%len(List))
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh": 
            VIEWER.Libs[3][ActiveObject][3][3][0]=List
            __LOG('---FORMAT---: set Vert List with %i verts'%len(List))
        else: print 'Unable to append Vert List to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    
def SetNormals( List=[] ):
    global ActiveObject
    if len(VIEWER.Libs[3])>0:
        if VIEWER.Libs[3][ActiveObject][3][0]=="":
            VIEWER.Libs[3][ActiveObject][3][0]="_Mesh"
            VIEWER.Libs[3][ActiveObject][3][3]=[[],List,[[],[]],[[],[],[],[],[],[],[],[]],[],[]]
            __LOG('---FORMAT---: set Normal List with %i normals'%len(List))
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh": 
            VIEWER.Libs[3][ActiveObject][3][3][1]=List
            __LOG('---FORMAT---: set Normal List with %i normals'%len(List))
        else: print 'Unable to append Normal List to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    
def SetColors( List0=[], List1=[] ):
    global ActiveObject
    if len(VIEWER.Libs[3])>0:
        if VIEWER.Libs[3][ActiveObject][3][0]=="":
            VIEWER.Libs[3][ActiveObject][3][0]="_Mesh"
            VIEWER.Libs[3][ActiveObject][3][3]=[[],[],[List0,List1],[[],[],[],[],[],[],[],[]],[],[]]
            __LOG('---FORMAT---: set Color Lists with [%i,%i] colors'%(len(List0),len(List1)))
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh": 
            VIEWER.Libs[3][ActiveObject][3][3][2]=[List0,List1]
            __LOG('---FORMAT---: set Color Lists with [%i,%i] colors'%(len(List0),len(List1)))
        else: print 'Unable to append Color Lists to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    
def SetUVs( List0=[], List1=[], List2=[], List3=[], List4=[], List5=[], List6=[], List7=[] ):
    global ActiveObject
    if len(VIEWER.Libs[3])>0:
        if VIEWER.Libs[3][ActiveObject][3][0]=="":
            VIEWER.Libs[3][ActiveObject][3][0]="_Mesh"
            VIEWER.Libs[3][ActiveObject][3][3]=[[],[],[[],[]],[List0,List1,List2,List3,List4,List5,List6,List7],[],[]]
            __LOG('---FORMAT---: set UV Lists with [%i,%i,%i,%i,%i,%i,%i,%i] UVs'%(
                len(List0),len(List1),len(List2),len(List3),len(List4),len(List5),len(List6),len(List7)))
        elif VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh": 
            VIEWER.Libs[3][ActiveObject][3][3][0]=[List0,List1,List2,List3,List4,List5,List6,List7]
            __LOG('---FORMAT---: set UV Lists with [%i,%i,%i,%i,%i,%i,%i,%i] UVs'%(
                len(List0),len(List1),len(List2),len(List3),len(List4),len(List5),len(List6),len(List7)))
        else: print 'Unable to append UV Lists to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"\nignoring current data'
    else: print 'please define an object'
    
#TODO:
#- validate vector lists

#- Validate replacements (don't replace a data with a default unless specified)
    
#___________________________________________________________________________________________

#Vectors: [ X, Y(, Z) ]
#Colors: [R,G,B,A] int( 0 : 255 ) OR float( 0.0 : 1.0 )
#^be careful not to specify an int when your type is float (for colors)
#^2D Verts and Normals are allowd.

#append a facepoint to the active primitive with the specified vectors
#(colors and uv's in list format are assumed to be single channel, and are read as such)
def SetFacepoint( Vert='', Normal='', Color='', UV='' ):
    global ActiveObject
    #verify we havn't switched objects to an invalid type before trying to add facepoints:
    if VIEWER.Libs[3][ActiveObject][3][0]=="_Mesh": #we can only set the facepoints of an active mesh object
        if len(VIEWER.Libs[3][ActiveObject][3][3])>0: #we can't append facepoints to an object with no primitives.
            Colors,UVs = VIEWER.Libs[3][ActiveObject][3][3][2],VIEWER.Libs[3][ActiveObject][3][3][3]
            
            def Index(value,List,Type=''): #returns either a valid index or ''
                if type(value)==list: #[X,Y(,Z)] or [I/R(,A/G(,B(,A)))]
                    try: return List.index(value)
                    except: 
                        List+=[value]
                        __LOG('---FORMAT---: set %s: %s'%(Type,str(value)))
                        return List.index(value) #vector or color
                elif type(value)==int: return value #index (doesn't validate against len(list))
                elif type(value)==str: return '' #no vector (validate any string to '')
                
            VID = Index(Vert,VIEWER.Libs[3][ActiveObject][3][3][0],'Vert')
            
            NID = Index(Normal,VIEWER.Libs[3][ActiveObject][3][3][1],'Nornal')
                
            CIDs = ( (Index(Color[0],Colors[0],'Color0')
                     ,(Index(Color[1],Colors[1],'Color1') if len(Color)==2 else '')
                     ) if type(Color)==tuple else (Index(Color,Colors[0]),'') )
            
            UVIDs = ( (Index(UV[0],UVs[0],'UV0')
                      ,(Index(UV[1],UVs[1],'UV1') if len(UV)>=2 else '')
                      ,(Index(UV[2],UVs[2],'UV2') if len(UV)>=3 else '')
                      ,(Index(UV[3],UVs[3],'UV3') if len(UV)>=4 else '')
                      ,(Index(UV[4],UVs[4],'UV4') if len(UV)>=5 else '')
                      ,(Index(UV[5],UVs[5],'UV5') if len(UV)>=6 else '')
                      ,(Index(UV[6],UVs[6],'UV6') if len(UV)>=7 else '')
                      ,(Index(UV[7],UVs[7],'UV7') if len(UV)==8 else '')
                      ) if type(UV)==tuple else (Index(UV,UVs[0]),'','','','','','','')
                    )
            
            VIEWER.Libs[3][ActiveObject][3][3][5][-1][1]+=[[VID,NID,CIDs,UVIDs]]
                
            __LOG('---FORMAT---: set Facepoint: [%s, %s, %s, %s]'%(str(VID),str(NID),str(CIDs),str(UVIDs)))
        else: print 'unable to append to a non-existant primitive'
    else:
        print 'Unable to append Facepoint to Object of type: "'+VIEWER.Libs[3][OID][3][0].split('_')[1]+'"'
        print 'Make sure the active object is a Mesh-type Object before trying to append Facepoints'

#TODO:
#- strict-er inputs (no errors allowed)

#___________________________________________________________________________________________

#this function is used to give a bone weight to the current (existing) vert
def SetWeight( BoneName=0, Weight=1.0, VertID='' ): #VertID is a TODO (should accept both list and int)
    global ActiveObject
    #verify we havn't switched objects to an invalid type:
    if ActiveObject != None:
        SD = VIEWER.Libs[3][ActiveObject][3]

        if VIEWER.Libs[3][ActiveObject][4] != '':
            ParentObject = VIEWER.Libs[3][VIEWER.Libs[3][ActiveObject][4]]
            if ParentObject[3][0] == "_Rig": #parent object must be a _Rig object
                if type(BoneName) == int: #check for the bone name in the parent _Rig oblect
                    if BoneName < len(ParentObject[3][3]): #is the index w/in the bone count?
                        BoneName = ParentObject[3][3][BoneName][0] #must be a string
                    else: BoneName = 'Bone'+str(BoneName) #must be a string
            else: BoneName = 'Bone'+str(BoneName)
        else: BoneName = 'Bone'+str(BoneName)
        
        if SD[0]=="_Mesh":
            if len(SD[3][5]): #Has Primitives
                if len(SD[3][5][-1][1]): #Has facepoints
                    if len(SD[3][0]): #Has Verts
                        #WGrps,found,WGid = SD[3][4],0,0
                        WGrps,found = SD[3][4],0
                        Vid = SD[3][5][-1][1][-1][0] #vert index from current primitive's current facepoint
                        if len(WGrps)>0:
                            #'''
                            while WGid < len(WGrps)-1 or not found: #faster (stops if found or at end)
                                WGN,WGFs,WGVs = WGrps[WGid]
                                if WGN == BoneName: #append Vid to an existing weight group
                                    WFid = len(WGFs) #assume the weight is a new weight
                                    try: WFid = WGFs.index(Weight) #try to get a valid weight index
                                    except: VIEWER.Libs[3][ActiveObject][3][3][4][WGid][1]+=[Weight] #append new weight
                                    VIEWER.Libs[3][ActiveObject][3][3][4][WGid][2]+=[[Vid,WFid]]
                                    found = 1
                                WGid += 1
                            ''' #^???throws an indexing error...???
                            for WGid,WG in enumerate(WGrps):
                                WGN,WGFs,WGVs = WG
                                if WGN == BoneName: #append Vid to an existing weight group
                                    WFid = len(WGFs) #assume the weight is a new weight
                                    try: WFid = WGFs.index(Weight) #try to get a valid weight index
                                    except: VIEWER.Libs[3][ActiveObject][3][3][4][WGid][1].append(Weight) #append new weight
                                    VIEWER.Libs[3][ActiveObject][3][3][4][WGid][2].append([Vid,WFid])
                                    found = 1
                            #'''
                        if not found: #append Vid to a new weight group
                            VIEWER.Libs[3][ActiveObject][3][3][4]+=[[BoneName,[Weight],[[Vid,0]]]]
                        

    #check get the vert index and append it to the specified weight
    
    #VIEWER.Libs[3][ActiveObject][3][3][-1][-1][4].append([Weight,Bones])

#TODO:
#- use VID to index a specific vert. (some model formats may force you to use this)
#(currently indexing the last used vert (OpenGL-style))

#___________________________________________________________________________________________


#return the mesh-objects from either the specified scene, or from the object library
def GetMeshObjects(Scene=''):
    def Sort(List):
        L=[]
        for ID,Object in enumerate(List):
            if type(Object)==int:
                if VIEWER.Libs[3][Object][3][0]=="_Mesh": L+=[Object]
            else:
                if Object[3][0]=="_Mesh": L+=[ID]
        return L
    
    if type(Scene)==str:
        if Scene=='': return Sort(VIEWER.Libs[3])
        else: return Sort(VIEWER.Libs[2][VIEWER.Libs[2].index(Scene)][1])
    elif type(Scene)==int: return Sort(VIEWER.Libs[2][Scene][1])

#TODO: better error handling on SceneLib.index(Scene) and SceneLib[Scene]

#___________________________________________________________________________________________

def GetObjectName(Object=0):
    if type(Object)==int: return VIEWER.Libs[3][Object][0]

#___________________________________________________________________________________________

def GetVerts(Object=''):
    if type(Object)==int: return VIEWER.Libs[3][Object][3][3][0]
    elif type(Object)==str: VIEWER.Libs[3][__GetOID(Object)][3][3][0]

#___________________________________________________________________________________________

def GetNormals(Object=''):
    if type(Object)==int: return VIEWER.Libs[3][Object][3][3][1]
    elif type(Object)==str: VIEWER.Libs[3][__GetOID(Object)][3][3][1]

#___________________________________________________________________________________________

def GetColors(Object='',Channel=0):
    if type(Object)==int: return VIEWER.Libs[3][Object][3][3][2][Channel]
    elif type(Object)==str: VIEWER.Libs[3][__GetOID(Object)][3][3][2][Channel]

#___________________________________________________________________________________________

def GetUVs(Object='',Channel=0):
    if type(Object)==int: return VIEWER.Libs[3][Object][3][3][3][Channel]
    elif type(Object)==str: VIEWER.Libs[3][__GetOID(Object)][3][3][3][Channel]

#___________________________________________________________________________________________

def GetPrimitives(Object=''):
    if type(Object)==int: return VIEWER.Libs[3][Object][3][3][5]
    elif type(Object)==str: VIEWER.Libs[3][__GetOID(Object)][3][3][5]

#___________________________________________________________________________________________

def AsTriangles( PrimitivesList, Option=0 ):
    Triangles,Quads = [],[] #NOTE: "Quads" is only for single primitive conversion
    for Primitive in PrimitivesList:
        index = 0;Tris = [3,[]]
        switch(Primitive[0])
        if case(0): #points
            if option==(1 or 3): pass #primitive is not Tri/Quad
            else: Triangles+=[Primitive]
        if case(1): #lines
            if option==(1 or 3): pass #primitive is not Tri/Quad
            else: Triangles+=[Primitive]
        if case(2): #line-strips
            if option==(1 or 3): pass #primitive is not Tri/Quad
            else: Triangles+=[Primitive]
        if case(3): #line-loops
            if option==(1 or 3): pass #primitive is not Tri/Quad
            else: Triangles+=[Primitive]
        if case(4): #triangles
            if option==(1 or 3): Triangles+=Primitive[1] #single primitive
            else: Triangles+=[Primitive]
        if case(5): #tri-strips
            while index != len(Primitive[1])-2:
                T=[Primitive[1][index],Primitive[1][index+1],Primitive[1][index+2]]
                if T[0] != T[1] and T[0] != T[2] and T[1] != T[2]: Tris[1]+=(T.reverse() if index%2 else T)
                index += 1
            if option==(1 or 3): Triangles+=Tris[1] #single primitive
            else: Triangles+=[Tris]
        if case(6): #tri-fans
            P=[Primitive[1][index]]
            while index != len(Primitive[1])-2:
                T=P+[Primitive[1][index+1],Primitive[1][index+2]]
                if T[0] != T[1] and T[0] != T[2] and T[1] != T[2]: Tris[1]+=(T.reverse() if index%2 else T)
                index += 1
            if option==(1 or 3): Triangles+=Tris[1] #single primitive
            else: TrianglesList+=[Tris]
        if case(7): #quads
            while index != len(Primitive[1]):
                Q=[Primitive[1][index],Primitive[1][index+1],Primitive[1][index+2],Primitive[1][index+3]]
                Tris[1]+=[Q[0],Q[1],Q[2],Q[1],Q[2],Q[3]] #TODO: face flipping
                index += 4
            switch(option)
            if case(0): Triangles+=[Tris]
            if case(1): Triangles+=Tris[1]
            if case(2): Triangles+=[Primitive]
            if case(3): Quads+=Primitive[1]
        if case(8): #quad-strips
            Qds=[]
            pass #unknown handling atm (TODO)
        if case(9): #Polygons
            pass #unknown handling atm (TODO)
    switch(Option)
    if case(0): return Triangles#................multiple triangle primitives
    if case(1): return [[3,Triangles]]#..........single triangle primitive
    if case(2): return Triangles#................multiple triangle and quad primitives
    if case(3): return [[3,Triangles],[6,Quads]]#single triangle and quad primitive

'''
def convertFromTriangles( TrianglesList ):
    P=ConvertToTriangles(TrianglesList,1) #only works for single tris atm
'''
