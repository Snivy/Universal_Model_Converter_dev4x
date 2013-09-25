#built by Tcll5850
#inspired by Roo525

from data.COMMON import * #essentials
Header( 0.001,                   #Script Version (for updates)
       ('MikuMikuDance',['pmd']),#model activation
       ('MikuMikuDance',['vmd']),#anim activation
       [''])                     #included libs

def ImportModel(T,C):

    def Vector(): return [f32(label=' -- X'),f32(label=' -- Y'),f32(label=' -- Z')]
    
    #--header--
    signature = string(3, label=' -- Signature') #'Pmd'
    if signature=='Pmd': #is the file valid?
        #continue if so
        version = f32(label=' -- Version')

        name = string(20,code='cp932',label=' -- Model Name').split('\x00')[0]
        comment = string(256,code='cp932',label=' -- Comment').split('\x00')[0]
        
        V,N,U,u=[],[],[],[]
        for I in range(u32(label=' -- Vertex count')):
            V+=[[f32(label=' -- Vert_X'),
                 f32(label=' -- Vert_Y'),
                 f32(label=' -- Vert_Z')]]
                
            N+=[[f32(label=' -- Normal_X'),
                 f32(label=' -- Normal_Y'),
                 f32(label=' -- Normal_Z')]]
                
            U+=[[f32(label=' -- UV_S'),
                 f32(label=' -- UV_T')]]
                
            u+=[[u16(label=' -- Unknown'),
                 u16(label=' -- Unknown')],
                
                [u8(label=' -- Unknown'),
                 u8(label=' -- Unknown')]]

        SetObject()

        #I had a problem with the other method not setting the vector data >_>
        SetVerts( V )
        SetNormals( N )
        
        SetPrimitive(UMC_TRIANGLES)
        for tri in StructArr(['u16','u16','u16'],
                      u32(label=' -- Triangle Count\n -- Triangle Data: [V1,V2,V3]')/3):
            SetFacepoint(tri[0],tri[0])
            SetFacepoint(tri[1],tri[1])
            SetFacepoint(tri[2],tri[2])
        
    else: print 'Invalid PMD file'
