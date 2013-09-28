#1
#v 0.001

import COMMON #file vars and functions for import/export processing

import VIEWER #mainly for the toggles
from VIEWER import __GL,__GLU#,__GLUT #GL functions

'''
from COMMON import Scripts


#Shapes (private)
#Widgets (private)
def Button(Text,X,Y,W,H,): pass


def Browser():
    import os
    Dir='C:/'; done=0

    clicked = 0

    while not done:
        items = os.listdir(Dir)

        cancel = Button('Cancel')
        if not cancel:
            if Button('..'):
                Dir
            else: #need a better RT method >_>
                #TODO: parse the list and collect info first
                for item in items:
                    if Button(item): #draw Clicked button
                        clicked=1
                    else: #draw unclicked button
                        if clicked: #action
                            clicked=0
                            if os.path.isdir(Dir+item):
                                Dir+=(item+'/')
                            else:
                                done=1
                                return Dir+item
                        else:
                            pass
                
        else:
            done=1
            return None


'''

#the GL selection/feedback buffers are a bit complicated for me,
#so I'm defining my own method derived from GL. (should be faster)

#GL wanted me to redraw everything during the selection and then after the selection...
#my method compaires the hitdefs with the current selection and changes the state of a valid hit

W_HitDefs = {} #this stores the hit-area for each widget (constantly updated during state changes)
W_States = {} #this stores the state of each widget
W_Types = {} #this stores the type of each widget (proper hit-logic handling depends on type)

pw,ph = 800,600

def __ImportModel(fpath, filterID): #Model import process
	pass
def __ExportModel(fpath, filterID): #Model export process
	pass
def __ImportAnim(fpath, filterID): #Anim import process
	pass
def __ExportAnim(fpath, filterID): #Anim export process
	pass
	
	
def __TButton(X,Y,Na,St=False,Text=''):
	global pw,ph
	
	try: State = W_States[Na]
	except KeyError: 
		State = St
		W_States.update({Na:St})
		W_Types.update({Na:'toggle'})
		
	W_HitDefs.update({Na:[X,Y,X+(pw*20),Y+(ph*20)]})
	
	if State: __GL.glColor4f(0.0,0.0,0.0,0.25)
	else:  __GL.glColor4f(0.0,0.0,0.0,0.1)
		
	__GL.glBegin(__GL.GL_QUADS)
	__GL.glVertex2f(X,Y)
	__GL.glVertex2f(X+(pw*20),Y)
	__GL.glVertex2f(X+(pw*20),Y+(ph*20))
	__GL.glVertex2f(X,Y+(ph*20))
	__GL.glEnd()
	
	return State
	
def __Button(X1,Y1,X2,Y2,Na,Text=''):
	global pw,ph
	pass
	
def __Browser(): #overlays GUI when activated (Clears hit-defs to avoid improper activation)
	#return file_path, filter_index
	pass
	
def __BrowseBar(X1,Y1,W):
	global pw,ph
	pass

def __ExPanel(X1,Y1,X2,Y2,EB,Na,MX=0,MY=0,St=True): #returns current state for other widgets
	global pw,ph
	
	try: State = W_States[Na]
	except KeyError: 
		State = St
		W_States.update({Na:St})
		W_Types.update({Na:'toggle'})
	
	if State:
		__GL.glBegin(__GL.GL_QUADS) 
		__GL.glColor4f(0.5,0.5,0.5,0.8) #model (left) panel
		__GL.glVertex2f(X1,Y1)
		__GL.glVertex2f(X1,Y2)
		__GL.glVertex2f(X2,Y2)
		__GL.glVertex2f(X2,Y1)
		__GL.glEnd()
		
	#60x15px rectangle
	if   EB==0: #top
		EBX1,EBY1,EBX2,EBY2=(X1+((X2-X1)/2)-(pw*30)),Y1,(X1+((X2-X1)/2)+(pw*30)),Y1+(ph*15)
		TPX1,TPY1 = EBX1+(pw*25),EBY1+(ph*5)
		TPX2,TPY2 = EBX1+(pw*30),EBY1+(ph*10)
		TPX3,TPY3 = EBX1+(pw*35),EBY1+(ph*5)
	elif EB==1: #right
		EBX1,EBY1,EBX2,EBY2=X2-(pw*15),((Y2-Y1)/2)-(ph*30),X2,((Y2-Y1)/2)+(ph*30)
		TPX1,TPY1 = EBX1+(pw*10),EBY1+(ph*25)
		TPX2,TPY2 = EBX1+(pw*5),EBY1+(ph*30)
		TPX3,TPY3 = EBX1+(pw*10),EBY1+(ph*35)
	elif EB==2: #bottom
		EBX1,EBY1,EBX2,EBY2=(X1+((X2-X1)/2)-(pw*30)),Y2-(ph*15),(X1+((X2-X1)/2)+(pw*30)),Y2
		TPX1,TPY1 = EBX1+(pw*25),EBY1+(ph*10)
		TPX2,TPY2 = EBX1+(pw*30),EBY1+(ph*5)
		TPX3,TPY3 = EBX1+(pw*35),EBY1+(ph*10)
	elif EB==3: #left
		EBX1,EBY1,EBX2,EBY2=X1,((Y2-Y1)/2)-(ph*30),X1+(pw*15),((Y2-Y1)/2)+(ph*30)
		TPX1,TPY1 = EBX1+(pw*5),EBY1+(ph*25)
		TPX2,TPY2 = EBX1+(pw*10),EBY1+(ph*30)
		TPX3,TPY3 = EBX1+(pw*5),EBY1+(ph*35)
	
	#is the panel expanded?
	if not State: 
		if   EB==0: #top
			Eq=((Y2-Y1)-(ph*15))
			EBY1,EBY2=EBY1+Eq,EBY2+Eq
			TPY1,TPY2,TPY3=TPY1+(Eq+(ph*5)),TPY2+(Eq-(ph*5)),TPY3+(Eq+(ph*5))
		elif EB==1: #right
			Eq=((X2-X1)-(pw*15))
			EBX1,EBX2=EBX1-Eq,EBX2-Eq
			TPX1,TPX2,TPX3=TPX1-(Eq+(pw*5)),TPX2-(Eq-(pw*5)),TPX3-(Eq+(pw*5))
		elif EB==2: #bottom
			Eq=((Y2-Y1)-(ph*15))
			EBY1,EBY2=EBY1-Eq,EBY2-Eq
			TPY1,TPY2,TPY3=TPY1-(Eq+(ph*5)),TPY2-(Eq-(ph*5)),TPY3-(Eq+(ph*5))
		elif EB==3: #left
			Eq=((X2-X1)-(pw*15))
			EBX1,EBX2=EBX1+Eq,EBX2+Eq
			TPX1,TPX2,TPX3=TPX1+(Eq+(pw*5)),TPX2+(Eq-(pw*5)),TPX3+(Eq+(pw*5))
			
		__GL.glColor4f(0.5,0.5,0.5,0.8)
		__GL.glBegin(__GL.GL_QUADS) #(just the BG color behind the toggle button)
		__GL.glVertex2f(EBX1+MX,EBY1+MY)
		__GL.glVertex2f(EBX1+MX,EBY2+MY)
		__GL.glVertex2f(EBX2+MX,EBY2+MY)
		__GL.glVertex2f(EBX2+MX,EBY1+MY)
		__GL.glEnd()
		
	W_HitDefs.update({Na:[EBX1+MX,EBY1+MY,EBX2+MX,EBY2+MY]})
	
	__GL.glColor4f(0.0,0.0,0.0,0.2)
	__GL.glBegin(__GL.GL_QUADS)
	__GL.glVertex2f(EBX1+MX,EBY1+MY)
	__GL.glVertex2f(EBX1+MX,EBY2+MY)
	__GL.glVertex2f(EBX2+MX,EBY2+MY)
	__GL.glVertex2f(EBX2+MX,EBY1+MY)
	__GL.glEnd()
	__GL.glBegin(__GL.GL_TRIANGLES)
	__GL.glVertex2f(TPX1+MX,TPY1+MY)
	__GL.glVertex2f(TPX2+MX,TPY2+MY)
	__GL.glVertex2f(TPX3+MX,TPY3+MY)
	__GL.glEnd()
	
	return State

ORTHO = True
def __DrawGUI(w,h,RotMatrix): #called directly by the display function after drawing the scene
	global pw,ph
	#the GUI is drawn over the scene by clearing the depth buffer
	pw,ph=1./w,1./h
	
	global W_HitDefs
	W_HitDefs = {} #clear the hitdefs to avoid improper activation
	
	__GL.glMatrixMode(__GL.GL_PROJECTION)
	__GL.glLoadIdentity()
	#glOrtho(-2*P, 2*P, -2, 2, -100, 100)
	__GLU.gluOrtho2D(0.0, 1.0, 1.0, 0.0)
	
	__GL.glMatrixMode(__GL.GL_MODELVIEW)
	
	__GL.glClear( __GL.GL_DEPTH_BUFFER_BIT )
	__GL.glPolygonMode(__GL.GL_FRONT_AND_BACK,__GL.GL_FILL)
	
	__GL.glLoadIdentity()
	
	__GL.glEnable(__GL.GL_BLEND)
	__GL.glDisable(__GL.GL_DEPTH_TEST)
	__GL.glDisable(__GL.GL_LIGHTING)
	
	__GL.glBegin(__GL.GL_QUADS) 
	__GL.glColor4f(0.4,0.4,0.4,0.8) #options toggle
	__GL.glVertex2f(pw*0,ph*0)
	__GL.glVertex2f(pw*w,ph*0)
	__GL.glVertex2f(pw*w,ph*20)
	__GL.glVertex2f(pw*0,ph*20)
	__GL.glEnd()
	__GL.glColor4f(0.0,0.0,0.0,0.2)
	__GL.glBegin(__GL.GL_TRIANGLES)
	__GL.glVertex2f(pw*((w/2)-10),ph*6)
	__GL.glVertex2f(pw*((w/2)+10),ph*6)
	__GL.glVertex2f(pw*(w/2),ph*15)
	__GL.glEnd()
	
	M = __ExPanel(pw*0,ph*21,pw*210,ph*h,1,'MODEL')
	if M:
		__BrowseBar(pw*10,ph*40,180)
		
	A = __ExPanel(pw*(w-210),ph*21,pw*w,ph*h,3,'ANIM')
	D = __ExPanel(pw*(211 if M else 1),ph*21,pw*(w-(211 if A else 1)),ph*150,2,'DSPL',(0 if M else pw*105)+(0 if A else pw*-105))
	if D:
		VIEWER.TOGGLE_LIGHTING = __TButton(pw*(221 if M else 11),ph*31,'EnLight',True,'Lighting')
		VIEWER.TOGGLE_WIREFRAME = __TButton(pw*(221 if M else 11),ph*56,'EnWire',False,'Wireframe')
		VIEWER.TOGGLE_BONES = __TButton(pw*(221 if M else 11),ph*81,'EnBone',True,'Bones')

		global ORTHO
		if VIEWER.TOGGLE_ORTHO != ORTHO: W_States['EnOrtho'] = VIEWER.TOGGLE_ORTHO; ORTHO = VIEWER.TOGGLE_ORTHO #HACK
		ORTHO = __TButton(pw*(321 if M else 111),ph*31,'EnOrtho',True,'Ortho')
		VIEWER.TOGGLE_ORTHO = ORTHO

		VIEWER.TOGGLE_3D = __TButton(pw*(321 if M else 111),ph*56,'En3D',False,'3D Analglyph')
		VIEWER.TOGGLE_NORMALS = __TButton(pw*(321 if M else 111),ph*81,'EnNrm',False,'Normals')
		
	C = __ExPanel(pw*(211 if M else 1),ph*(h-150),pw*(w-(211 if A else 1)),ph*h,0,'CTRL',(0 if M else pw*105)+(0 if A else pw*-105))
	
	
	__GL.glDisable(__GL.GL_BLEND)
	__GL.glEnable(__GL.GL_DEPTH_TEST)
	
	#axis
	__GL.glLineWidth(1.0)
	__GL.glPushMatrix()
	__GL.glTranslatef(pw*(228 if M else 17),ph*(h-(167 if C else 17)),0)
	__GL.glScalef(pw*600,ph*600,1)
	__GL.glMultMatrixf(RotMatrix)

	__GL.glColor3f(1.0,0.0,0.0)
	__GL.glBegin(__GL.GL_LINES); __GL.glVertex3f(0.0,0.0,0.0); __GL.glVertex3f(0.02,0.0,0.0); __GL.glEnd() #X
	__GL.glTranslatef(0.0145,0.0,0.0); __GL.glRotatef(90, 0.0, 1.0, 0.0)
	#__GLUT.glutSolidCone(0.003, 0.011, 8, 1)
	__GL.glRotatef(-90, 0.0, 1.0, 0.0); __GL.glTranslatef(-0.0145,0.0,0.0)
	__GL.glColor3f(0.0,1.0,0.0)
	__GL.glBegin(__GL.GL_LINES); __GL.glVertex3f(0.0,0.0,0.0); __GL.glVertex3f(0.0,-0.02,0.0); __GL.glEnd() #Y
	__GL.glTranslatef(0.0,-0.0145,0.0); __GL.glRotatef(90, 1.0, 0.0, 0.0)
	#__GLUT.glutSolidCone(0.003, 0.011, 8, 1)
	__GL.glRotatef(-90, 1.0, 0.0, 0.0); __GL.glTranslatef(0.0,0.0145,0.0)
	__GL.glColor3f(0.0,0.0,1.0)
	__GL.glBegin(__GL.GL_LINES); __GL.glVertex3f(0.0,0.0,0.0); __GL.glVertex3f(0.0,0.0,0.02); __GL.glEnd() #Z
	__GL.glTranslatef(0.0,0.0,0.0145)
	#__GLUT.glutSolidCone(0.003, 0.011, 8, 1)
	__GL.glTranslatef(0.0,0.0,-0.0145)
	__GL.glColor3f(0.5,0.5,0.5) ; #__GLUT.glutSolidSphere(0.003, 8, 4)
	__GL.glPopMatrix()
	


lastHit = [0,False] #last hit record to be compaired with current hit record [ button, state ]
def __CheckHit(b,x,y,s): #checks if the hit (click) executes a command
	#b - mouse-button (0,1,2 = L,M,R)
	#x,y hit position
	#s - state 1 - 0 = execute (full click)
	#    state starts at 0
	#    1 means we've clicked a button (we can change our area during this)
	#    0 means we've released
	
	#the state will cause the area to have different affects on different widgets when a particular button is pressed.
	
	#print ['L','M','R'][b]+' - '+str([x,y])+' - '+str(s)
	#print str(x)+','+str(y)
	#print HitDefs
	for name in W_HitDefs:
		X1,Y1,X2,Y2 = W_HitDefs[name] #Hit Area
		if X1<x<X2 and Y1<y<Y2: #are we in the hit area of this widget?
			if   W_Types[name]=='toggle':
				if not s: #make sure we update upon click-release
					W_States[name]=(False if W_States[name] else True)
			elif W_Types[name]=='button':
				if s: #Click
					W_States[name][0]=True
				if not s: #Release
					W_States[name][1]=True
				#leave the false-state changes up to the functions
	
def __CheckPos(x,y): #checks the new mouse position when moved
	pass 
