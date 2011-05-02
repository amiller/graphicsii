from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from clrender import CLRender
from clrender import N

from glrender import GLRender

class GlutWindow(object):
	
	updated = False
	use_cl = False
	texId = None
	scale = 1
	angles = [0,0,0]
	oldx = 0 
	oldy = 0
	
	def __init__(self):
		self.glrender = GLRender()
		self.clrender = CLRender()
		self.create_texture()
		
	def reshape(self, width, height):
		glViewport(0, 0, width, height)
		if (height == 0): height = 1
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90,float(width)/height,0.1, 100)

	def keyboard(self, key, x, y):
		if key == chr(27): quit()
		if key == 'c': self.use_cl = not self.use_cl
		if key == 'w': self.scale *= 1.414
		if key == 's': self.scale /= 1.414
		self.updated = True
		glutPostRedisplay()
		
	def display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		if not self.mol: return
		
		if self.use_cl:
			if self.updated:
				self.clrender.angles = self.angles
				self.clrender.scale = self.scale
				self.clrender.compute()
				glBindTexture(GL_TEXTURE_2D, self.texId)
				glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, N, N, GL_RGBA, GL_UNSIGNED_BYTE, self.clrender.dst)
				self.updated = False
				
			glBindTexture(GL_TEXTURE_2D, self.texId)
			glEnable(GL_TEXTURE_2D)
			glBegin(GL_QUADS)
			glTexCoord2f( 0.0, 0.0 ); glVertex3f( -1.0, -1.0, -1.0 )
			glTexCoord2f( 0.0, 1.0 );	glVertex3f( -1.0, 1.0, -1.0 )
			glTexCoord2f( 1.0, 1.0 ); glVertex3f( 1.0, 1.0, -1.0 )
			glTexCoord2f( 1.0, 0.0 ); glVertex3f( 1.0, -1.0, -1.0 )
			glEnd()
			glDisable(GL_TEXTURE_2D)
		else:
			self.glrender.angles = self.angles
			self.glrender.scale = self.scale
			self.glrender.render()
		glutSwapBuffers()

	def load_molecule(self, filename):
		# set the local molecule data
		self.clrender.load_molecule(filename)
		self.mol = self.glrender.mol = self.clrender.mol

	def create_texture(self):    
		self.texId = glGenTextures(1);
		glBindTexture(GL_TEXTURE_2D, self.texId);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, N, N, 0, GL_RGBA, GL_UNSIGNED_BYTE, None);
		glBindTexture(GL_TEXTURE_2D, 0);


if __name__ == "__main__":

	glutInit(len(sys.argv), sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(512, 512)
	glutCreateWindow('PDB Viewer')
	
	window = GlutWindow()
	window.load_molecule('sugars/sucrose.pdb')
	window.reshape(512,512)
	glutReshapeFunc(window.reshape)
	glutDisplayFunc(window.display)
	glutKeyboardFunc(window.keyboard)

	glutMainLoop()



