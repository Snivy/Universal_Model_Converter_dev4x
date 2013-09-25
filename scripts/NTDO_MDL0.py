from data.COMMON import * #essentials
Header(  0.001, 							#Script Version (for updates)
			('Nintendo',['mdl0','brmdl']),   #model activation
			('',[]),							#anim activation
			['revolution'],				#included libs
			['NtdoImg']) 					#image handlers

''' UMC model import/export script written by Tcll5850 '''

def ImportModel(FT,Cmd):

    def MTX44(): return [[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]]

    def Offset_Name(offset):
        p=jump(offset-1,label=' -- String_Data')
        Str=string(bu8( label=' -- String_Length'))
        jump(p); return Str

    def RList(offset):

        #Nobody has helped me figure this area out,
        #brbx (the only correctly-structured/working src) is too confusing for me D:
        #Kryal hasn't returned since I asked
        #BJ isn't much help (I understand his area though.)
        #Toomai doesn't understand it that well (last I heard from him)
        #Bero disappeared <_< (he was on once lately, but not too lately as of now)
        #anyone else I talk to either has little knowledge, or doesn't care about it. >_<

        #I won't be able to build a working exporter until this area is figured out
        #at least importing can easily be loosely formatted for this... :P

        jump(offset,      label=' -- Resource_Group')
        group_len = bu32( label=' -- Resource_Group_Length')
        offset_cnt = bu32(label=' -- Resource_Offset_Count')
        skip(16,          label=' -- Resource_Offset -1 (old method)') #'FFFF 0000 000# 000# 00000000 00000000
        LABEL('\n -- Resource_Offsets [Group_ID,padding,Prev_ID,Next_ID,String_Offset,Data_Offset]:')
        return StructArr(['bs16','bu16','bu16','bu16','bu32','bu32'],offset_cnt)

    def Bounds(Type): #MinX,Y(,Z),MaxX,Y(,Z)
        LABEL('\n -- Bounds:')
        return [bf32(),bf32(),bf32(),bf32()]+([bf32(),bf32()] if Type==3 else [])

    #global header:
    magic = string(4, label=' -- MDL0_Magic')
    DataLen = bu32(   label=' -- Data_Length')
    version = bu32(   label=' -- Version')
    brres_hdr = bs32( label=' -- Brres_Header')

    #data sections
    Definits = (bu32(label=' -- Definitions')if version>7 else 0)
    Bones    = (bu32(label=' -- Bones')      if version>7 else 0)
    Vertices = (bu32(label=' -- Vertices')   if version>7 else 0)
    Normals  = (bu32(label=' -- Normals')    if version>7 else 0)
    Colors   = (bu32(label=' -- Colors')     if version>7 else 0)
    UVs      = (bu32(label=' -- UVs')        if version>7 else 0)
    Unk1     = (bu32(label=' -- Unknown1')   if version>9 else 0)
    Unk2     = (bu32(label=' -- Unknown2')   if version>9 else 0)
    Materials= (bu32(label=' -- Materials')  if version>7 else 0)
    Nodes    = (bu32(label=' -- Nodes')      if version>7 else 0)
    Objects  = (bu32(label=' -- Objects')    if version>7 else 0)
    Textures = (bu32(label=' -- Textures')   if version>7 else 0)
    Pallets  = (bu32(label=' -- Pallets')    if version>7 else 0)
    Unk3     = (bu32(label=' -- Unknown3')   if version>10 else 0)

    #local header:
    MDL0_Name = Offset_Name(bu32(label=' -- String_Offset'))
    header_len = bu32(      label=' -- Header_Length')
    MDL0_offset = bs32(     label=' -- MDL0_Header_Offset')
    header_unk1 = bu32(     label=' -- Unknown')
    header_unk2 = bu32(     label=' -- Unknown')
    num_verticies = bu32(   label=' -- Vert_Count')
    num_faces = bu32(       label=' -- Face_Count')
    header_unk3 = bu32(     label=' -- Unknown')
    Def_Count = bu32(       label=' -- Def_Count')
    unk_flags = bu32(       label=' -- Unknown_Flags')
    header_unk5 = bu16(     label=' -- Unknown')
    Data_Offset = bu16(     label=' -- Data_Offset')
    boundbox = Bounds(3)

    if bool(Unk1+Unk2+Unk3):
        LABEL('''\n\nThis MDL0 uses an unknown resource.
              please contact me at Tcll5850@gmail.com and be sure to
              send me the MDL0 so I may add support for this data.\n'''.lstrip())


    #Collect the needed data for the objects
    global _Bones
    LABEL('\n -- Links:')
    _Links = bs32(['']*bu32(label=' -- Link_Count')) #Definition Links
    _Definitions={'NodeTree':[],'NodeMix':{},'DrawOpa':[],'DrawXlu':[] }
    _Bones=[]
    _Vertices=[]
    _Normals=[]
    _Colors=[]
    _UVs=[]

    _materials=[] #later



    if bool(Definits):
        for I,pad,P,N,S,D in RList(Definits):
            DN = Offset_Name(Definits+S)
            jump(Definits+D,label=' -- Definitions')
            while True:
                switch(bu8(label=' -- Type ( '))
                if   case(1): LABEL('End_Marker )'); break
                elif case(2):
                    LABEL('Bone_Mapping )')
                    _Definitions[DN]+=[ [bu16(label=' -- Bone_ID'),_Links[bu16(label=' -- Parent_Link_Index')]] ] #[BoneID,ParentID]
                elif case(3): #weights: { ID:[[BoneID, Value], []] }:
                    LABEL('Bone_Weighting )')
                    LI=bu16(label=' -- Link_Index')
                    WL=[[_Links[bu16(label=' -- Weight_Link_Index')],bf32(label=' -- Weight_Value')] for i in range(bu8(label=' -- Weight_count'))]
                    _Definitions[DN].update({LI:WL})
                elif case(4):
                    LABEL('Material )')
                    _Definitions[DN]+=[
                        [bu16(label=' -- Material_ID'),bu16(label=' -- Object_ID'),bu16(label=' -- Bone_ID'),bu8(label=' -- Unknown')] ]
                elif case(5):
                    LABEL('Link_Indexing )')
                    LI=bu16(label=' -- Link_Index')
                    WL=[[bu16(label=' -- Bone_ID'),1.0]]
                    _Definitions[DN].update({LI:WL})
    
    
    if bool(Bones):
        def TransformMatrix( translate, rotate, scale ):
            degrad = pi/180
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

        def Loc(Mtx): return [Mtx[0][3],Mtx[1][3],Mtx[2][3]]

        def Rot(Mtx):
            degrad = pi/180
            y = asin(Mtx[1][0])
            if (pi/2) - abs(y) < 0.0001:
                z = 0.0
                if y>0: x = atan2(Mtx[0][1],Mtx[0][2])
                else: x = atan2(Mtx[0][1],-Mtx[0][2])
            else:
                c = cos(y)
                x = atan2(Mtx[1][2]/c,Mtx[2][2]/c)
                z = atan2(Mtx[0][0]/c,Mtx[0][1]/c)
                if pi - abs(z) < 0.05:
                    y = pi-y
                    c = cos(y)
                    x = atan2(Mtx[1][2]/c,Mtx[2][2]/c)
                    z = atan2(Mtx[0][0]/c,Mtx[0][1]/c)
            return [x*degrad,y*degrad,z*degrad]
                    
        
                    
        for I,pad,P,N,S,D in RList(Bones):
            jump(Bones+D,label=' -- Bones')
            
            #boneheader
            block_size = bu32(  label=' -- Data_Size')
            MDL0_header = bs32( label=' -- MDL0_Header_Offset')
            Bone_Name = Offset_Name(Bones+D+bu32(label=' -- String_Offset'))
            Bone_ID = bu32(     label=' -- Bone_ID')
            Link_Index = bu32(  label=' -- Link_Index')
            
            _UNUSED,_FLAG15,_FLAG14,_FLAG13,_FLAG12,_FLAG11,_FLAG10,_HasGeometry,_FLAG8,_FLAG7,_HasChildren,_FLAG5,_FLAG4,_FixedScale,_FixedRotation,_FixedTranslation,_NoTransform=Field(['16',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], bu32(label=' -- Bone_Flags'))
            
            skip(8) #padding
            LABEL('\n -- Loc:'); LX,LY,LZ=bf32(['','',''])
            LABEL('\n -- Rot:'); RX,RY,RZ=bf32(['','',''])
            LABEL('\n -- Sca:'); SX,SY,SZ=bf32(['','',''])
            
            #LRS=[LX,LY,LZ,RX,RY,RZ,SX,SY,SZ]
            
            _Bounds = Bounds(3)
            
            _parent = bs32(     label=' -- Parent offset (ignored)')
            _child = bs32(      label=' -- Child offset (ignored)')
            _next = bs32(       label=' -- Next offset (ignored)')
            _prev = bs32(       label=' -- Prev offset (ignored)')
            P2 = bs32(          label=' -- Part 2 offset')
            
            TransMtx=TransformMatrix( [LX,LY,LZ], [RX,RY,RZ], [SX,SY,SZ] )
            FrameMtx=MTX44()
            
            if Bone_ID>0:
                for BID,PID in _Definitions['NodeTree']:
                    if BID==Bone_ID:
                        FrameMtx=MtxMultiply(TransMtx,_Bones[PID][5])
                        break
                    
            BindMtx=Matrix(3,4,'bf32')+[[0,0,0,1]]
            InvBindMtx=Matrix(3,4,'bf32')+[[0,0,0,1]]

            LRS=[BindMtx[0][3],BindMtx[1][3],BindMtx[2][3],RX,RY,RZ,SX,SY,SZ]
            
            _Bones+=[[Bone_Name,LRS,TransMtx,BindMtx,InvBindMtx,FrameMtx]]
            
    #create the rig object and link the bones to it
    SetObject(MDL0_Name+'_Rig',24)
    for BID,PID in _Definitions['NodeTree']:
        BN,BLRS,BTMTX,BBMTX,BIMTX,BFMTX=_Bones[BID]
        PN,PLRS,PTMTX,PBMTX,PIMTX,PFMTX=_Bones[PID]
        SetBone(BN,0,BLRS,BBMTX,PN)
    
    def Vector(cnt, dmt, CT, ev):
        L = StructArr([['bu8','bs8','bu16','bs16','bf32'][CT]]*dmt,cnt)
        return [[D/pow(2.0,evaluator) for D in V] for V in L] if CT<4 else L

    if bool(Vertices):
        for I,pad,P,N,S,D in RList(Vertices):
            jump(Vertices+D,label=' -- Vertices')

            #vectorheader
            block_size = bu32(  label=' -- Data_Size')
            MDL0_header = bs32( label=' -- MDL0_Header_Offset')
            data_offset = bu32( label=' -- Data_Offset') #usu 32 or 64(if bounds)
            Mesh_Name = Offset_Name(Vertices+D+bu32(label=' -- String_Offset'))
            VertID = bu32(      label=' -- Vert_ID')
            XYZ = bu32(         label=' -- is_XYZ')
            _GXCompType = bu32( label=' -- Component_Type')
            evaluator = bu8(    label=' -- Evaluator')
            stride = bu8(       label=' -- Vert_Stride')
            vector_count = bu16(label=' -- Vert_Count')

            Bounds(2+XYZ)

            j=Jump(Vertices+D+data_offset, label=' -- Vector_Data')
            _Vertices+=[Vector(vector_count, 2+XYZ, _GXCompType, evaluator)]
            #^lousy method (ID's discarded) used until I figure out the resource group enumeration.


    if bool(Normals):
        for I,pad,P,N,S,D in RList(Normals):
            jump(Normals+D,label=' -- Normals')

            #vectorheader
            block_size = bu32(  label=' -- Data_Size')
            MDL0_header = bs32( label=' -- MDL0_Header_Offset')
            data_offset = bu32( label=' -- Data_Offset') #usu 32 or 64(if bounds)
            Mesh_Name = Offset_Name(Normals+D+bu32(label=' -- String_Offset'))
            NormID = bu32(      label=' -- Normal_ID')
            NBT = bu32(         label=' -- is_NBT')
            _GXCompType = bu32( label=' -- Component_Type')
            evaluator = bu8(    label=' -- Evaluator')
            stride = bu8(       label=' -- Normal_Stride')
            vector_count = bu16(label=' -- Normal_Count')

            j=Jump(Normals+D+data_offset, label=' -- Vector_Data')
            _Normals+=[Vector(vector_count, 3, _GXCompType, evaluator)]
            #^lousy method (ID's discarded) used until I figure out the resource group enumeration.


    if bool(UVs):
        for I,pad,P,N,S,D in RList(UVs):
            jump(UVs+D,label=' -- UVs')

            #vectorheader
            block_size = bu32(  label=' -- Data_Size')
            MDL0_header = bs32( label=' -- MDL0_Header_Offset')
            data_offset = bu32( label=' -- Data_Offset') #usu 32 or 64(if bounds)
            Mesh_Name = Offset_Name(UVs+D+bu32(label=' -- String_Offset'))
            UVID = bu32(      label=' -- UV_ID')
            ST = bu32(         label=' -- is_ST')
            _GXCompType = bu32( label=' -- Component_Type')
            evaluator = bu8(    label=' -- Evaluator')
            stride = bu8(       label=' -- UV_Stride')
            vector_count = bu16(label=' -- UV_Count')

            j=Jump(UVs+D+data_offset, label=' -- Vector_Data')
            _UVs+=[Vector(vector_count, 2, _GXCompType, evaluator)]
            #^lousy method (ID's discarded) used until I figure out the resource group enumeration.


    def color(cnt, fmt):
        RGB565,RGB8,RGBX8,RGBA4,RGBA6,RGBA8 = range(6)
        data=StructArr([                #_GXCompType (Colors):
            'bu16',                     #RGB565= 0,
            ['bu8','bu8','bu8'],        #RGB8  = 1,
            ['bu8','bu8','bu8','bu8'],  #RGBX8 = 2, #X is disreguarded
            ['bu8','bu8'],              #RGBA4 = 3,
            'bu24',                     #RGBA6 = 4,
            ['bu8','bu8','bu8','bu8']   #RGBA8 = 5
            ][fmt],cnt)

        switch(fmt)
        if   case(RGB565): return [[int(((D>>11)&31)*(255/31.)),int(((D>>5)&63)*(255/63.)),int((D&31)*(255/31.))] for D in data] #[R,G,B]
        elif case(RGB8): return data #[R,G,B]
        elif case(RGBX8): return [D[0:3] for D in data] #[R,G,B]
        elif case(RGBA4): return [[(RG>>4*16)+RG>>4,(RG&15*16)+RG&15,(BA>>4*16)+BA>>4,(BA&15*16)+BA&15] for RG,BA in data] #[R,G,B,A]
        elif case(RGBA6): return [(D>>18)*(255/63),((D>>12)&63)*(255/63),((D>>6)&63)*(255/63),(D&63)*(255/63)] #[R,G,B,A]
        elif case(RGBA8): return data #[R,G,B,A]


    if bool(Colors):
        for I,pad,P,N,S,D in RList(Colors):
            jump(Colors+D,label=' -- Colors')

            #vectorheader
            block_size = bu32(  label=' -- Data_Size')
            MDL0_header = bs32( label=' -- MDL0_Header_Offset')
            data_offset = bu32( label=' -- Data_Offset')
            Mesh_Name = Offset_Name(Colors+D+bu32(label=' -- String_Offset'))
            ColID = bu32(       label=' -- Color_ID')
            RGBA = bu32(        label=' -- is_RGBA')
            _GXCompType = bu32( label=' -- Component_Type')
            stride = bu8(       label=' -- Color_Stride')
            scale = bu8(        label=' -- Scale')
            color_count = bu16( label=' -- Color_Count')


            j=Jump(Colors+D+data_offset, label=' -- Color_Data')
            _Colors+=[color(color_count, _GXCompType)]
            #^lousy method (ID's discarded) used until I figure out the resource group enumeration.
    
    
    #Process everything when we get here
    if bool(Objects):
        def getCPList(lo,hi): # CP register (old code (currently faster than using Field())
            return [
            (lo & 1), ((lo >> 1) & 1), ((lo >> 2) & 1), ((lo >> 3) & 1), ((lo >> 4) & 1),
            ((lo >> 5) & 1), ((lo >> 6) & 1), ((lo >> 7) & 1), ((lo >> 8) & 1),
            ((lo >> 9) & 3), ((lo >> 11) & 3), ((lo >> 13) & 3), ((lo >> 15) & 3),
            (hi & 3), ((hi >> 2) & 3), ((hi >> 4) & 3), ((hi >> 6) & 3),
            ((hi >> 8) & 3), ((hi >> 10) & 3), ((hi >> 12) & 3), ((hi >> 14) & 3),
            ((hi >> 16) & 3), ((hi >> 18) & 3), ((hi >> 20) & 3), ((hi >> 22) & 3),
            ((hi >> 24) & 3), ((hi >> 26) & 3), ((hi >> 28) & 3)]

        def CPT(V): #face-point index/value formats
            switch(V)
            if case(0): return '',0  #Null
            if case(1): return None,0 #Direct Data
            if case(2): return bu8(),1 #8bit index
            if case(3): return bu16(),2 #16bit index
            
        def MTXMultVec(V,M):
            return [(M[0][0]*V[0]) + (M[0][1]*V[1]) + (M[0][2]*V[2]) + M[0][3],
                    (M[1][0]*V[0]) + (M[1][1]*V[1]) + (M[1][2]*V[2]) + M[1][3],
                    (M[2][0]*V[0]) + (M[2][1]*V[1]) + (M[2][2]*V[2]) + M[2][3]]
        
        def Transform(vert,mtcs):
            global _Bones
            inflmtx = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
            Wghts=[]

            #---restructured using the src for BrawlBox:
            if len(mtcs)>1:
                for BID,W in mtcs:
                    BN,BLRS,BTMTX,BBMTX,BIMTX,BFMTX=_Bones[BID]
                    tempmtx = MtxMultiply(BBMTX,BIMTX)
                    for r in range(4):
                        for c in range(4):
                            inflmtx[r][c]+=tempmtx[r][c]*W
                    Wghts+=[[BN,W]]
            
            elif len(mtcs)==1:
                BID,W = mtcs[0] #W is always 1.0 (statically defaulted)
                BN,BLRS,BTMTX,BBMTX,BIMTX,BFMTX=_Bones[BID]
                inflmtx=BBMTX
                Wghts+=[[BN,W]]
                
            return MTXMultVec(vert,inflmtx),Wghts #return weights for UMC's functions
            
        def _Rotate(V,M):
            return [(M[0][0]*V[0]) + (M[0][1]*V[1]) + (M[0][2]*V[2]),
                    (M[1][0]*V[0]) + (M[1][1]*V[1]) + (M[1][2]*V[2]),
                    (M[2][0]*V[0]) + (M[2][1]*V[1]) + (M[2][2]*V[2])]
        
        def NTransform(normal,mtcs):
            global _Bones
            inflmtx = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
            Wghts=[]
            
            if len(mtcs)>1:
                for BID,W in mtcs:
                    BN,BLRS,BTMTX,BBMTX,BIMTX,BFMTX=_Bones[BID]
                    tempmtx = MtxMultiply(BBMTX,BIMTX)
                    for r in range(3):
                        for c in range(3):
                            inflmtx[r][c]+=tempmtx[r][c]*W
            
            elif len(mtcs)==1:
                BID,W = mtcs[0] #W is always 1.0 (statically defaulted)
                BN,BLRS,BTMTX,BBMTX,BIMTX,BFMTX=_Bones[BID]
                inflmtx=[BBMTX[0][:3],BBMTX[1][:3],BBMTX[2][:3]]
                
            return _Rotate(normal,inflmtx)

        XF_VtxMtxCache=[None]*16
        XF_NrmMtxCache=[None]*16
        
        for I,pad,P,N,S,D in RList(Objects):
            jump(Objects+D,label=' -- Object')
            
            Block_Size=bu32(    label=' -- Data_Size')
            MDL0_header=bs32(   label=' -- MDL0_Header_Offset')
            Link=bs32(          label=' -- Link_ID/Def_Table')
            CPL=getCPList( bu32(label=' -- CP_Lo'), bu32(label=' -- CP_Hi') ) #TODO: use attribute definitions
            INVTXSPEC=bu32(     label=' -- XF_Specs')
            Attribute_size=bu32(    label=' -- Attribute_Size')
            Attribute_flags=bu32(   label=' -- Attribute_Flags') #0x00000080 or 0x000000A0
            #^I honestly don't think these have anything to do with the arrributes
            Attributes_offset=bu32( label=' -- Attributes_Offset')+34+Objects+D
            Buffer_Size=bu32(   label=' -- Data_Buffer_Size')
            Data_Size=bu32(     label=' -- Data_Size')
            Primitives_Offset=bu32(label=' -- Data_Offset')+36+Objects+D
            Elm_Flags=bu32(     label=' -- Element_Flags') #unused (CPL does this automatically) :P
            unk3=bu32(          label=' -- Unknown') #usually 0
            Object_Name=Offset_Name(Objects+D+bu32(label=' -- String_Offset'))
            ID=bu32(            label=' -- Object_ID')
            num_verts=bu32(     label=' -- Vert_Count')
            num_faces=bu32(     label=' -- Face_Count')

            LABEL('\n -- Vert_Input:');     vertex_input=bs16()
            LABEL('\n -- Normal_Input:');   normal_input=bs16()
            LABEL('\n -- Color_Inputs:');   color_inputs=[bs16(),bs16()]
            LABEL('\n -- UV_Inputs:');      UV_inputs=[bs16(),bs16(),bs16(),bs16(),bs16(),bs16(),bs16(),bs16()]
            unknown_inputs=[]
            if version>9:
                LABEL('\n -- Unknown_Inputs:'); unknown_inputs=StructArr('bs16',2)

            Def_Tbl=bu32(       label=' -- Definition_Table_Offset')+Objects+D
            if Link==-1: #use def table
                jump(Def_Tbl,   label=' -- Definition_Table')
                Defs=StructArr('bu16',bu32(label=' -- Definition_Count'))
                
            # ^ I'll be working on this area later...
            #  tbh though, it isn't really needed >_>


            #jump(Attributes_offset,) #soon :/

            SetObject(Object_Name, ParentName=(MDL0_Name+'_Rig' if bool(len(_Definitions['NodeTree'])) else ''))

            Jump(Primitives_Offset,label=' -- Primitives:')
            pos = 0
            while pos<Buffer_Size:
                Switch(bh8()) #primitive ID
                pos+=1
                t=''
                #0x0002 B 024
                if   Case('20'): #vert matrix
                    LABEL(' -- Primitive Type ( XF_Vert_Matrix )')
                    Link,Len,XFAddr = Field(['16','4','12'],bu32()); pos+=4
                    XF_VtxMtxCache[XFAddr/12]=_Definitions['NodeMix'][Link] #[ [BoneID, Weight], [] ]
                    #  use the bone ID to get the bone's name and bind matrix.
                    
                elif Case('28'): #normal matrix (3x3)
                    LABEL(' -- Primitive Type ( XF_Normal_Matrix )')
                    Link,Len,XFAddr = Field(['16','4','12'],bu32()); pos+=4
                    ##XF_NrmMtxCache[XFAddr/12]=_Definitions['NodeMix'][Link] #[ [BoneID, Weight], [] ]
                    #if( ( readNum( f, 2, 2, true ) - 0xb000 ) / 0x0c > 7 )
                    
                elif Case('30'): #UV matrix
                    LABEL(' -- Primitive Type ( XF_UV_Matrix )')
                    Val,Len,Adr=Field(['16','4','12'],bu32()); pos+=4
                elif Case('38'): #light matrix
                    LABEL(' -- Primitive Type ( XF_Light_Matrix )')
                    Val,Len,Adr=Field(['16','4','12'],bu32()); pos+=4

                elif Case('78'): t,n = UMC_POLYGON,      'Polygon' #possible support based on pattern (hasn't actually been seen)
                elif Case('80'): t,n = UMC_QUADS,        'Quads'
                elif Case('88'): t,n = UMC_QUADSTRIP,    'QuadStrip' #possible support based on pattern (hasn't actually been seen)
                elif Case('90'): t,n = UMC_TRIANGLES,    'Triangles'
                elif Case('98'): t,n = UMC_TRIANGLESTRIP,'TriangleStrip'
                elif Case('A0'): t,n = UMC_TRIANGLEFAN,  'TriangleFan'
                elif Case('A8'): t,n = UMC_LINES,        'Lines'
                elif Case('B0'): t,n = UMC_LINESTRIP,    'LineStrip'
                elif Case('B8'): t,n = UMC_POINTS,       'Points'

                if t!='':
                    LABEL(' -- Primitive Type ( '+n+' )')
                    SetPrimitive(t)
                    pos+=2
                    vmtcs=[] if Link==-1 else [[_Links[Link],1.0]]
                    nmtcs=[] if Link==-1 else [[_Links[Link],1.0]]
                    for v in range(bu16(label=' -- Facepoint_Count')):
                        V,N,C,U = '','',['',''],['']
                        Weights=[]
                        for I,CPV in enumerate(CPL):
                            D,L=CPT(CPV); pos+=L

                            #not sure if anything other than matrix indecies can be direct data
                            #(there doesn't seem to be a defined relation to specific formatting values) >_>
                            switch(I)
                            if   case( 0): #vert/nor_mtx
                                if CPV==1: 
                                    i=bu8(label=' -- Vert/Normal_Mtx value')/3; pos+=1
                                    vmtcs=XF_VtxMtxCache[i]; nmtcs=XF_NrmMtxCache[i]
                            elif case( 1): #uv[0]_mtx (unknown processing)
                                if CPV==1: bu8(label=' -- UV[0]_Mtx value')/3; pos+=1
                            elif case( 2): #uv[1]_mtx
                                if CPV==1: bu8(label=' -- UV[1]_Mtx value')/3; pos+=1
                            elif case( 3): #uv[2]_mtx
                                if CPV==1: bu8(label=' -- UV[2]_Mtx value')/3; pos+=1
                            elif case( 4): #uv[3]_mtx
                                if CPV==1: bu8(label=' -- UV[3]_Mtx value')/3; pos+=1
                            elif case( 5): #uv[4]_mtx
                                if CPV==1: bu8(label=' -- UV[4]_Mtx value')/3; pos+=1
                            elif case( 6): #uv[5]_mtx
                                if CPV==1: bu8(label=' -- UV[5]_Mtx value')/3; pos+=1
                            elif case( 7): #uv[6]_mtx
                                if CPV==1: bu8(label=' -- UV[6]_Mtx value')/3; pos+=1
                            elif case( 8): #uv[7]_mtx
                                if CPV==1: bu8(label=' -- UV[7]_Mtx value')/3; pos+=1

                            #I'm aware of 'dmt', 'CT', and 'ev' not being defined for direct data: ( where do I define them?? )
                            #I've only coded the basis for direct data support just in case it can be made avaliable.
                            elif case( 9): #vert
                                if CPV==1: V=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- Vert value')
                                elif CPV>1: LABEL(' -- Vert Index');   V,Weights=Transform(_Vertices[vertex_input][D],vmtcs)
                                
                            elif case(10): #normal
                                if CPV==1: V=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- Normal value')
                                elif CPV>1: LABEL(' -- Normal Index'); N=NTransform(_Normals[normal_input][D],vmtcs) ##NTransform(_Normals[normal_input][D],nmtcs)

                            elif case(11): #color[0]
                                if CPV==1: C[0]=('' if I=='' else color(1,CT)[0]); LABEL(' -- Color[0] value')
                                elif CPV>1: LABEL(' -- Color[0] Index'); C[0]=_Colors[color_inputs[0]][D]
                            elif case(12): #color[1]
                                if CPV==1: C[1]=('' if I=='' else color(1,CT)[0]); LABEL(' -- Color[1] value')
                                elif CPV>1: LABEL(' -- Color[1] Index'); C[1]=_Colors[color_inputs[1]][D]

                            elif case(13): #uv[0]
                                if CPV==1: U[0]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[0] value')
                                elif CPV>1: LABEL(' -- UV[0] Index');   U[0]=_UVs[UV_inputs[0]][D]
                            elif case(14): #uv[1]
                                if CPV==1: U[1]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[1] value')
                                elif CPV>1: LABEL(' -- UV[1] Index');   U[1]=_UVs[UV_inputs[1]][D]
                            elif case(15): #uv[2]
                                if CPV==1: U[2]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[2] value')
                                elif CPV>1: LABEL(' -- UV[2] Index');   U[2]=_UVs[UV_inputs[2]][D]
                            elif case(16): #uv[3]
                                if CPV==1: U[3]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[3] value')
                                elif CPV>1: LABEL(' -- UV[3] Index');   U[3]=_UVs[UV_inputs[3]][D]
                            elif case(17): #uv[4]
                                if CPV==1: U[4]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[4] value')
                                elif CPV>1: LABEL(' -- UV[4] Index');   U[4]=_UVs[UV_inputs[4]][D]
                            elif case(18): #uv[5]
                                if CPV==1: U[5]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[5] value')
                                elif CPV>1: LABEL(' -- UV[5] Index');   U[5]=_UVs[UV_inputs[5]][D]
                            elif case(19): #uv[6]
                                if CPV==1: U[6]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[6] value')
                                elif CPV>1: LABEL(' -- UV[6] Index');   U[6]=_UVs[UV_inputs[6]][D]
                            elif case(20): #uv[7]
                                if CPV==1: U[7]=('' if I=='' else Vector(1, dmt, CT, ev)[0]); LABEL(' -- UV[7] value')
                                elif CPV>1: LABEL(' -- UV[7] Index');   U[7]=_UVs[UV_inputs[7]][D]

                            elif case(21): pass #vert_mtx_arr
                            elif case(22): pass #normal_mtx_arr
                            elif case(23): pass #uv_mtx_arr
                            elif case(24): pass #light_mtx_array
                            elif case(25): pass #NBT (NX,NY,NZ, BX,BY,BZ, TX,TY,TZ)
                            #elif case(255):pass #CP_NULL

                            #debugging:
                            #if D!='': LABEL(' - '+str(pos)+' > '+str(Buffer_Size)+' ?')

                        SetFacepoint( V,N,tuple(C),tuple(U) )
                        if len(Weights): (SetWeight( N, W ) for N,W in Weights)


def XExportModel(FT): #WIP (not functional yet)

    #to build resource groups:
    #    1: sort names alphabetically
    #    2: insert empty string
    #    3: add names to the table

    #group names by length
    #compair names in binary tree fashon
    #chars are in R>L order, bits in L>R

    def CompareBits(b1, b2=0):
            i=8
            while i>0:
                i-=1
                if (b1 & 1<<(i-1)) != (b2 & 1<<(i-1)): return i-1 #(not sure)
            return 0

    #def GenerateID(name="") #Generate the MDL0 Group ID
    #    return -1 if name=="" else ((len(name) - 1) << 3) | CompareBits(ord(name[len(name)-1]))

    _name, _id, _index, _left, _right = "",0,0,[],[]

    def IsRight(Cname):
        global _name, _id
        return False if len(_name) != len(Cname) else ((ord(Cname[(_id >> 3)]) >> (_id & 7)) & 1) != 0

    def GenerateId(Cname, Cid, Cindex, Cleft, Cright):
        global _name, _id, _left, _right

        for i in range(len(_name)):

            if (_name[i] != Cname[i]):
                _id = (i << 3) | CompareBits(ord(_name[i]), ord(Cname[i]))

                if IsRight(comparison): _left,_right = this,comparison
                else: _left,_right = comparison,this

                return _id

        return 0
