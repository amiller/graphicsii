import pyglet
from pyglet.window import key
from OpenGL.GL import *
from OpenGL.GLU import *

from clrender import CLRender
from clrender import N

from glrender import GLRender

from molecule import Molecule
from pfmloader import load_pfm

class PDBWindow(pyglet.window.Window):
	
	use_cl = None
	
	angles = [0,0,0]
	scale = 1
	updated = False
	mol = None
	texId = None
	
	def on_draw(self):
		self.clear()
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		if not self.mol: return
		
		if self.use_cl:
			if self.updated:
				self.clrender.angles = self.angles
				self.clrender.scale = self.scale
				self.clrender.compute()
				self.updated = False
			self.clrender.render()
		else:
			self.glrender.angles = self.angles
			self.glrender.scale = self.scale
			self.glrender.render()
	
	def load_molecule(self, filename):
		# set the local molecule data
		self.mol = Molecule(filename)
		self.clrender.set_molecule(self.mol)
		self.glrender.set_molecule(self.mol)

	def load_envmap(self, filename):
		envmap = load_pfm(filename)
		self.clrender.set_envmap(envmap)
		self.glrender.set_envmap(envmap)

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE: 
			self.close()
		if symbol == key.C:
			self.use_cl = not self.use_cl
		if symbol == key.UP: 
			self.scale *= 1.414
		if symbol == key.DOWN:
			self.scale /= 1.414
		self.updated = True

	def on_resize(self, width, height):
		glViewport(0, 0, width, height)
		if (height == 0): height = 1
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90,float(width)/height,0.1, 100)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.angles[0] -= dy
		self.angles[1] += dx
		self.updated = True

	def __init__(self, *args, **kwargs):
		pyglet.window.Window.__init__(self, *args, **kwargs)
		
		self.glrender = GLRender()
		self.clrender = CLRender()

		
if __name__ == "__main__":
	w = PDBWindow(width=512,height=512)
	w.load_molecule('data/sugars/sucrose.pdb')
	#w.load_envmap('data/probes/campus_probe.pfm')
	w.load_envmap('data/probes/beach_probe.pfm')
	#w.load_envmap('data/probes/stpeters_probe.pfm')
	pyglet.app.run()
