from Bio.PDB.PDBParser import PDBParser
import string
import numpy as np
import struct

# This file parses the PDB files using the parser in biopython. It also
# uses the element color and radius table borrowed from the original assignment.

class Sphere(object):
	x,y,z = 0,0,0
	radius = 1.5
	r,g,b,a = 0,0,0,255

class Molecule(object):
	
	radius = 0
	spheres = []
	
	def __init__(self, filename):
		
		self.spheredata = ''
		
		E2C = {}
		E2R = {}
		exec elements # Read the color mappings at the bottom of this file
		
		# Read the file
		atoms = []
		parser = PDBParser()
		structure = parser.get_structure('test',filename)
		for model in structure.get_list():
		  for chain in model.get_list():
		    for residue in chain.get_list():
		      for atom in residue.get_list():
						atoms += [atom]
		
		# Look up colors and radius
		spheres = []
		for atom in atoms:
			s = Sphere()
			s.x, s.y, s.z = atom.get_coord()
			element = atom.get_name().strip(string.digits)
			s.radius = E2R[element] if E2R.has_key(element) else 1.5
			color = E2C[element] if E2C.has_key(element) else 0xFF1493
			s.r = (color & 0xff) / 255.0
			s.g = ((color & 0xff00) >> 8) / 255.0
			s.b = ((color & 0xff0000) >> 16) / 255.0
			spheres += [s]
			
			self.spheredata += struct.pack('fff f ffff', s.x,s.y,s.z, s.radius, s.r,s.g,s.b,1.0)
			
			
		self.spheres = spheres

		# Figure out the total radius
		xs, ys, zs = [s.x for s in spheres], [s.y for s in spheres], [s.z for s in spheres]
		dx = max(xs) - min(xs)
		dy = max(ys) - min(ys)
		dz = max(zs) - min(zs)
		self.radius = np.sqrt(dx*dx + dy*dy + dz*dz) / 2 + 1.5
		self.x = (max(xs) + min(xs)) / 2
		self.y = (max(ys) + min(ys)) / 2
		self.z = (max(zs) + min(zs)) / 2

elements = """
# I filtered these lines of code using the regular expression /\*.*?\*/ which 
# got rid of the C-style comments 
E2C["H"] =  0xFFFFFF  	  	;
E2C["HE"]=  0xFFC0CB  	  	;
E2C["LI"]=  0xB22222  	  	;
E2C["BE"]=  0xFF1493  	  	;
E2C["B"] =  0x00FF00  	  	;
E2C["C"] =  0x808080  	  	;
E2C["N"] =  0x8F8FFF  	  	;
E2C["O"] =  0xF00000  	  	;
E2C["F"] =  0xDAA520  	  	;
E2C["NE"]=  0xFF1493  	  	;
E2C["NA"]=  0x0000FF  	  	;
E2C["MG"]=  0x228B22  	  	;
E2C["AL"]=  0x808090  	  	;
E2C["SI"]=  0xDAA520  	  	;
E2C["P"] =  0xFFA500  	  	;
E2C["S"] =  0xFFC832  	  	;
E2C["CL"]=  0x00FF00  	  	;
E2C["AR"]=  0xFF1493  	  	;
E2C["K"] =  0xFF1493  	  	;
E2C["CA"]=  0x808090  	  	;
E2C["SC"]=  0xFF1493  	  	;
E2C["TI"]=  0x808090  	  	;
E2C["V"] =  0xFF1493  	  	;
E2C["CR"]=  0x808090  	  	;
E2C["MN"]=  0x808090  	  	;
E2C["FE"]=  0xFFA500  	  	;
E2C["CO"]=  0xFF1493  	  	;
E2C["NI"]=  0xA52A2A  	  	;
E2C["CU"]=  0xA52A2A  	  	;
E2C["ZN"]=  0xA52A2A  	  	;
E2C["GA"]=  0xFF1493  	  	;
E2C["GE"]=  0xFF1493  	  	;
E2C["AS"]=  0xFF1493  	  	;
E2C["SE"]=  0xFF1493  	  	;
E2C["BR"]=  0xA52A2A  	  	;
E2C["KR"]=  0xFF1493  	  	;
E2C["RB"]=  0xFF1493  	  	;
E2C["SR"]=  0xFF1493  	  	;
E2C["Y"] =  0xFF1493  	  	;
E2C["ZR"]=  0xFF1493  	  	;
E2C["NB"]=  0xFF1493  	  	;
E2C["MO"]=  0xFF1493  	  	;
E2C["TC"]=  0xFF1493  	  	;
E2C["RU"]=  0xFF1493  	  	;
E2C["RH"]=  0xFF1493  	  	;
E2C["PD"]=  0xFF1493  	  	;
E2C["AG"]=  0x808090  	  	;
E2C["CD"]=  0xFF1493  	  	;
E2C["IN"]=  0xFF1493  	  	;
E2C["SN"]=  0xFF1493  	  	;
E2C["SB"]=  0xFF1493  	  	;
E2C["TE"]=  0xFF1493  	  	;
E2C["I"] =  0xA020F0  	  	;
E2C["XE"]=  0xFF1493  	  	;
E2C["CS"]=  0xFF1493  	  	;
E2C["BA"]=  0xFFA500  	  	;
E2C["LA"]=  0xFF1493  	  	;
E2C["CE"]=  0xFF1493  	  	;
E2C["PR"]=  0xFF1493  	  	;
E2C["ND"]=  0xFF1493  	  	;
E2C["PM"]=  0xFF1493  	  	;
E2C["SM"]=  0xFF1493  	  	;
E2C["EU"]=  0xFF1493  	  	;
E2C["GD"]=  0xFF1493  	  	;
E2C["TB"]=  0xFF1493  	  	;
E2C["DY"]=  0xFF1493  	  	;
E2C["HO"]=  0xFF1493  	  	;
E2C["ER"]=  0xFF1493  	  	;
E2C["TM"]=  0xFF1493  	  	;
E2C["YB"]=  0xFF1493  	  	;
E2C["LU"]=  0xFF1493  	  	;
E2C["HF"]=  0xFF1493  	  	;
E2C["TA"]=  0xFF1493  	  	;
E2C["W"] =  0xFF1493  	  	;
E2C["RE"]=  0xFF1493  	  	;
E2C["OS"]=  0xFF1493  	  	;
E2C["IR"]=  0xFF1493  	  	;
E2C["PT"]=  0xFF1493  	  	;
E2C["AU"]=  0xDAA520  	  	;
E2C["HG"]=  0xFF1493  	  	;
E2C["TL"]=  0xFF1493  	  	;
E2C["PB"]=  0xFF1493  	  	;
E2C["BI"]=  0xFF1493  	  	;
E2C["PO"]=  0xFF1493  	  	;
E2C["AT"]=  0xFF1493  	  	;
E2C["RN"]=  0xFF1493  	  	;
E2C["FR"]=  0xFF1493  	  	;
E2C["RA"]=  0xFF1493  	  	;
E2C["AC"]=  0xFF1493  	  	;
E2C["TH"]=  0xFF1493  	  	;
E2C["PA"]=  0xFF1493  	  	;
E2C["U"] =  0xFF1493  	  	;
E2C["NP"]=  0xFF1493  	  	;
E2C["PU"]=  0xFF1493  	  	;
E2C["AM"]=  0xFF1493  	  	;
E2C["CM"]=  0xFF1493  	  	;
E2C["BK"]=  0xFF1493  	  	;
E2C["CF"]=  0xFF1493  	  	;
E2C["ES"]=  0xFF1493  	  	;
E2C["FM"]=  0xFF1493  	  	;
E2C["MD"]=  0xFF1493  	  	;
E2C["NO"]=  0xFF1493  	  	;
E2C["LR"]=  0xFF1493  	  	;
E2C["RF"]=  0xFF1493  	  	;
E2C["DB"]=  0xFF1493  	  	;
E2C["SG"]=  0xFF1493  	  	;
E2C["BH"]=  0xFF1493  	  	;
E2C["HS"]=  0xFF1493  	  	;
E2C["MT"]=  0xFF1493  	  	;

E2R["F"]= 	1.47
E2R["CL"]= 	1.89
E2R["H"]=   1.100 
E2R["C"]=   1.548
E2R["N"]=   1.400
E2R["O"]=   1.348
E2R["P"]=   1.880
E2R["S"]= 	1.808
E2R["CA"]= 	1.948
E2R["FE"]= 	1.948
E2R["ZN"]= 	1.148
E2R["I"]= 	1.748
"""