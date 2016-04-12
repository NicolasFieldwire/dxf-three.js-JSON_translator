import math
import numpy as np

def end_three():
	file = open("three_3d.txt",'a')
	file.write('\n		);\n		scene.add( line );\n\n')

def write_three(x, y, z, b):

	if z != 0:
		new_point = transpose(x,y)

		x = new_point[0]
		y = new_point[1]
		z = new_point[2]

		a = 'new_point = ' + str(new_point)
		print a

	file = open("three_3d.txt",'a')
	file.write('			new THREE.Vector3( '+ str(x) + ', ' + str(y) + ', ' + str(z) + '),\n')

def start_three(asset_count):

	file = open("three_3d.txt",'a')
	file.write('// asset ' + str(asset_count) + '\n\n')
	file.write('		geometry.vertices.push(\n\n')

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

def transpose(old_x, old_y):
	xWCS = [1, 0, 0]
	yWCS = [0, 1, 0]
	zWCS = [0, 0, 1]
	N = [0.7071067811865472, -0.7071067811865479, 0.0]

	if math.sqrt(math.pow(N[0], 2)) < 1/64 and math.sqrt(math.pow(N[1], 2)) < 1/64:
		Ax = cross(yWCS, N)
	else:
		Ax = cross(zWCS, N)

	Ay = cross(N, Ax)

	print Ax
	print Ay

	# build new co-ord system matrix
	new_coord_sys = [Ax, Ay, N]
	# new_coord_sys = [[0, 0, 1], [0, 1, 0], [2, 0, 0]]

	print new_coord_sys
	
	# find inverse co-ord system as transfer matrix
	INV_new_coord_sys = np.linalg.inv(new_coord_sys)
	print INV_new_coord_sys

	point2 = np.dot(INV_new_coord_sys, np.dot([xWCS, yWCS, zWCS], [old_x, old_y, 0]))
	print point2

	return point2

def import_scan():

	# overwrite old three.txt file
	file = open("three_3d.txt",'w')
	file.close

	asset_count = 1

	import_list = open("test3d.dxf").readlines()
	print len(import_list)
	# remove all \n from strings
	for n, i in enumerate(import_list):
		if "\n" in i:
			import_list[n] = i.replace('\n','')

	# start scaning list for lines and stuff.
	for n, i in enumerate(import_list):

		if "POLYLINE" in i:

			# write first lines for a new part
			start_three(asset_count)
			asset_count += 1

			# find index of next 'seqend' to find end of polyline feature
			p_end = 0
			p_add = 1
			p_boo = False
			while p_boo == False:
				if "SEQEND" in import_list[n + p_add]:
					p_end = n + p_add
					p_boo = True
				p_add += 1

			# print import_list[p_end]
			# print n
			# print p_end

			for polyline_ind in range(n, p_end):

				if "VERTEX" in import_list[polyline_ind]:

					# get index of next vertex or sequend to get indiv vertex feature
					v_end = 0
					v_add = 1
					v_boo = False

					while v_boo == False:
						if "VERTEX" in import_list[polyline_ind + v_add] or "SEQEND" in import_list[polyline_ind + v_add]:
							v_end = polyline_ind + v_add
							v_boo = True
						v_add += 1

					for v in range(polyline_ind, v_end):
						if "10" in import_list[v] and \
							"20" in import_list[v + 2] and \
							"30" in import_list[v + 4]: # and \
							#"42" in import_list[v + 6]:

							x = float(import_list[v + 1])
							y = float(import_list[v + 3])
							z = float(import_list[v + 5])
							#bulge = float(import_list[v + 7])
							bulge = 0.0

							print x
							print y
							print z
							print bulge

							write_three(x, y, z, bulge)
						
						# if "10" in import_list[v] and "20" in import_list[v + 2]:
						# 	print "10 " + import_list[v + 1]
						# if "20" in import_list[v] and "30" in import_list[v + 2]:
						# 	print "20 " + import_list[v + 1]
						# if "42" in import_list[v] and "0" in import_list[v + 2]:
						#	print "42 " + import_list[v + 1]


			# write first lines for a new part
			# end_three()

if __name__ == '__main__':
	import_scan()

# if __name__ == '__main__':
# 	print 'This program is being run by itself'
# else:
# 	print 'I am being imported from another module'