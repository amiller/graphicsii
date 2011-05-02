import numpy as np

# I found the HDR images hard to work with, so I just downloaded the PFM versions.
# These are trivial to read.
# http://netpbm.sourceforge.net/doc/pfm.html

def load_pfm(filename):
	global buf
	with open(filename, 'rb') as f:
		
		idline = f.readline().strip()
		dims = [int(x) for x in f.readline().split()]
		scale = float(f.readline())
	
		arr = np.fromfile(f,np.float32)
		
		if idline == 'PF': return arr.reshape(dims + [3])
		elif idline == 'Pf': return arr.reshape(dims)

if __name__ == "__main__":
	p = load_pfm('data/probes/stpeters_probe.pfm')