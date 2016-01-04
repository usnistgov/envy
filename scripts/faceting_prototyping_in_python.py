import matplotlib.pyplot as plt, numpy as np

"""
A little script in python for prototyping generation of facets and vertices in JS
"""

def ij_to_index(i, j, Nj):
	""" Convert i,j pair into index if vertex """
	return j + Nj*i

def mesh_to_facets(X, Y, Z):

	assert(isinstance(X,list))
	assert(isinstance(Y,list))
	assert(isinstance(Z,list))
	N1 = len(X)
	if N1 == 0:
		raise ValueError('X cannot be empty')
	N2 = len(X[0])

	assert(len(Y) == N1)
	assert(len(Z) == N1)
	vertices = []
	facets = []
	for i in range(N1):
		assert(isinstance(X[i],list))
		assert(isinstance(Y[i],list))
		assert(isinstance(Z[i],list))
		assert(len(X[i])  == N2)
		assert(len(X[i])  == N2)
		assert(len(X[i])  == N2)

		for j in range(N2):
			vertices += [X[i][j], Y[i][j], Z[i][j]]
			if j < N2-1 and i < N1-1:
				# triangle one
				t1_indices = [ij_to_index(i,j,N2), ij_to_index(i+1,j, N2), ij_to_index(i,j+1, N2)]
				# triangle two indices
				t2_indices = [ij_to_index(i+1,j,N2), ij_to_index(i+1,j+1, N2), ij_to_index(i,j+1, N2)	]
				facets += t1_indices
				facets += t2_indices

	return vertices, facets

def do_plot(vertices, facets):
	n = 3
	xx, yy, zz = zip(*[vertices[i:i+n] for i in xrange(0, len(vertices), n)])

	for triangle in [facets[i:i+4] for i in xrange(0, len(facets), 4)]:
		indices = triangle[0:3] + [triangle[0]]
		x = [vertices[3*i] for i in indices]
		y = [vertices[3*i+1] for i in indices]
		z = [vertices[3*i+2] for i in indices]
		plt.fill(x, y)

	plt.plot(xx, yy, 'o')
	plt.show()

def sines_data_example():
	NX = 500
	NY = 300
	x = np.linspace(0, 2*np.pi, NX)
	y = np.linspace(0, 2*np.pi, NY)

	X,Y = np.meshgrid(x,y)
	Z = np.sin(X/2)*np.sin(Y)

	vertices, facets = mesh_to_facets((X*10).tolist(), (Y*10).tolist(), (Z*10).tolist())

	import json
	with open('sines.json','w') as fp:
		json.dump([dict(vertices = vertices, facets = facets)], fp, indent = 2)

def water_viscosity_example():
	NX = 300
	NY = 300
	T = np.linspace(300, 900, NX)
	P = np.logspace(np.log10(1e3), np.log10(1e8), NY)
	TT, PP = np.meshgrid(T, P)
	del T, P
	MU = np.zeros_like(TT)
	import CoolProp
	for i in range(TT.shape[0]):
		for j in range(TT.shape[1]):
			MU[i,j] = CoolProp.CoolProp.PropsSI("V", "T", TT[i,j], "P", PP[i,j], "Water")

	vertices, facets = mesh_to_facets((TT/4.0).tolist(), (np.log(PP)*10).tolist(), (np.log(MU)*75).tolist())

	print len(vertices), len(facets)
	import json
	with open('water_viscosity.json','w') as fp:
		json.dump([dict(vertices = vertices, facets = facets)], fp, indent = 2)

if __name__=='__main__':
	sines_data_example()
	water_viscosity_example()