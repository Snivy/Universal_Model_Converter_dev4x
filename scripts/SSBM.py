from data.COMMON import * #essentials
Header( 0.001,              #Script Version (for updates)
       ('Melee',['dat']),   #model activation
       ('Melee',['dat']),   #anim activation
       [''])#revolution'])  #included libs
#gist number: 2757147

#for the work I've done to get this far, this should really be v3.6 heh...
#but because this is a first release for a new program, why waste it. ^_^

from data.COMMON import * #essentials + Libs
#the functions from the included libs are imported directly into COMMON
#(you don't need the lib's name to use it's function)

#def ImportGUI(): #still in development
#this function is called before ImportModel
#-----------

def ImportModel(T,C):
    from math import cos,sin,pi #please refrain from using imports (these will be supported by dev5)
    global degrad; degrad = pi/180

    #used by _Bone and _Object for storing and reading the transformed matrices
    global bones; bones=[] #bone offsets
    global matrices; matrices=[] #matrices ( bind,invbind = matrices[ bones.index(bone_offset) ] )
    
    def MTX44(): return [[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]]

    def TransformMatrix( translate, rotate, scale ):
        global degrad
        cosx = cos(rotate[0] * degrad)
        sinx = sin(rotate[0] * degrad)
        cosy = cos(rotate[1] * degrad)
        siny = sin(rotate[1] * degrad)
        cosz = cos(rotate[2] * degrad)
        sinz = sin(rotate[2] * degrad)

        return [
            [   scale[0] * cosy * cosz,
                scale[1] * (sinx * cosz * siny - cosx * sinz),
                scale[2] * (sinx * sinz + cosx * cosz * siny),
                translate[0]],
            [   scale[0] * sinz * cosy,
                scale[1] * (sinx * sinz * siny + cosz * cosx),
                scale[2] * (cosx * sinz * siny - sinx * cosz),
                translate[1]],
            [   -scale[0] * siny,
                scale[1] * sinx * cosy,
                scale[2] * cosx * cosy,
                translate[2]],
            [0.0,0.0,0.0,1.0]]

    '''this block will change'''
    def str_off(offset): #returns a hex-string of a given int offset '0x00000000'
        STRING=(hex(offset).replace('0x','')).upper()
        return '0'*(8-len(STRING))+STRING
    
    ################################################################################################
    '''object-block functions'''
    def vector(D_Type, exponent, offset=None, IS3D=1): #returns an [X,Y(,Z)] vector
        #TODO: direct data values (if ever found)
        
        def DataType(DT):
            if DT==0: return bu8()/pow(2.0,exponent) #8bit unsigned pseudo-float
            if DT==1: return bs8()/pow(2.0,exponent) #8bit signed pseudo-float
            if DT==2: return bu16()/pow(2.0,exponent) #16bit unsigned pseudo-float
            if DT==3: return bs16()/pow(2.0,exponent) #16bit signed pseudo-float
            if DT==4: return bf32() #32bit float

        if offset==None: #Direct format
            return '' #yet to be seen (return blank vector)
        else: #indexed format
            j=Jump(offset, label=' -- Vector Data:')
            vec=[DataType(D_Type),DataType(D_Type)]+([DataType(D_Type)] if IS3D else [])
            Jump(j); return vec
                
    def transform(V,M): #transform the vector via the matrix
        return [((M[0][0]*V[0]) + (M[0][1]*V[1]) + (M[0][2]*V[2]) + M[0][3]),
                ((M[1][0]*V[0]) + (M[1][1]*V[1]) + (M[1][2]*V[2]) + M[1][3]),
                ((M[2][0]*V[0]) + (M[2][1]*V[1]) + (M[2][2]*V[2]) + M[2][3])]
    
    def Ntransform(N,M): #transform the normal via the matrix
        return [(M[0][0]*N[0]) + (M[0][1]*N[1]) + (M[0][2]*N[2]),
                (M[1][0]*N[0]) + (M[1][1]*N[1]) + (M[1][2]*N[2]),
                (M[2][0]*N[0]) + (M[2][1]*N[1]) + (M[2][2]*N[2])]

    def getWeights(WOL):
        Jump(WOL, label=' -- [ Weight_Offset ]:' )
        ML=[]
        for WO in StructArr(['bu32']): #Matrix/Weight Offset
            Jump(WO[0]+32, label=' -- [ Bone_Offset , Weight ]:')
            inflmtx = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]

            #---restructured using the src for BrawlBox:
            _weights = StructArr(['bu32','bf32'])
            if len(_weights)>1:
                for MO,W in _weights:
                    bind,invbind = matrices[bones.index(MO+32)]
                    '''
                    invbind = MtxTranspose(invbind)
                    invbind[0][3],invbind[1][3],invbind[2][3] = invbind[3][:3]
                    invbind[3][0],invbind[3][1],invbind[3][2] = [0.0,0.0,0.0]
                    '''
                    #'''
                    tempmtx = MtxMultiply(bind,invbind)
                    '''^ that's the world-transform matrix'''
                    for r in range(4):
                        for c in range(4):
                            inflmtx[r][c]+=tempmtx[r][c]*W
            
            elif len(_weights)==1:
                MO,W = _weights[0]
                bind,invbind = matrices[bones.index(MO+32)]
                for r in range(4):
                    for c in range(4):
                        inflmtx[r][c]=bind[r][c]*W
            #---
            '''
            inflmtx = MtxTranspose(invbind)
            inflmtx[0][3],inflmtx[1][3],inflmtx[2][3] = inflmtx[3][:3]
            inflmtx[3][0],inflmtx[3][1],inflmtx[3][2] = [0.0,0.0,0.0]
            '''
            #'''
            
            ML+=[ inflmtx ]
        return ML
    
    def getAttrs(AO): Jump(AO, label=' -- Attributes [CP_index,CP_Type,IsXYZ/NBT/A/ST,Data_Type,Exponent,unk,Stride/Format,Offset]');\
        return StructArr(['bu32','bu32','bu32','bu32','bu8','bu8','bu16','bu32'],[255,'*','*','*','*','*','*','*'])
        
    def CPT(T): #face-point index/value formats
        if T == 0: return '',0 #null
        if T == 1: return None,0 #direct data (handled by code)
        if T == 2: return bu8(),1 #8bit index
        if T == 3: return bu16(),2 #16bit index


    def geometry(Attributes,weights_list):
        global length;length=0
        
        def color(fmt,offset=None,alpha=1): #currently returns [R,G,B,A] int() colors only
            global length #TODO: remove to increase speed (faster if we don't redefine this function)
            if offset==None: #Direct format
                if fmt==0:length+=2;D=bu16(); return [
                    int(((D>>11)&31)*(255/31)),int(((D>>5)&63)*(255/63)),int((D&31)*(255/31)),255] #RGB565
                if fmt==1:length+=3; return [bu8(),bu8(),bu8(),255] #return [bu8(),bu8(),bu8()] #RGB8
                if fmt==2:length+=4; return [bu8(),bu8(),bu8(),bu8()] #RGBX8
                if fmt==3:length+=2; RG,BA=bu8(),bu8(); R,G,B,A=RG>>4,RG&15,BA>>4,BA&15; return [
                    (R*16)+R,(G*16)+G,(B*16)+B,(A*16)+A]#RGBA4
                if fmt==4:length+=3; D=bu24(); return [
                    (D>>18)*(255/63),((D>>12)&63)*(255/63),((D>>6)&63)*(255/63),(D&63)*(255/63)] #RGBA6
                if fmt==5:length+=4; return [bu8(),bu8(),bu8(),bu8()] #RGBA8
            else: #indexed format
                return [255,255,255,255] #yet to be seen (returning white)
                
            
        count=bu16(label=' -- Facepoint Count')
        while count>0:
            tmtx = MTX44() #transformations
            V,N,C,U='','',['',''],['','','','','','','','']
            for attr in Attributes:
                I,L=CPT(attr[1]); length += L
                def Get(IS3D): return vector(attr[3], attr[4], (attr[7]+(I*attr[6]))+32, IS3D)
                
                switch(attr[0])
                if   case( 0): tmtx = weights_list[bu8()/3];length+=1; LABEL(' -- Weight Index/value') #vert/nor_mtx
                elif case( 1): bu8()/3; length+=1 #uv[0]_mtx (value not used yet)
                elif case( 2): bu8()/3; length+=1 #uv[1]_mtx
                elif case( 3): bu8()/3; length+=1 #uv[2]_mtx
                elif case( 4): bu8()/3; length+=1 #uv[3]_mtx
                elif case( 5): bu8()/3; length+=1 #uv[4]_mtx
                elif case( 6): bu8()/3; length+=1 #uv[5]_mtx
                elif case( 7): bu8()/3; length+=1 #uv[6]_mtx
                elif case( 8): bu8()/3; length+=1 #uv[7]_mtx
                elif case( 9): LABEL(' -- Vert Index/value');   V=('' if I=='' else transform(Get(attr[2]),tmtx)) #vert
                elif case(10): LABEL(' -- Normal Index/value'); N=('' if I=='' else Ntransform(Get(1),tmtx)) #normal
                elif case(11): C[0]=('' if I=='' else color(attr[3],I,attr[2])); LABEL(' -- Color0 Index/value') #color0
                elif case(12): C[1]=('' if I=='' else color(attr[3],I,attr[2])); LABEL(' -- Color1 Index/value') #color1
                elif case(13): LABEL(' -- UV0 Index/value');    U[0]=('' if I=='' else Get(0)) #UV0
                elif case(14): LABEL(' -- UV1 Index/value');    U[1]=('' if I=='' else Get(0)) #UV1
                elif case(15): LABEL(' -- UV2 Index/value');    U[2]=('' if I=='' else Get(0)) #UV2
                elif case(16): LABEL(' -- UV3 Index/value');    U[3]=('' if I=='' else Get(0)) #UV3
                elif case(17): LABEL(' -- UV4 Index/value');    U[4]=('' if I=='' else Get(0)) #UV4
                elif case(18): LABEL(' -- UV5 Index/value');    U[5]=('' if I=='' else Get(0)) #UV5
                elif case(19): LABEL(' -- UV6 Index/value');    U[6]=('' if I=='' else Get(0)) #UV6
                elif case(20): LABEL(' -- UV7 Index/value');    U[7]=('' if I=='' else Get(0)) #UV7
                elif case(21): pass #vert_mtx_arr
                elif case(22): pass #normal_mtx_arr
                elif case(23): pass #uv_mtx_arr
                elif case(24): pass #light_mtx_array
                elif case(25): LABEL(' -- NBT Index/value');    N=('' if I=='' else Get(1))#transform(Get(1),tmtx)) #NBT (NX,NY,NZ, BX,BY,BZ, TX,TY,TZ)
                elif case(255):pass #CP_NULL

                '''NBT:
                0x000003C07C: read 0x00000019 as 25	CP_index
                0x000003C080: read 0x00000003 as 3	CP_Type
                0x000003C084: read 0x00000001 as 1	isNBT
                0x000003C088: read 0x00000004 as 4	Data_Type
                0x000003C08C: read 0x00 as 0		Exponent
                0x000003C08D: read 0x00 as 0		unk
                0x000003C08E: read 0x0024 as 36		stride
                0x000003C090: read 0x00007200 as 29184	offset
                '''

                #NOTE: currently NBT just evaluates the normal vector
                #this is because the bi-normal and tangent vectors are not supported in this development
                #this has already been fixed in the upcoming dev5 release ;)
                
            count-=1

            SetFacepoint(V,N,tuple(C),tuple(U))
            if len(tmtx): (SetWeight( N, W ) for N,M,W in tmtx)
        
        return length+3

    #-----------------------------------------------------------------------------------------------
    '''read a DAT object'''
    def _Object(offset): #pobj
        
        Jump(offset, label=' -- Object Struct')
        
        unk = bu32(     label=' -- Unknown')
        Next = bu32(    label=' -- Next Object Struct Offset')+32
        attrs = bu32(   label=' -- Facepoint Attributes Offset')+32
        flags = bu16(   label=' -- Unknown Object Flags')
        DL_size = bu16( label=' -- Display List Size')*32
        DL_data = bu32( label=' -- Display List Offset')+32
        weights = bu32( label=' -- Weight Offsets List Offset:')+32
        
        name='obj'+str_off(offset)
        SetObject( name, ParentName='joint_obj') #create a new mesh object
        
        weights_list=(getWeights(weights) if weights>32 else [])
        Attributes=getAttrs(attrs)
        
        
        Jump(DL_data);LABEL(' -- Display List:')
        while DL_size>0:
            
            Switch(bh8())
            if   Case('78'): t,n = UMC_POLYGON,      'Polygon' #possible support based on pattern (hasn't actually been seen)
            elif Case('80'): t,n = UMC_QUADS,        'Quads'
            elif Case('88'): t,n = UMC_QUADSTRIP,    'QuadStrip' #possible support based on pattern (hasn't actually been seen)
            elif Case('90'): t,n = UMC_TRIANGLES,    'Triangles'
            elif Case('98'): t,n = UMC_TRIANGLESTRIP,'TriangleStrip'
            elif Case('A0'): t,n = UMC_TRIANGLEFAN,  'TriangleFan'
            elif Case('A8'): t,n = UMC_LINES,        'Lines'
            elif Case('B0'): t,n = UMC_LINESTRIP,    'LineStrip'
            elif Case('B8'): t,n = UMC_POINTS,       'Points'
            else: t=''

            if t!='':
                LABEL(' -- Primitive Type: '+n)
                SetPrimitive(t)
                DL_size-=geometry(Attributes,weights_list)
            else: DL_size-=1

        if Next>32: _Object(Next)

    ################################################################################################
    '''read the data structure of a DAT mesh object'''
    #NOTE: the term 'Mesh' may change
    def _Mesh(offset):
        Jump(offset, label=' -- Mesh Struct')
        
        unk = bu32(     label=' -- Unknown')
        Next = bu32(    label=' -- Next Mesh Struct Offset')+32
        Material = bu32(label=' -- Material Struct Offset')+32
        Object = bu32(  label=' -- Object Struct Offset')+32

        if Next>32: _Mesh(Next)
        if Material>32: pass #Material_MAP(Material) #materials/textures aren't used by UMC yet >_>
        if Object>32: _Object(Object)

    ################################################################################################
    '''read and transform a DAT bone before storing it's data'''
    def _Bone(offset, parent='', prev='', pbm=MTX44(), pibm=MTX44()):
        
        Jump(offset, label=' -- Bone Struct')
        
        unk1 = bu32(    label=' -- Unknown')
        Flags = bu32(   label=' -- Unknown Bone Flags')
        
        Child = bu32(   label=' -- Child Bone Struct Offset')+32
        Next = bu32(    label=' -- Next Bone Struct Offset')+32
        Mesh = bu32(    label=' -- Mesh Struct Offset')+32
        
        RX = bf32(label=' -- Rotation X')
        RY = bf32(label=' -- Rotation Y')
        RZ = bf32(label=' -- Rotation Z')
        SX = bf32(label=' -- Scale X')
        SY = bf32(label=' -- Scale Y')
        SZ = bf32(label=' -- Scale Z')
        LX = bf32(label=' -- Location X')
        LY = bf32(label=' -- Location Y')
        LZ = bf32(label=' -- Location Z')
        
        inv_off = bu32( label=' -- Inverse-Bind Matrix Offset')+32
        unk2 = bu32(    label=' -- Unknown')
        
        if inv_off>32: #World Inverse-Bind
            Jump(inv_off, label=' -- Inverse-Bind Matrix')
            ibm = [ [bf32(label=' -- XX'),bf32(label=' -- XY'),bf32(label=' -- XZ'),bf32(label=' -- XW')],
                    [bf32(label=' -- YX'),bf32(label=' -- YY'),bf32(label=' -- YZ'),bf32(label=' -- YW')],
                    [bf32(label=' -- ZX'),bf32(label=' -- ZY'),bf32(label=' -- ZZ'),bf32(label=' -- ZW')],
                    [0.0,0.0,0.0,1.0]] #mtx44
            '''
            bilt = MtxTranspose(bilt)
            bilt[0][3],bilt[1][3],bilt[2][3] = bilt[3][:3]
            bilt[3][0],bilt[3][1],bilt[3][2] = [0.0,0.0,0.0]
            '''
            #'''
            
        else: #load default matrix
            ibm=pibm #MTX44()

        #tm = TransformMatrix( [LX,LY,LZ], [RX,RY,RZ], [SX,SY,SZ] )
        bm = MtxInvert(ibm) #MtxMultiply( tm, pbm )

        LX,LY,LZ = bm[0][3],bm[1][3],bm[2][3] #transform bone Loc with the matrix
            
        SetObject('joint_obj') #active object being the rig object
        pa = 'bn'+str_off(parent) if parent!='' else ''
        pr = 'bn'+str_off(prev) if prev!='' else ''
        SetBone('bn'+str_off(offset),0,[LX,LY,LZ,RX,RY,RZ,SX,SY,SZ],ibm,pa,pr)
        
        global bones; bones+=[offset]
        global matrices; matrices+=[[bm,ibm]]
        
        if Child>32: _Bone(Child,offset,'',bm,ibm)
        if Next>32: _Bone(Next,parent,offset,pbm,pibm)
        if Mesh>32: _Mesh(Mesh)
        
    ################################################################################################
    #main header:
    block_size = bu32(  label=' -- DataBlock Size')
    offset_tbl = bu32(  label=' -- Relocation Table Offset')+32
    num_offsets = bu32( label=' -- Relocation Offset Count')
    num_bases = bu32(   label=' -- Root Node Count')
    num_refs = bu32(    label=' -- Reference Node Count')
    tmp1 = bu32(        label=' -- Unknown') #001B?
    unk1 = bu32(        label=' -- Pad?')
    unk2 = bu32(        label=' -- Pad?')
    
    for i in range(num_bases): #parse the DAT data for each base node
        Jump(offset_tbl+(num_offsets*4)+(i*8), label='Root Nodes') #get to the base node
        offset = bu32(label=' -- Data Offset')+32
        last=Jump(offset_tbl+(num_offsets*4)+((num_bases+num_refs)*8)+bu32(label=' -- String Offset'), label=' -- String')
        base_name=String().split('_')#; jump(last)

        base_name_length = len(base_name)
        
        if base_name_length>2 and base_name[2] == 'joint':
            #set a rig object for bones, and child mesh objects (UMC formatting)
            SetObject('joint_obj',24) #last viewport (24)
            _Bone(offset) #begin reading the model
