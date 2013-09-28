#1
#v 0.001

import sys; #sys.path.append('data')
import COMMON

#TODO: remove:
from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL import GL as __GL, GLU as __GLU
import Python.ArcBall as __AB, pygame as __pyg
from pygame.locals import * #TODO: localize
from tkFileDialog import askopenfilename,asksaveasfilename

from LOGGING import LOG as __LOG, WRITE_LOG as __WLOG #will be moved to GUI
import GUI as __GUI

global Libs; Libs=[ [], # Reserved
                    [], # Reserved
                    [["UMC_Def_Scene",[]]], # Scenes
                    [], # Objects
                    [], # Materials
                    [], # Material Add-ins
                    [], # Textures
                    []] # Images

#toggles
TOGGLE_FULLSCREEN=0
TOGGLE_ORTHO=1
TOGGLE_LIGHTING=1
TOGGLE_3D=0
TOGGLE_3D_MODE=[0,0]
TOGGLE_WIREFRAME=0
TOGGLE_BONES=1
TOGGLE_GRID=2
TOGGLE_NORMALS=0
#TOGGLE_REDRAW=False

#display list definition variables:
global __TOP_GRID,__SIDE_GRID,__FRONT_GRID,\
    __QUAD_FLOOR,__LINE_FLOOR,\
    __MODEL_DATA,__NORMAL_DATA,__BONE_DATA
#the bone data is seperate so it can be drawn over the model data (X-ray), or within the model data
#(specified by clearing the depth buffer before drawing the bones)

#local usage:
width,height = 800,600
W,H = 800,600; 
__abt=__AB.ArcBallT(width,height)

#copied from COMMON cause this doesn't exist in COMMON 9_9
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


#Tcll5850: HOORAY! My very first working class in UMC. =D
#this class deals with the matrix applied to the model-view transformation
class __viewMatrixclass():
    def __init__(self):
        #[SX, RZ,-RY, 0
        #-RZ, SY, RX, 0
        # RY,-RX, SZ, 0
        # TX, TY, TZ, 1]
        import Python.ArcBall as __AB #TODO: use global import
        self.__ID33=__AB.Matrix3fT
        self.__ID44=__AB.Matrix4fT

        self.reset()

    def reset(self): #called by key 9
        self.X,self.Y,self.Z=0.0,0.0,0.0
        self.RotMtx=self.__ID33()
        self._scale=0.1
        self.rotate(10.0,350.0,0.0)

    #keeping this here for reference (when needed),
    #since this works flawlessly for matrix (not view) transformation
    '''
    def translate(self,x,y,z):  #matrix translation
        self.Matrix[3][0]+=(self.Matrix[0][0]*x)+(self.Matrix[1][0]*y)+(self.Matrix[2][0]*z)
        self.Matrix[3][1]+=(self.Matrix[0][1]*x)+(self.Matrix[1][1]*y)+(self.Matrix[2][1]*z)
        self.Matrix[3][2]+=(self.Matrix[0][2]*x)+(self.Matrix[1][2]*y)+(self.Matrix[2][2]*z)
        self.Matrix[3][3]+=(self.Matrix[0][3]*x)+(self.Matrix[1][3]*y)+(self.Matrix[2][3]*z)

    #matrix rotation:
    def __RotX(self,x): #rotate along X axis
        from math import sin, cos, pi
        cosx,sinx=cos(x/180.0*pi),sin(x/180.0*pi)
        var1,var2=self.RotMtx[1][0],self.RotMtx[2][0]
        self.RotMtx[1][0]=(var1*cosx) +(var2*sinx)
        self.RotMtx[2][0]=(var1*-sinx)+(var2*cosx)
        var1,var2=self.RotMtx[1][1],self.RotMtx[2][1]
        self.RotMtx[1][1]=(var1*cosx) +(var2*sinx)
        self.RotMtx[2][1]=(var1*-sinx)+(var2*cosx)
        var1,var2=self.RotMtx[1][2],self.RotMtx[2][2]
        self.RotMtx[1][2]=(var1*cosx) +(var2*sinx)
        self.RotMtx[2][2]=(var1*-sinx)+(var2*cosx)
    def __RotY(self,y): #rotate along Y axis
        from math import sin, cos, pi
        cosy,siny=cos(y/180.0*pi),sin(y/180.0*pi)
        var1,var2=self.RotMtx[0][0],self.RotMtx[2][0]
        self.RotMtx[0][0]=(var1*cosy)+(var2*-siny)
        self.RotMtx[2][0]=(var1*siny)+(var2*cosy)
        var1,var2=self.RotMtx[0][1],self.RotMtx[2][1]
        self.RotMtx[0][1]=(var1*cosy)+(var2*-siny)
        self.RotMtx[2][1]=(var1*siny)+(var2*cosy)
        var1,var2=self.RotMtx[0][2],self.RotMtx[2][2]
        self.RotMtx[0][2] =(var1*cosy)+(var2*-siny)
        self.RotMtx[2][2]=(var1*siny)+(var2*cosy)
    def __RotZ(self,z): #rotate along Z axis
        from math import sin, cos, pi
        cosz,sinz=cos(z/180.0*pi),sin(z/180.0*pi)
        var1,var2=self.RotMtx[0][0],self.RotMtx[1][0]
        self.RotMtx[0][0]=(var1*cosz) +(var2*sinz)
        self.RotMtx[1][0]=(var1*-sinz)+(var2*cosz)
        var1,var2=self.RotMtx[0][1],self.RotMtx[1][1]
        self.RotMtx[0][1]=(var1*cosz) +(var2*sinz)
        self.RotMtx[1][1]=(var1*-sinz)+(var2*cosz)
        var1,var2=self.RotMtx[0][2],self.RotMtx[1][2]
        self.RotMtx[0][2]=(var1*cosz) +(var2*sinz)
        self.RotMtx[1][2]=(var1*-sinz)+(var2*cosz)
    '''

    def _getMtx(self):
        mtx=self.__ID44()
        #apply rotation
        mtx[0][0]=self.RotMtx[0][0]
        mtx[0][1]=self.RotMtx[0][1]
        mtx[0][2]=self.RotMtx[0][2]
        mtx[1][0]=self.RotMtx[1][0]
        mtx[1][1]=self.RotMtx[1][1]
        mtx[1][2]=self.RotMtx[1][2]
        mtx[2][0]=self.RotMtx[2][0]
        mtx[2][1]=self.RotMtx[2][1]
        mtx[2][2]=self.RotMtx[2][2]

        #apply rotation to translation and apply translation
        #import COMMON #Tcll5850: yes I'm using UMC scripting functions... bite me
        ir=MtxInvert(mtx) #inverse rotation
        mtx[3][0]=(ir[0][0]*self.X)+(ir[0][1]*self.Y)+(ir[0][2]*self.Z)
        mtx[3][1]=(ir[1][0]*self.X)+(ir[1][1]*self.Y)+(ir[1][2]*self.Z)
        mtx[3][2]=(ir[2][0]*self.X)+(ir[2][1]*self.Y)+(ir[2][2]*self.Z)

        #apply scale and return the result
        mtx[0][0] *= self._scale; mtx[1][0] *= self._scale; mtx[2][0] *= self._scale
        mtx[0][1] *= self._scale; mtx[1][1] *= self._scale; mtx[2][1] *= self._scale
        mtx[0][2] *= self._scale; mtx[1][2] *= self._scale; mtx[2][2] *= self._scale
        mtx[0][3] *= self._scale; mtx[1][3] *= self._scale; mtx[2][3] *= self._scale
        mtx[3][0] *= self._scale; mtx[3][1] *= self._scale; mtx[3][2] *= self._scale
        return mtx

    def translate(self,x,y,z):  #modify the matrix translation (from view)
        X=(self.RotMtx[0][0]*x)+(self.RotMtx[0][1]*y)+(self.RotMtx[0][2]*z)
        Y=(self.RotMtx[1][0]*x)+(self.RotMtx[1][1]*y)+(self.RotMtx[1][2]*z)
        Z=(self.RotMtx[2][0]*x)+(self.RotMtx[2][1]*y)+(self.RotMtx[2][2]*z)

        X/=self._scale; Y/=self._scale; Z/=self._scale
        self.X+=X; self.Y+=Y; self.Z+=Z

    def rotate(self,x=0.0,y=0.0,z=0.0): #modify the matrix rotation (from view)
        from math import sin,cos,radians
        import Python.ArcBall as __AB
        cosx = cos(radians(x)); sinx = sin(radians(x))
        cosy = cos(radians(y)); siny = sin(radians(y))
        cosz = cos(radians(z)); sinz = sin(radians(z))

        m = self.__ID33()
        m[0][0] = cosy * cosz
        m[0][1] = sinz * cosy
        m[0][2] = -siny
        m[1][0] = (sinx * cosz * siny - cosx * sinz)
        m[1][1] = (sinx * sinz * siny + cosz * cosx)
        m[1][2] = sinx * cosy;
        m[2][0] = (sinx * sinz + cosx * cosz * siny)
        m[2][1] = (cosx * sinz * siny - sinx * cosz)
        m[2][2] = cosx * cosy

        self.RotMtx = __AB.Matrix3fMulMatrix3f(self.RotMtx,m)

    def mtxrotate(self,mtx33): #modify the matrix rotation (from view)
        self.RotMtx=mtx33
        
    def scale(self,s): #modify the matrix scale (applied to view when calling the main matrix)
        self._scale*=s

    def getaxismtx(self): #a transformation matrix designed specifically for the GUI axis display
        rm=self.__ID44()
        rm[0][0]=self.RotMtx[0][0]
        rm[0][1]=self.RotMtx[0][1]*-1
        rm[0][2]=self.RotMtx[0][2]
        rm[1][0]=self.RotMtx[1][0]*-1
        rm[1][1]=self.RotMtx[1][1]
        rm[1][2]=self.RotMtx[1][2]*-1
        rm[2][0]=self.RotMtx[2][0]
        rm[2][1]=self.RotMtx[2][1]*-1
        rm[2][2]=self.RotMtx[2][2]
        return rm

__viewMatrix = __viewMatrixclass()
#all viewing transformations are applied to the view-matrix...
#this matrix is applied to the modelview matrix before drawing the models
#this saves performance since the calculations don't have to be recalculated for every frame
# however, calling __viewMatrix._getMtx() builds the matrix from internal eular values before returning it.
# (it's fast, but could be slightly faster (save the last matrix for re-use until updated))

def __if2f(i): return (i*0.003921568627450980392156862745098 if type(i)==int else i) #__if2f(255) >>> 1.0

from FORMAT import UMC_POINTS,UMC_LINES,UMC_LINESTRIP,UMC_LINELOOP,UMC_TRIANGLES,UMC_TRIANGLESTRIP,UMC_TRIANGLEFAN,UMC_QUADS,UMC_QUADSTRIP,UMC_POLYGON
__UMCGLPRIMITIVES = {
    UMC_POINTS:__GL.GL_POINTS,
    UMC_LINES:__GL.GL_LINES,
    UMC_LINESTRIP:__GL.GL_LINE_STRIP,
    UMC_LINELOOP:__GL.GL_LINE_LOOP,
    UMC_TRIANGLES:__GL.GL_TRIANGLES,
    UMC_TRIANGLESTRIP:__GL.GL_TRIANGLE_STRIP,
    UMC_TRIANGLEFAN:__GL.GL_TRIANGLE_FAN,
    UMC_QUADS:__GL.GL_QUADS,
    UMC_QUADSTRIP:__GL.GL_QUAD_STRIP,
    UMC_POLYGON:__GL.GL_POLYGON}

__GL_TEX = {}
def __M():
    global Libs,__UMCGLPRIMITIVES,__GL_TEX
    __GL.glEnable(__GL.GL_TEXTURE_2D)
    #__GL.glEnable(__GL.GL_ALPHA_TEST) #useless (deprecated anyways)
    
    #define textures here
    __GL.glPixelStorei(__GL.GL_UNPACK_ALIGNMENT,1)
    for Name,W,H,Pixels,Colors in Libs[7]:
        image = bytearray()
        if len(Colors)==0:
            Format = len(Pixels[0])-1 #I, IA, RGB, or RGBA format
            for IRAGBA in Pixels: image += bytearray(IRAGBA)
        else:
            Format = len(Colors[0])-1 #I, IA, RGB, or RGBA format
            for I in Pixels: image += bytearray(Colors[I])
            
        __GL_TEX[Name] = __GL.glGenTextures(1)
        __GL.glPixelStorei(__GL.GL_UNPACK_ALIGNMENT,1)
        _IFMT = [__GL.GL_RGB, __GL.GL_RGBA, __GL.GL_RGB, __GL.GL_RGBA][Format]
        _PXFMT = [__GL.GL_LUMINANCE,__GL.GL_LUMINANCE_ALPHA,__GL.GL_RGB,__GL.GL_RGBA][Format]
        __GL.glTexImage2D(__GL.GL_TEXTURE_2D, 0, _IFMT, W, H, 0, _PXFMT, __GL.GL_UNSIGNED_BYTE, str(image))

    __GL.glColor3f(1.0,1.0,1.0)
    for Name,Objects in Libs[2]:
        for ID in Objects:
            ObjectName,Viewport,LRS,Sub_Data,Parent_ID=Libs[3][ID]
            SDType,SDName,SDData1,SDData2=Sub_Data

            if SDType=="_Mesh":
                __GL.glLineWidth(1.0)

                MaterialName,AddOn,MatColors,Textures,R1,R2 = Libs[4][SDData1] if type(SDData1)==int else [
                    "UMC_Def_Mat", '', [[1.0,1.0,1.0,1.0],[1.0,1.0,1.0,1.0],[0.5,0.5,0.5,1.0],[0.0,0.0,0.0,0.0],25.0], [], [], []
                    ]
                
                MAR,MAG,MAB,MAA = MatColors[0] #Ambient
                MDR,MDG,MDB,MDA = MatColors[1] #Diffuse
                MSR,MSG,MSB,MSA = MatColors[2] #Specular
                MER,MEG,MEB,MEA = MatColors[3] #Emmisive
                MSV = MatColors[4] #Shininess
                
                C0R,C0G,C0B,C0A= (MAR+MDR)/2,(MAG+MDG)/2,(MAB+MDB)/2,(MAA+MDA)/2

                #call from pre-defined textures here
                for TexID in Textures:
                    TexName,TexParams,Reserved,ImageName = Libs[6][TexID]
                    
                    # Apply Texture(s)
                    __GL.glBindTexture(__GL.GL_TEXTURE_2D, __GL_TEX[ImageName] )
                    
                    #__GL.glTexEnvf(__GL.GL_TEXTURE_ENV, __GL.GL_TEXTURE_ENV_MODE, __GL.GL_MODULATE)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_WRAP_S, __GL.GL_CLAMP)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_WRAP_T, __GL.GL_CLAMP)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_WRAP_S, __GL.GL_REPEAT)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_WRAP_T, __GL.GL_REPEAT)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_MAG_FILTER, __GL.GL_NEAREST)
                    __GL.glTexParameterf(__GL.GL_TEXTURE_2D, __GL.GL_TEXTURE_MIN_FILTER, __GL.GL_NEAREST)
                    __GL.glTexEnvf(__GL.GL_TEXTURE_ENV, __GL.GL_TEXTURE_ENV_MODE, __GL.GL_MODULATE)

                Verts,Normals,Colors,UVs,Weights,Primitives=SDData2
                
                LC0,LC1=[0,0,0,0],[0,0,0,0] #Remember last used colors (starts at transparent black)
                for Primitive,Facepoints in Primitives:
                    __GL.glBegin(__UMCGLPRIMITIVES[Primitive])
                    for V,N,(C0,C1),(U0,U1,U2,U3,U4,U5,U6,U7) in Facepoints:

                        if U0!='': __GL.glMultiTexCoord2f(__GL.GL_TEXTURE0,UVs[0][U0][0],UVs[0][U0][1])
                        #if U1!='': glMultiTexCoord2f(GL_TEXTURE1,Fl(UVs[1][U1][0]),Fl(UVs[1][U1][1]))
                        #if U2!='': glMultiTexCoord2f(GL_TEXTURE2,Fl(UVs[2][U2][0]),Fl(UVs[2][U2][1]))
                        #if U3!='': glMultiTexCoord2f(GL_TEXTURE3,Fl(UVs[3][U3][0]),Fl(UVs[3][U3][1]))
                        #if U4!='': glMultiTexCoord2f(GL_TEXTURE4,Fl(UVs[4][U4][0]),Fl(UVs[4][U4][1]))
                        #if U5!='': glMultiTexCoord2f(GL_TEXTURE5,Fl(UVs[5][U5][0]),Fl(UVs[5][U5][1]))
                        #if U6!='': glMultiTexCoord2f(GL_TEXTURE6,Fl(UVs[6][U6][0]),Fl(UVs[6][U6][1]))
                        #if U7!='': glMultiTexCoord2f(GL_TEXTURE7,Fl(UVs[7][U7][0]),Fl(UVs[7][U7][1]))
                        #max texture is 31

                        if C0!='': #IRAGBA format
                            C0L=len(Colors[0][C0])
                            C0R,C0G,C0B,C0A=[__if2f(Colors[0][C0][0]),
                                             __if2f(Colors[0][C0][1]) if C0L>2 else __if2f(Colors[0][C0][0]),
                                             __if2f(Colors[0][C0][2]) if C0L>2 else __if2f(Colors[0][C0][0]),
                                             __if2f(Colors[0][C0][3]) if C0L==4 else (__if2f(Colors[0][C0][1]) if C0L==2 else 1.0)]
                            __GL.glColor4f((MAR+MDR+C0R)/3,(MAG+MDG+C0G)/3,(MAB+MDB+C0B)/3,(MAA+MDA+C0A)/3)
                                
                        if C1!='': #IRAGBA format
                            C1L=len(Colors[1][C1])
                            C1R,C1G,C1B,C1A=[__if2f(Colors[1][C1][0]),
                                             __if2f(Colors[1][C1][1]) if C1L>2 else __if2f(Colors[1][C1][0]),
                                             __if2f(Colors[1][C1][2]) if C1L>2 else __if2f(Colors[1][C1][0]),
                                             __if2f(Colors[1][C1][3]) if C1L==4 else (__if2f(Colors[1][C1][1]) if C1L==2 else 1.0)]
                            __GL.glSecondaryColor3f(C1R,C1G,C1B)
                            
                            #Alpha is supported but not registered here (glSecondaryColor4f is not a registered function)

                        UpdateMat=0
                        if LC0!=[C0R,C0G,C0B,C0A]: UpdateMat=1; LC0=[C0R,C0G,C0B,C0A]
                        #if LC1!=[C1R,C1G,C1B,C1A]: UpdateMat=1; LC1=[C1R,C1G,C1B,C1A]
                        if UpdateMat:
                            __GL.glMaterialfv(__GL.GL_FRONT_AND_BACK, __GL.GL_AMBIENT, [(MAR+C0R)/2,(MAG+C0G)/2,(MAB+C0B)/2,(MAA+C0A)/2])
                            __GL.glMaterialfv(__GL.GL_FRONT_AND_BACK, __GL.GL_DIFFUSE, [(MDR+C0R)/2,(MDG+C0G)/2,(MDB+C0B)/2,(MDA+C0A)/2])
                            __GL.glMaterialfv(__GL.GL_FRONT_AND_BACK, __GL.GL_SPECULAR, [(MSR+C0R)/2,(MSG+C0G)/2,(MSB+C0B)/2,(MSA+C0A)/2])
                            __GL.glMaterialfv(__GL.GL_FRONT_AND_BACK, __GL.GL_EMISSION, [MER,MEG,MEB,MEA])
                            __GL.glMaterialf(__GL.GL_FRONT_AND_BACK, __GL.GL_SHININESS, MSV)

                        if N!='': __GL.glNormal3f(Normals[N][0],Normals[N][1],Normals[N][2])

                        VL=len(Verts[V])
                        VX,VY,VZ=Verts[V]+([0.0] if VL==2 else [])
                        __GL.glVertex3f(VX,VY,VZ)

                    __GL.glEnd()
    __GL.glDisable(__GL.GL_TEXTURE_2D)
    #__GL.glDisable(__GL.GL_ALPHA_TEST)

def __N():
    global Libs,__UMCGLPRIMITIVES
    __GL.glLineWidth(1.0)
    __GL.glColor3f(0,1,1)
    for Name,Objects in Libs[2]:
        for ID in Objects:
            ObjectName,Viewport,LRS,Sub_Data,Parent_ID=Libs[3][ID]
            SDType,SDName,SDData1,SDData2=Sub_Data

            if SDType=="_Mesh":
                Verts,Normals,Colors,UVs,Weights,Primitives=SDData2
                for Primitive,Facepoints in Primitives:
                    __GL.glBegin(__GL.GL_LINES)
                    for V,N,Cs,Us in Facepoints:
                        if N!='':
                            NX,NY,NZ=Normals[N][0],Normals[N][1],Normals[N][2]
                            VL=len(Verts[V])
                            VX,VY,VZ=Verts[V]+([0.0] if VL==2 else [])
                            
                            __GL.glVertex3f(VX,VY,VZ)
                            __GL.glVertex3f(VX+NX,VY+NY,VZ+NZ)
                    __GL.glEnd()

def __B():
    global Libs
    for Name,Objects in Libs[2]:
        for ID in Objects:
            ObjectName,Viewport,LRS,Sub_Data,Parent_ID=Libs[3][ID]
            SDType,SDName,SDData1,SDData2=Sub_Data
            if SDType=="_Rig":
                __GL.glLineWidth(3.5)
                for bone in SDData2:
                    PLRS,CLRS = (SDData2[bone[4]][2] if type(bone[4])==int else [0,0,0,0,0,0,1,1,1]),bone[2]
                    __GL.glBegin(GL_LINES)
                    __GL.glColor3f(1,1,1)
                    __GL.glVertex3f((PLRS[0]*PLRS[6]),(PLRS[1]*PLRS[7]),(PLRS[2]*PLRS[8]))
                    __GL.glVertex3f((CLRS[0]*CLRS[6]),(CLRS[1]*CLRS[7]),(CLRS[2]*CLRS[8]))
                    __GL.glEnd()

def __Draw_Scene():
    global TOGGLE_FULLSCREEN,TOGGLE_LIGHTING,TOGGLE_3D,TOGGLE_WIREFRAME,TOGGLE_BONES,TOGGLE_ORTHO,TOGGLE_NORMALS
    global __viewMatrix
    global __TOP_GRID,__SIDE_GRID,__FRONT_GRID,__QUAD_FLOOR,__LINE_FLOOR,__MODEL_DATA,__NORMAL_DATA,__BONE_DATA

    __GL.glMultMatrixf(__viewMatrix._getMtx())

    __GL.glDisable(__GL.GL_LIGHTING) #disable for the grid
    if TOGGLE_GRID<4:
        global __TOP_GRID,__SIDE_GRID,__FRONT_GRID,__QUAD_FLOOR
        __GL.glCallList([__TOP_GRID,__SIDE_GRID,__FRONT_GRID,__QUAD_FLOOR][TOGGLE_GRID])

    
    if TOGGLE_LIGHTING: __GL.glEnable(__GL.GL_LIGHTING)
    __GL.glCallList(__MODEL_DATA) #finally got display lists working =D

    if TOGGLE_LIGHTING: __GL.glDisable(__GL.GL_LIGHTING) #disable for the grid and bones
    if TOGGLE_NORMALS: __GL.glCallList(__NORMAL_DATA)
    if TOGGLE_BONES:
        if TOGGLE_BONES==2: __GL.glClear( __GL.GL_DEPTH_BUFFER_BIT ) #overlay the bones (X-Ray)
        __GL.glCallList(__BONE_DATA)
        for Name,Objects in Libs[2]: #de-scaled bone joints
            for ID in Objects:
                ObjectName,Viewport,LRS,Sub_Data,Parent_ID=Libs[3][ID]
                SDType,SDName,SDData1,SDData2=Sub_Data
                if SDType=="_Rig":
                    for bone in SDData2:
                        PLRS,CLRS = (SDData2[bone[4]][2] if type(bone[4])==int else [0,0,0,0,0,0,1,1,1]),bone[2]
                        __GL.glTranslate((CLRS[0]*CLRS[6]),(CLRS[1]*CLRS[7]),(CLRS[2]*CLRS[8]))
                        #glutSolidSphere(0.03/__viewMatrix._scale, 25, 25)
                        __GL.glTranslate(-(CLRS[0]*CLRS[6]),-(CLRS[1]*CLRS[7]),-(CLRS[2]*CLRS[8]))
    
    pass

#___________________________________________________________________________________________
"""
_mode=0 #logger mode: 0=write, 1=append
DIR='' #to remember the import directory
def Keyboard(key, x, y):
    global TOGGLE_FULLSCREEN,TOGGLE_LIGHTING,TOGGLE_GRID,TOGGLE_WIREFRAME,TOGGLE_BONES,TOGGLE_3D,TOGGLE_ORTHO
    global _mode,DIR

    global __MODEL_DATA,__BONE_DATA

    #//--// need a GUI handler for these
    if key == chr(9): #import model
        typenames,modules,modnames,ihandlers,decmpr = [],[],[],[],[]; iftypes,isupport = [],[]
        for M,D,I in COMMON._Scripts[0][0]: #get model import scripts
            if D[1] != ('',['']): #script has model info (not sure if it's safe to remove this yet)
                iftypes+=[(D[1][0],tuple(["*.%s"%T for T in D[1][1]]))]
                for T in D[1][1]:
                    try: isupport.index("*.%s"%T) #is this file type already supported?
                    except: isupport+=["*.%s"%T] #add the current file type to the supported types list
                    modnames+=[D[1][0]] #displayed in the GUI or Tk fiter
                    typenames+=[T] #filetype
                    modules+=[M] #current script
                    ihandlers+=[I] #included image handlers

        #----- Tkinter dialog (will be replaced)
        _in=askopenfilename(title='Import Model', filetypes=[('Supported', " ".join(isupport))]+iftypes)

        #-----

        if _in=='': pass #action cancelled
        else:
            COMMON.__functions=[0,0,0,0] #prevent unwanted initialization

            #this block will change once I use my own dialog
            #Tkinter doesn't return the filter ID
            #-----
            it = _in.split('.')[-1]
            if typenames.count(it)>1:
                print '\nThis filetype is used by multiple scripts:\n'
                scr = []
                for idx,ft in enumerate(typenames):
                    if ft==it: scr+=[[modnames[idx],modules[idx]]]
                for I,NM in enumerate(scr): print ' %i - %s'%(I,NM[0])
                print
                sid=input('Please enter the script ID here: ')
                i=__import__(scr[sid][1])
            else:
                ti=typenames.index(it)
                i=__import__(modules[ti])
            COMMON.__ReloadScripts() #check for valid changes to the scripts
            #-----

            try: #can we get our hands on the file?
                COMMON.ImportFile(_in,1) #set the file data

                global Libs; __Libs=Libs #remember last session in case of a script error

                Libs=[[],[],[],[],[["Def_Scene",[]]],[]] #reset the data for importing
                print 'Converting from import format...'

                try: #does the script contain any unfound errors?
                    __LOG('-- importing %s --\n'%_in.split('/')[-1])
                    i.ImportModel(it,None)
                    print 'Verifying data...'
                    glNewList(__MODEL_DATA, GL_COMPILE); __M(); glEndList()
                    glNewList(__BONE_DATA, GL_COMPILE); __B(); glEndList()
                    print 'Updating Viewer\n'

                    glutSetWindowTitle("Universal Model Converter v3.0a (dev5) - %s" % _in.split('/')[-1])

                    #export UMC session data
                    l=open('session.ses','w')
                    l.write(str([1,Libs]))
                    l.close()

                    COMMON.__ClearFiles() #clear the file data to be used for writing

                except:
                    Libs=__Libs
                    print "Error! Check 'session-info.log' for more details.\n"
                    import traceback
                    typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
                    traceback.print_exception(
                        typ,val,tb#,
                        #limit=2,
                        #file=sys.stdout
                        )
                    print

                __Libs=[] #save memory usage

            except: pass #an error should already be thrown

            __WLOG(0) #write log
            COMMON.__CleanScripts() #remove pyc files

    if key == chr(5): #export model
        COMMON.__ClearFiles() #clear the file data again... just in case

        etypenames,emodules,emodnames,ehandlers = [],[],[],[]; eftypes = []
        for M,D,I in COMMON._Scripts[0][1]:
            if D[1] != ('',['']): #has model info
                eftypes+=[(D[1][0],tuple(["*.%s"%T for T in D[1][1]]))]
                for T in D[1][1]:
                    emodnames+=[D[1][0]]
                    etypenames+=[T]
                    emodules+=[M]
                    ehandlers+=[I]

        #Tkinter dialog (will be replaced)
        #-----
        _en=asksaveasfilename(title='Export Model', filetypes=eftypes, defaultextension='.ses')
        #-----

        if _en=='': pass
        else:
            COMMON.__functions=[0,0,0,0] #prevent unwanted initialization

            #this block will change once I use my own dialog
            #Tkinter doesn't return the filter ID
            #-----
            et = _en.split('.')[-1]
            if etypenames.count(et)>1:
                print '\nThis filetype is used by multiple scripts:\n'
                scr = []
                for idx,ft in enumerate(etypenames):
                    if ft==et: scr+=[[emodnames[idx],emodules[idx]]]
                for I,NM in enumerate(scr): print ' %i - %s'%(I,NM[0])
                print
                sid=input('Please enter the script ID here: ')
                e=__import__(scr[sid][1])
            else:
                e=__import__(emodules[etypenames.index(et)])
            COMMON.__ReloadScripts() #check for valid changes to the scripts
            #-----

            '''
            try:
                COMMON.ExportFile(_en) #add the file to the data space

                print 'converting to export format...'
                e.ExportModel(et,None)
                COMMON.__WriteFiles()
                print 'Done!'

            except:
                print "Error! Check 'session-info.log' for details.\n"
            '''
            COMMON.ExportFile(_en) #add the file to the data space

            print 'converting to export format...'
            e.ExportModel(et,None)
            COMMON.__WriteFiles()
            print 'Refreshing Viewer\n'
            #'''

            __WLOG(_mode) #write log
            COMMON.__CleanScripts() #remove pyc files
    #//--//
"""

#___________________________________________________________________________________________

def __SDLVResize(W,H, VMODE): #A limitation of SDL (the GL context also needs to be reset with the screen)
    __pyg.display.set_mode((W,H), VMODE)
    #DspInf = __pyg.display.Info()

    #UI display lists:
    global __TOP_GRID,__SIDE_GRID,__FRONT_GRID,__QUAD_FLOOR,__LINE_FLOOR,__MODEL_DATA,__NORMAL_DATA,__BONE_DATA

    def G(D):
        __GL.glLineWidth(1.0)
        GS=60; i0,i1 = (D+1 if D<2 else 0),(D-1 if D>0 else 2)
        C1,C2,A1,A2,nA1,nA2=[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]
        C1[D],C2[i0]=1,1
        A1[D],A2[i0]=GS,GS; nA1[D],nA2[i0]= -GS,-GS
        S1,iS1=A1,A1;S2,iS2=A2,A2; nS1,niS1=nA1,nA1;nS2,niS2=nA2,nA2
        __GL.glBegin(__GL.GL_LINES)
        __GL.glColor3fv(C1);__GL.glVertex3f(A1[0],A1[1],A1[2]);__GL.glVertex3f(nA1[0],nA1[1],nA1[2])
        __GL.glColor3fv(C2);__GL.glVertex3f(A2[0],A2[1],A2[2]);__GL.glVertex3f(nA2[0],nA2[1],nA2[2])
        __GL.glColor3f(0.5,0.5,0.5)
        s=0
        while s < GS:
            s+=10; S1[i0],nS1[i0],S2[D],nS2[D]=s,s,s,s
            __GL.glVertex3f(S1[0],S1[1],S1[2]);__GL.glVertex3f(nS1[0],nS1[1],nS1[2])
            __GL.glVertex3f(S2[0],S2[1],S2[2]);__GL.glVertex3f(nS2[0],nS2[1],nS2[2])
            iS1[i0],niS1[i0],iS2[D],niS2[D]=-s,-s,-s,-s
            __GL.glVertex3f(iS1[0],iS1[1],iS1[2]);__GL.glVertex3f(niS1[0],niS1[1],niS1[2])
            __GL.glVertex3f(iS2[0],iS2[1],iS2[2]);__GL.glVertex3f(niS2[0],niS2[1],niS2[2])
        __GL.glEnd()

    def F(D):
        __GL.glLineWidth(1.0)
        def quad(p1,p2):
            __GL.glVertex3f(p1+2.5,0,p2+2.5); __GL.glVertex3f(p1+2.5,0,p2-2.5)
            __GL.glVertex3f(p1-2.5,0,p2-2.5); __GL.glVertex3f(p1-2.5,0,p2+2.5)

        FS=40; clr=0.3125; p1=0
        while p1 < FS:
            clr=(0.3125 if clr==0.5 else 0.5); p2=0
            while p2 < FS:
                __GL.glColor3f(clr,clr,clr)
                if D: #draw lines so you can actually see the floor
                    __GL.glBegin(__GL.GL_LINE_LOOP); quad(p1,p2); __GL.glEnd()
                    __GL.glBegin(__GL.GL_LINE_LOOP); quad(p1,-p2); __GL.glEnd()
                    __GL.glBegin(__GL.GL_LINE_LOOP); quad(-p1,-p2); __GL.glEnd()
                    __GL.glBegin(__GL.GL_LINE_LOOP); quad(-p1,p2); __GL.glEnd()
                    #TODO: this draws lines for every quad instead of just the outside quads
                    #^a performance killer >_>
                else:
                    __GL.glBegin(__GL.GL_QUADS)
                    quad(p1,p2); quad(p1,-p2)
                    quad(-p1,p2); quad(-p1,-p2)
                    __GL.glEnd()
                p2+=5; clr=(0.3125 if clr==0.5 else 0.5)
            p1+=5

    __FRONT_GRID = __GL.glGenLists(1); __GL.glNewList(__FRONT_GRID, __GL.GL_COMPILE); G(2); __GL.glEndList()
    __SIDE_GRID = __GL.glGenLists(1);  __GL.glNewList(__SIDE_GRID, __GL.GL_COMPILE); G(1); __GL.glEndList()
    __TOP_GRID = __GL.glGenLists(1);   __GL.glNewList(__TOP_GRID, __GL.GL_COMPILE); G(0); __GL.glEndList()
    __QUAD_FLOOR = __GL.glGenLists(1); __GL.glNewList(__QUAD_FLOOR, __GL.GL_COMPILE); F(0); __GL.glEndList()
    __LINE_FLOOR = __GL.glGenLists(1); __GL.glNewList(__LINE_FLOOR, __GL.GL_COMPILE); F(1); __GL.glEndList()
    __MODEL_DATA = __GL.glGenLists(1); __BONE_DATA = __GL.glGenLists(1)
    __NORMAL_DATA = __GL.glGenLists(1)

    __GL.glClearColor(0.13, 0.13, 0.13, 1.0)
    __GL.glClearDepth(1.0)

    #TODO: need to manage these more efficiently:
    __GL.glEnable(__GL.GL_DEPTH_TEST)
    __GL.glDepthFunc(__GL.GL_LEQUAL)
    __GL.glEnable(__GL.GL_LIGHTING)
    __GL.glEnable(__GL.GL_LIGHT0)
    __GL.glEnable(__GL.GL_NORMALIZE) #scale normals when model is scaled
    __GL.glDisable(__GL.GL_BLEND) #disabled for models
    __GL.glBlendFunc(__GL.GL_SRC_ALPHA, __GL.GL_ONE_MINUS_SRC_ALPHA)

    #__GL.glDisable(__GL.GL_ALPHA_TEST)
    #__GL.glAlphaFunc(__GL.GL_GREATER, 0.1)

    __GL.glShadeModel(__GL.GL_SMOOTH)
    
    glNewList(__MODEL_DATA, GL_COMPILE); __M(); glEndList()
    glNewList(__NORMAL_DATA, GL_COMPILE); __N(); glEndList()
    glNewList(__BONE_DATA, GL_COMPILE); __B(); glEndList()

    #__GUI.__ResizeGUI(W,H)


def Init():
    
    VIDEOMODE = OPENGL|DOUBLEBUF|RESIZABLE
    #VIDEOMODE&=~RESIZABLE
    __pyg.display.init()
    icon = __pyg.Surface((1,1)); icon.set_alpha(255)
    __pyg.display.set_icon(icon)
    __pyg.display.set_caption("Universal Model Converter v3.0a (dev4.5)")
    global width,height
    __SDLVResize(width,height, VIDEOMODE)

    __pyg.joystick.init()
    joy = [__pyg.joystick.Joystick(j) for j in range(__pyg.joystick.get_count())]
    for j in joy: j.init()

    #__GUI.__initGUI()
    
    global W,H; LW,LH=W,H #restored screen size (coming from full-screen)
    global TOGGLE_FULLSCREEN,TOGGLE_LIGHTING,TOGGLE_GRID,TOGGLE_WIREFRAME,TOGGLE_BONES,TOGGLE_3D,TOGGLE_ORTHO
    MODS=0 #Modifier keys (global use) [ Alt(4)[0b100] | Ctrl(2)[0b10] | Shift(1)[0b1] ]
    __lastRot = __AB.Matrix3fT() #last updated rotation (ArcBall view rotation)
    O = 0.025 # eye translation offset
    EYE=None #3D L or R EYE (for Shutter method)
    while True:
        '''
        line=0
        for axis in range(GCNJS.get_numaxes()):
            #sys.stdout.write("axis%i: %s\n"%(axis,str(GCNJS.get_axis(axis))))
            GCNJS.get_axis(axis)
            line+=1
        for hat in range(GCNJS.get_numhats()):
            #sys.stdout.write("hat%i: %s\n"%(hat,str(GCNJS.get_hat(hat))))
            GCNJS.get_hat(hat)
            line+=1
        for button in range(GCNJS.get_numbuttons()):
            #sys.stdout.write("button%i: %s\n"%(button,str(GCNJS.get_button(button))))
            GCNJS.get_button(button)
            line+=1
        #sys.stdout.write('%s'%('\r'*line))
        '''

        for i,e in enumerate(__pyg.event.get()):
            if e.type == QUIT: __pyg.display.quit(); return None #VIEWER.init() >>> None

            if e.type == ACTIVEEVENT: pass #e.gain; e.state

            if e.type == KEYDOWN: #e.key; e.mod
                #__GUI.__KeyPress(e.key)

                if e.key==K_RSHIFT or e.key==K_LSHIFT: MODS|=0b001
                if e.key==K_RCTRL or e.key==K_LCTRL: MODS|=0b010
                if e.key==K_RALT or e.key==K_LALT: MODS|=0b100

                if e.key not in [K_RSHIFT,K_LSHIFT,K_RCTRL,K_LCTRL,K_RALT,K_LALT]:
                    TOGGLE_GRID=(2 if TOGGLE_GRID<3 else TOGGLE_GRID) #don't let MODS affect the grid
                    

                if e.key==K_KP5:
                    TOGGLE_ORTHO = 0 if TOGGLE_ORTHO else 1
                    '''
                    __GUI.Widgets['Projection'].info[0]=[1,0][__GUI.Widgets['Projection'].info[0]] #change widget state
                    TOGGLE_ORTHO = __GUI.Widgets['Projection'].info[0] #verify TOGGLE_ORTHO if panel is closed
					'''
                    
                if e.key==K_i:
                    if MODS&0b010: #import model
                        import COMMON
                        typenames,modules,modnames,ihandlers = [],[],[],[]; iftypes,isupport = [],[]
                        for M,D,I in COMMON._Scripts[0][0]:
                            if D[1] != ('',['']): #has model info
                                iftypes+=[(D[1][0],tuple(["*.%s"%T for T in D[1][1]]))]
                                for T in D[1][1]:
                                    try: isupport.index("*.%s"%T)
                                    except: isupport+=["*.%s"%T]
                                    modnames+=[D[1][0]]
                                    typenames+=[T]
                                    modules+=[M]
                                    ihandlers+=[I]
                                    
                        #----- Tkinter dialog (will be replaced)
                        _in=askopenfilename(title='Import Model', filetypes=[('Supported', " ".join(isupport))]+iftypes)
                        #-----
                        
                        if _in=='': pass #action cancelled
                        else:
                            COMMON.__functions=[0,0,0,0] #prevent unwanted initialization

                            #this block will change once I use my own dialog
                            #Tkinter doesn't return the filter ID
                            #-----
                            it = _in.split('.')[-1]
                            if typenames.count(it)>1:
                                print '\nThis filetype is used by multiple scripts:\n'
                                scr = []
                                for idx,ft in enumerate(typenames):
                                    if ft==it: scr+=[[modnames[idx],modules[idx]]]
                                for I,NM in enumerate(scr): print ' %i - %s'%(I,NM[0])
                                print 
                                sid=input('Please enter the script ID here: ')
                                i=__import__(scr[sid][1])
                            else:
                                i=__import__(modules[typenames.index(it)])
                            #-----
                            
                            try: #can we get our hands on the file?
                                COMMON.ImportFile(_in,1) #set the file data
                                
                                global Libs; __Libs=Libs #remember last session in case of a script error

                                Libs=[[],[],[["Def_Scene",[]]],[],[],[],[],[]] #reset the data for importing
                                print 'Converting from import format...'
                                
                                try: #does the script contain any unfound errors?
                                    __LOG('-- importing %s --\n'%_in.split('/')[-1])
                                    i.ImportModel(it,None)
                                    print 'Verifying data...'

                                    #export UMC session data
                                    l=open('session.ses','w')
                                    l.write(str([1,Libs]))
                                    l.close()

                                    glNewList(__MODEL_DATA, GL_COMPILE); __M(); glEndList()
                                    glNewList(__NORMAL_DATA, GL_COMPILE); __N(); glEndList()
                                    glNewList(__BONE_DATA, GL_COMPILE); __B(); glEndList()
                                    print 'Updating Viewer\n'
                                    
                                    __pyg.display.set_caption("Universal Model Converter v3.0a (dev4.5) - %s" % _in.split('/')[-1])
                                    #glutSetWindowTitle("Universal Model Converter v3.0a (dev5) - %s" % _in.split('/')[-1])

                                    COMMON.__ClearFiles() #clear the file data to be used for writing

                                except:
                                    Libs=__Libs
                                    print "Error! Check 'session-info.log' for more details.\n"
                                    import sys,traceback
                                    typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
                                    traceback.print_exception(
                                        typ,val,tb#,
                                        #limit=2,
                                        #file=sys.stdout
                                        )
                                    print
                                
                                __Libs=[] #save memory usage
                            
                            except: pass #an error should already be thrown

                            __WLOG(0) #write log
                            COMMON.__CleanScripts() #remove pyc files
					
                if e.key==K_e:
                    if MODS&0b010: #export model
                        COMMON.__ClearFiles() #clear the file data again... just in case
                        
                        etypenames,emodules,emodnames,ehandlers = [],[],[],[]; eftypes = []
                        for M,D,I in COMMON._Scripts[0][1]:
                            if D[1] != ('',['']): #has model info
                                eftypes+=[(D[1][0],tuple(["*.%s"%T for T in D[1][1]]))]
                                for T in D[1][1]:
                                    emodnames+=[D[1][0]]
                                    etypenames+=[T]
                                    emodules+=[M]
                                    ehandlers+=[I]

                        #Tkinter dialog (will be replaced)
                        #-----
                        _en=asksaveasfilename(title='Export Model', filetypes=eftypes, defaultextension='.ses')
                        #-----
                        
                        if _en=='': pass
                        else:
                            COMMON.__functions=[0,0,0,0] #prevent unwanted initialization
                            
                            #this block will change once I use my own dialog
                            #Tkinter doesn't return the filter ID
                            #-----
                            et = _en.split('.')[-1]
                            if etypenames.count(et)>1:
                                print '\nThis filetype is used by multiple scripts:\n'
                                scr = []
                                for idx,ft in enumerate(etypenames):
                                    if ft==et: scr+=[[emodnames[idx],emodules[idx]]]
                                for I,NM in enumerate(scr): print ' %i - %s'%(I,NM[0])
                                print 
                                sid=input('Please enter the script ID here: ')
                                em=__import__(scr[sid][1])
                            else:
                                em=__import__(emodules[etypenames.index(et)])
                            #-----

                            try:
                                COMMON.ExportFile(_en) #add the file to the data space
                                
                                print 'converting to export format...'
                                em.ExportModel(et,None)
                                COMMON.__WriteFiles()
                                print 'Done!'
                                
                            except:
                                print "Error! Check 'session-info.log' for more details.\n"
                                import sys,traceback
                                typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
                                print
                                traceback.print_exception(
                                    typ,val,tb#,
                                    #limit=2,
                                    #file=sys.stdout
                                    )
                                
                            __WLOG(0) #write log
                            COMMON.__CleanScripts() #remove pyc files

                if e.key==K_KP9: #reset the view
                    if MODS==0: 
                        __viewMatrix.mtxrotate(__AB.Matrix3fT()) #rotation
                        __viewMatrix.rotate(10.0,350.0,0.0)
                    elif MODS&0b001: __viewMatrix.X=0.0;__viewMatrix.Y=0.0;__viewMatrix.Z=0.0 #translation
                    elif MODS&0b010: __viewMatrix._scale=0.1 #scale
                    elif MODS&0b100: __viewMatrix.reset() #everything

                if e.key==K_KP8: #rotate/translate U
                    if MODS&0b001: __viewMatrix.translate(0.0,-0.25,0.0)
                    else: __viewMatrix.rotate(5.0,0.0,0.0)
                if e.key==K_KP2: #rotate/translate D
                    if MODS&0b001: __viewMatrix.translate(0.0,0.25,0.0)
                    else: __viewMatrix.rotate(-5.0,0.0,0.0)
                if e.key==K_KP4: #rotate/translate L
                    if MODS&0b001: __viewMatrix.translate(0.25,0.0,0.0)
                    else: __viewMatrix.rotate(0.0,5.0,0.0)
                if e.key==K_KP6: #rotate/translate R
                    if MODS&0b001: __viewMatrix.translate(-0.25,0.0,0.0)
                    else: __viewMatrix.rotate(0.0,-5.0,0.0)


                #//--// kept as an added option
                if e.key==K_KP_PLUS: __viewMatrix.scale(1.1)
                if e.key==K_KP_MINUS: __viewMatrix.scale(1/1.1)
                #//--//


                if e.key==K_KP1: #front view
                    TOGGLE_GRID=(0 if TOGGLE_GRID<3 else TOGGLE_GRID)
                    __viewMatrix.mtxrotate(__AB.Matrix3fT()) #reset the rotation using a minor bug
                    if MODS&0b010: __viewMatrix.rotate(0.0,180.0,0.0) #back View
                    
                if e.key==K_KP3:
                    TOGGLE_GRID=(1 if TOGGLE_GRID<3 else TOGGLE_GRID)
                    __viewMatrix.mtxrotate(__AB.Matrix3fT()) #reset the rotation
                    if MODS&0b010: __viewMatrix.rotate(0.0,90.0,0.0) #right-side View
                    else: __viewMatrix.rotate(0.0,-90.0,0.0) #left-side view
                    
                if e.key==K_KP7:
                    TOGGLE_GRID=(2 if TOGGLE_GRID<3 else TOGGLE_GRID)
                    __viewMatrix.mtxrotate(__AB.Matrix3fT()) #reset the rotation
                    if MODS&0b010: __viewMatrix.rotate(-90.0,0.0,0.0) #bottom View
                    else: __viewMatrix.rotate(90.0,0.0,0.0) #top view

                if e.key==K_ESCAPE: 
                    if TOGGLE_FULLSCREEN:
                        TOGGLE_FULLSCREEN=0
                        VIDEOMODE&=~FULLSCREEN
                        VIDEOMODE|=RESIZABLE
                        W,H = LW,LH
                    else:
                        TOGGLE_FULLSCREEN=1
                        VIDEOMODE&=~RESIZABLE
                        VIDEOMODE|=FULLSCREEN
                        LW,LH=W,H; W,H = 1280,1024

                    __SDLVResize(W,H, VIDEOMODE)
                    __abt.setBounds(W,H)

            if e.type == KEYUP: #e.key; e.mod
                #__GUI.__KeyRelease(e.key)

                if e.key==K_RSHIFT or e.key==K_LSHIFT: MODS&=0b110
                if e.key==K_RCTRL or e.key==K_LCTRL: MODS&=0b101
                if e.key==K_RALT or e.key==K_LALT: MODS&=0b011

            if e.type == MOUSEBUTTONDOWN: #e.pos; e.button
                x,y=e.pos
                #__GUI.__Click(e.button,(1./W)*x,(1./H)*y) #GUI
                __GUI.__CheckHit(e.button,(1./W)*x,(1./H)*y,True)

                if e.button==2:
                    __lastRot=__viewMatrix.RotMtx
                    __abt.click(__AB.Point2fT(x,y))
                else: __lastRot=__viewMatrix.RotMtx

                if   e.button==4: 
                    if MODS==0: __viewMatrix.scale(1.1)
                    elif MODS&0b001: __viewMatrix.translate(0.0,0.25,0.0) #translate Y
                    elif MODS&0b010: __viewMatrix.translate(0.25,0.0,0.0) #translate X
                elif e.button==5:
                    if MODS==0: __viewMatrix.scale(1/1.1)
                    elif MODS&0b001: __viewMatrix.translate(0.0,-0.25,0.0) #translate Y
                    elif MODS&0b010: __viewMatrix.translate(-0.25,0.0,0.0) #translate X

            if e.type == MOUSEBUTTONUP: #e.pos; e.button
                x,y=e.pos
                #__GUI.__Release(e.button,(1./W)*x,(1./H)*y)
                __GUI.__CheckHit(e.button,(1./W)*x,(1./H)*y,False)

                if e.button==2: __lastRot=__viewMatrix.RotMtx

            if e.type == MOUSEMOTION: #e.pos; e.rel; e.buttons
                x,y = e.pos; rx,ry = e.rel
                #__GUI.__Motion(e.buttons,x,y,rx,ry) #GUI

                if e.buttons[1]: #MMB view rotation (like blender24)
                    if MODS&0b001: 
                        s = __viewMatrix._scale
                        tx = ((1./W)*rx)/s
                        ty = ((1./H)*-ry)/s
                        __viewMatrix.translate(tx,ty,0.0)
                    elif MODS&0b010:
                        s = ry
                        __viewMatrix.scale(s)
                    else:
                        __viewMatrix.mtxrotate(
                            __AB.Matrix3fMulMatrix3f(
                                __lastRot, #get our previous view rot matrix
                                __AB.Matrix3fSetRotationFromQuat4f(__abt.drag(__AB.Point2fT(x,y))) #get a rot matrix from the mouse position
                            ) #multiply the matrices
                        ) #update the view matrix with the new rotation

                    if TOGGLE_GRID<3 and TOGGLE_GRID!=2: TOGGLE_GRID=2

            if e.type == JOYAXISMOTION: #e.joy; e.axis; e.value
                pass #print 'Joy:',e.joy, ', Axis:',e.axis, ', Value:',e.value
            if e.type == JOYBALLMOTION: pass #e.joy; e.ball; e.rel
            if e.type == JOYHATMOTION: #e.joy; e.hat; e.value
                pass #print 'Joy:',e.joy, ', Hat:',e.hat, ', Value:',e.value
            if e.type == JOYBUTTONDOWN: #e.joy; e.button
                pass #print 'Joy:',e.joy, ', Button:',e.button
            if e.type == JOYBUTTONUP: pass #e.joy; e.button

            if e.type == VIDEORESIZE: #e.size; e.w; e.h
                _w,_h = e.size
                if _w+_h>0 and _h>0:
                    W,H=_w,_h
                    __SDLVResize(W,H, VIDEOMODE)
                    __abt.setBounds(W,H)

            if e.type == VIDEOEXPOSE: pass
            if e.type == USEREVENT: pass #e.code
           
        
        #Display:

        __GL.glViewport(0, 0, W, H)

        __GL.glMatrixMode(__GL.GL_MODELVIEW)
        __GL.glLoadIdentity()

        __GL.glClear(__GL.GL_COLOR_BUFFER_BIT|__GL.GL_DEPTH_BUFFER_BIT)

        __GL.glPushMatrix()

        __GL.glLightfv(__GL.GL_LIGHT0, __GL.GL_POSITION, ( 1.5, 1.5, 2.0, 0.0 ))

        __GL.glPolygonMode(__GL.GL_FRONT_AND_BACK,(__GL.GL_LINE if TOGGLE_WIREFRAME else __GL.GL_FILL))

        if TOGGLE_3D==1: #Analglyph
            __GL.glDrawBuffer( __GL.GL_BACK_LEFT ) #not really sure why this is needed,
            #but the code doesn't work if removed...

            #L Eye (2 colors)
            if   TOGGLE_3D_MODE[0]==0: __GL.glColorMask( 1,0,0,1 )
            elif TOGGLE_3D_MODE[0]==1: __GL.glColorMask( 0,1,0,1 )
            elif TOGGLE_3D_MODE[0]==2: __GL.glColorMask( 0,0,1,1 )
            __GL.glClear( __GL.GL_COLOR_BUFFER_BIT | __GL.GL_DEPTH_BUFFER_BIT )
            __GL.glLoadIdentity(); __GL.glTranslate(O,0.0,0.0)
            __Draw_Scene()

            #R Eye (1 color)
            if TOGGLE_3D_MODE[0]==0: __GL.glColorMask( 0,1,1,1 ) #doesn't overlay
            if TOGGLE_3D_MODE[0]==1: __GL.glColorMask( 1,0,1,1 )
            if TOGGLE_3D_MODE[0]==2: __GL.glColorMask( 1,1,0,1 )
            __GL.glClear( __GL.GL_DEPTH_BUFFER_BIT )
            __GL.glLoadIdentity(); __GL.glTranslate(-O*2,0.0,0.0)
            __Draw_Scene()

            __GL.glColorMask( 1,1,1,1 ) #restore the color mask for later drawing

        elif TOGGLE_3D==2: #Shutter (need a better method than simply rotating between frames)
            #does not require quad-buffered hardware. (I might add error-detection-support for this later)
            #... if your machine supports this, it should greatly improve visual performance quality ;)
            EYE=(-O if EYE==O else O)
            __viewMatrix.translate(EYE,0.0,0.0)
            __Draw_Scene()

        else: __Draw_Scene() #no 3D display
        __GL.glPopMatrix()

        __GUI.__DrawGUI(W, H, __viewMatrix.getaxismtx())


        __GL.glMatrixMode(__GL.GL_PROJECTION)
        __GL.glLoadIdentity()

        P=float(W)/float(H)
        if TOGGLE_ORTHO: __GL.glOrtho(-2*P, 2*P, -2, 2, -100, 100)
        else: __GLU.gluPerspective(43.6025, P, 1, 100.0); __GLU.gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        #gluLookAt( eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz)
        #glOrtho(GLdouble left, GLdouble right, GLdouble bottom, GLdouble top, GLdouble near, GLdouble far)
        #glFrustum(GLdouble left, GLdouble right, GLdouble bottom, GLdouble top, GLdouble near, GLdouble far)
        #gluPerspective(GLdouble fovy, GLdouble aspect, GLdouble near, GLdouble far)

        __pyg.display.flip()
#Init()
