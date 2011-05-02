import pyglet.gl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from shader import Shader
from molecule import Molecule

class GLRender(object):
	
	scale = 1
	angles = [0,0,0]
	mol = None
	envTex = None
	
	def __init__(self):
		# Setup the GLSL program
		with open('molgl.vert','r') as f:
			vert = f.readlines()
		with open('molgl.frag','r') as f:
			frag = f.readlines()
		self.shader = Shader(vert=vert, frag=frag)
		
		# Some parameters
		glEnable(GL_DEPTH_TEST)
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	
	def applySceneTransforms(self):
		gluLookAt(0, 0, 2*self.mol.radius, 0, 0, 0, 0, 1, 0); # Push molecule away from the origin along -Z direction.
		glScalef(self.scale,self.scale,self.scale);
		def mouse_rotate(xAngle, yAngle, zAngle):
			glRotatef(xAngle, 1.0, 0.0, 0.0);
			glRotatef(yAngle, 0.0, 1.0, 0.0);
			glRotatef(zAngle, 0.0, 0.0, 1.0);
		mouse_rotate(self.angles[0],self.angles[1],self.angles[2]);
		glTranslatef(-self.mol.x, -self.mol.y, -self.mol.z); # Bring molecue center to origin
		
	def set_molecule(self, mol):
		self.mol = mol
		
	def set_envmap(self, envmap):
		if self.envTex: glDeleteTextures(self.envTex)
		self.envTex = glGenTextures(1);
		glBindTexture(GL_TEXTURE_2D, self.envTex);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, envmap.shape[0], envmap.shape[1], 0, 
			GL_RGB, GL_FLOAT, envmap);
		glBindTexture(GL_TEXTURE_2D, 0);

	def render(self):
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.envTex)
		self.applySceneTransforms()
		self.shader.bind()
		#self.shader.uniformf('scale',self.scale)
		self.shader.uniformf('scale', 1)
		self.shader.uniformi('tex', 0)
		self.shader.uniformi('envMapping', 1)

		# Draw all the sphere
		for sphere in self.mol.spheres:
			glColor3f(sphere.r, sphere.g, sphere.b);
			glPushMatrix()
			glTranslatef(sphere.x, sphere.y, sphere.z);
			q = gluNewQuadric()
			gluSphere(q, sphere.radius,20,20)
			#glutSolidSphere(sphere.radius,20,20);
			glPopMatrix()
		self.shader.unbind()
		glBindTexture(GL_TEXTURE_2D, 0)
		glDisable(GL_TEXTURE_2D)
