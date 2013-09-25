#Plugin Header:
from data.COMMON import * #essentials
Header( 0.001,                      #Script Version (for updates)
       ('Wavefront',['obj','mod']), #model activation
       ('',[]),                     #anim activation
       [''])                        #included libs
#specified Libraries will be included with COMMON

def ImportModelUI(): #still in development
    CheckBox('Calculate Normals')
    Text('included UV channels:')
    File('UV1')
    File('UV2')
    File('UV3')
    File('UV4')
    File('UV5')
    File('UV6')
    File('UV7')

def ImportModel(T,C):
    Verts,Normals,UVs,Object = [],[],[],'Default_Object'
    lines = string([])
    for line in lines: #collect mesh data first
        line=line.split(' ')
        if line[0]=='v': Verts+=[[float(line[1]),float(line[2])]+([float(line[3])] if len(line)==4 else [])]
        if line[0]=='vn': Normals+=[[float(line[1]),float(line[2])]+([float(line[3])] if len(line)==4 else [])]
        if line[0]=='vt': UVs+=[[float(line[1])]+([float(line[2])] if len(line)==3 else [])]
    for line in lines: #then build (safer)
        line=line.split(' ')
        if line[0]=='o': Object=str(line[-1])
        if line[0]=='f':
            SetObject(Object)

            #I really need a function to do this.
            LP,CP = None,UMC_TRIANGLES #Last/Current Primitive
            if   len(line)==2: CP = UMC_POINTS
            elif len(line)==3: CP = UMC_LINES
            elif len(line)==4: CP = UMC_TRIANGLES
            elif len(line)==5: CP = UMC_QUADS
            elif len(line)>=6: CP = UMC_POLYGON
            if LP!=CP: SetPrimitive(CP)
            LP=CP #update the last primitive to check with the next
            
            for FP in line[1:]:
                FP=FP.split('/') #[v] or [v,u,n]
                if FP!=['\r']:
                    #I'll never understand why this happens 0.o (with any Q3D OBJ export)
                    #['###','###','###']
                    #['\r'] <- at every face end
                    #then we also get an indexing error (not sure if every OBJ does this)
                    SetFacepoint(Verts[int(FP[0])-1],
                             (Normals[int(FP[2])-1] if len(FP)==3 else ''),
                             (UVs[int(FP[1])-1] if len(FP)==3 and FP[1]!='' else ''))
                

def ExportModel(T,C):
    #TODO: still getting ideas for this:
    #NewFile('*.mtl') #add an mtl to the file library
    #SwitchFile() #switch back to the obj

    def OBJFP(FP):
        global vcnt,ncnt,ucnt#v-----working only with channel 0 atm. (1-7 will come)
        v,vt,vn = FP[0],FP[3][0],FP[1]
        return str(v+vcnt)+('/'+str(vt+ucnt)+('/'+str(vn+ncnt) if vn!='' else '') if vt!='' else ('//'+str(vn+ncnt) if vn!='' else ''))

    global vcnt,ncnt,ucnt
    vcnt,ncnt,ucnt=1,1,1 #index starts at 1
    String('#OBJ created with Universal Model Converter.\n')
    for OID in GetMeshObjects():
        Verts=GetVerts(OID)
        for Vert in Verts: String('v '+str(Vert[0])+' '+str(Vert[1])+(' '+str(Vert[2]) if len(Vert)==3 else ' 0.0')+'\n')
        String('\n')
        Normals=GetNormals(OID)
        for Normal in Normals: String('vn '+str(Normal[0])+' '+str(Normal[1])+(' '+str(Normal[2]) if len(Normal)==3 else ' 0.0')+'\n')
        String('\n')
        UVs=GetUVs(OID,0)
        for UV in UVs: String('vt '+str(UV[0])+' '+(str(UV[1]) if len(UV)==2 else ' 0.0')+'\n')
        String('\n')

        String('o '+GetObjectName(OID)+'\n')
        for Type,Facepoints in GetPrimitives(OID):
            #TODO: what if '' is returned from OBJFP?

            #TODO: we don't [i]really[/i] need the switch
            #(it can be done with a single additive code-block)
            i=0
            Switch(Type)
            if Case(UMC_POINTS):
                while i<len(Facepoints):
                    FP0=OBJFP(Facepoints[i])
                    String('f '+FP0+'\n'); i+=1
            if Case(UMC_LINES):
                while i<len(Facepoints)-1:
                    FP0,FP1=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1])
                    String('f '+FP0+' '+FP1+'\n'); i+=2
            if Case(UMC_LINESTRIP):
                while i<len(Facepoints)-1:
                    FP0,FP1=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1])
                    String('f '+FP0+' '+FP1+'\n' if FP0!=FP1 else ''); i+=1
            if Case(UMC_LINELOOP):
                while i<len(Facepoints)-1:
                    FP0,FP1=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1])
                    String('f '+FP0+' '+FP1+'\n' if FP0!=FP1 else ''); i+=1
            if Case(UMC_TRIANGLES):
                while i<len(Facepoints)-2:
                    FP0,FP1,FP2=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1]),OBJFP(Facepoints[i+2])
                    String('f '+FP0+' '+FP1+' '+FP2+'\n'); i+=3
            if Case(UMC_TRIANGLESTRIP):
                while i<len(Facepoints)-2:
                    FP0,FP1,FP2=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1]),OBJFP(Facepoints[i+2])
                    String('f '+(FP2 if(i%2)else FP0)+' '+FP1+' '+(FP0 if(i%2)else FP2)+'\n' if (FP0!=FP1!=FP2!=FP0) else ''); i+=1
            if Case(UMC_TRIANGLEFAN):
                while i<len(Facepoints)-2:
                    FP0,FP1,FP2=OBJFP(Facepoints[0]),OBJFP(Facepoints[i+1]),OBJFP(Facepoints[i+2])
                    String('f '+(FP2 if(i%2)else FP0)+' '+FP1+' '+(FP0 if(i%2)else FP2)+'\n' if (FP0!=FP1!=FP2!=FP0) else ''); i+=1
            if Case(UMC_QUADS):
                while i<len(Facepoints)-3:
                    FP0,FP1,FP2,FP3=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1]),OBJFP(Facepoints[i+2]),OBJFP(Facepoints[i+3])
                    String('f '+FP0+' '+FP1+' '+FP2+' '+FP3+'\n'); i+=4
            if Case(UMC_QUADSTRIP):
                while i<len(Facepoints)-3:
                    FP0,FP1,FP2,FP3=OBJFP(Facepoints[i]),OBJFP(Facepoints[i+1]),OBJFP(Facepoints[i+2]),OBJFP(Facepoints[i+3])
                    String('f '+FP0+' '+FP1+' '+FP2+' '+FP3+'\n' if (FP0!=FP1!=FP2!=FP3!=FP0!=FP2!=FP1!=FP3) else ''); i+=2
            if Case(UMC_POLYGON):
                pass #TODO... (not widely used)


        String('\n')
        vcnt+=len(Verts)
        ncnt+=len(Normals)
        ucnt+=len(UVs)


