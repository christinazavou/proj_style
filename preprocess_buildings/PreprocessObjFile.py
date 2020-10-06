import os
import numpy as np


def read_materials(folder, mtl_fn):
	materials = {}
	with open(os.path.join(folder, mtl_fn), 'r') as f_mtl:
		for line in f_mtl:
			line = line.strip().split(' ')
			if line[0] == 'newmtl':
				assert (len(line) == 2)
				mlt = line[1]
			elif line[0] == 'Kd':
				assert (len(line) == 5) or (len(line) == 4)
				rgb = np.array([float(line[1]), float(line[2]), float(line[3])], dtype=np.float32)
				materials[mlt] = rgb
			else:
				continue
	return materials

				
def read_obj(folder, obj_fn):
	"""Read BuildNet obj with accompanied .mtl file
	   Only diffuse parameter is specified in the material file (Kd r g b)

	   Return:
	   		vertices: N x 3, numpy.ndarray(float)
	   		faces: M x 3, numpy.ndarray(int)
	   		face_color: M x 3, numpy.ndarray(float)
	   		face_normals: M x 3, numpy.ndarray(float)
	   		lines: K x 2, numpy.ndarray(int)
	"""

	assert(os.path.isfile(os.path.join(folder, obj_fn)))

	# Return variables
	vertices, faces, face_color, lines, vertex_normals = [], [], [], [], []

	with open(os.path.join(folder, obj_fn), 'r') as f_obj:
		# Get .mtl file
		first_line = f_obj.readline().strip().split(' ')
		if first_line[0] == "#":
			f_obj.readline()
			first_line = f_obj.readline().strip().split(' ')
		assert(first_line[0] == 'mtllib')
		mtl_fn = first_line[1]
		assert(mtl_fn[:-4] == obj_fn[:-4])
		assert(os.path.isfile(os.path.join(folder, mtl_fn)))

		# Read material params
		diffuse_materials = read_materials(folder, mtl_fn)

		# Read obj geometry
		for line in f_obj:
			line = line.strip().split(' ')
			if line[0] == 'v':
				# Vertex row
				assert(len(line) == 4)
				vertex = [float(line[1]), float(line[2]), float(line[3])]
				vertices.append(vertex)
			if line[0] == 'vn':
				# Vertex normal row
				assert (len(line) == 4)
				vn = [float(line[1]), float(line[2]), float(line[3])]
				vertex_normals.append(vn)
			if line[0] == 'usemtl':
				# Material row
				assert(len(line) == 2)
				color = diffuse_materials[line[1]]
			if line[0] == 'f':

				# assert(len(line) == 4)
				# face_normal_ind = int(line[1].split('/')[-1])
				# # assert(face_normal_ind == int(line[2].split('/')[-1]))
				# # assert(face_normal_ind == int(line[3].split('/')[-1]))
				# face_normal = vertex_normals[face_normal_ind-1]
				# face = [float(line[1].split('/')[0]), float(line[2].split('/')[0]), float(line[3].split('/')[0]),
				# 		color[0], color[1], color[2],
				# 		face_normal[0], face_normal[1], face_normal[2]]
				# faces.append(face)


				v1, vt1, vn1 = line[1].split('/')
				v2, vt2, vn2 = line[2].split('/')
				v3, vt3, vn3 = line[3].split('/')

				face = [float(v1), float(v2), float(v3),
						color[0], color[1], color[2],
						# we ignore texture, we only use colour (you could use vertex_textures)
						vertex_normals[int(vn1) - 1], vertex_normals[int(vn2) - 1], vertex_normals[int(vn3) - 1]]
				faces.append(face)

			if line[0] == 'l':
				# Line row
				assert(len(line) == 3)
				l = [float(line[1]), float(line[2])]
				lines.append(l)

	vertices = np.vstack(vertices)
	faces = np.vstack(faces)
	face_color = faces[:, 3:6]
	face_normals = faces[:, 6:9]
	faces = faces[:, 0:3]
	# lines = np.vstack(lines)

	return vertices, faces.astype(np.int32), face_color, face_normals, lines


def faces_indices_with_index_0(faces):
	if np.min(faces) == 1:
		faces -= 1
	return faces


def write_ply(folder, ply_fn, vertices, faces, face_color, face_normals):
	'''Write shape in .ply with face color information

	   Return:
	   		None
	'''

	# Create header
	header = 'ply\n' \
			 'format ascii 1.0\n' \
			 'element vertex ' + str(len(vertices)) + '\n' \
			 'property float x\n' \
			 'property float y\n' \
			 'property float z\n' \
			 'element face ' + str(len(faces)) + '\n' \
			 'property list uchar int vertex_indices\n' \
			 'property float red\n' \
			 'property float green\n' \
			 'property float blue\n' \
			 'property float nx\n' \
			 'property float ny\n' \
			 'property float nz\n' \
			 'end_header\n'

	faces = faces_indices_with_index_0(faces)

	def write_vertices():
		[f_ply.write(' '.join([str(v[0]), str(v[1]), str(v[2])]) + '\n') for v in vertices]

	def write_faces_with_colours_and_normals():
		for face_ind, face in enumerate(faces):
			color = face_color[face_ind]
			face_normal = face_normals[face_ind]
			row = ' '.join([
				str(len(face)),
				str(face[0]), str(face[1]), str(face[2]),
				str(color[0]), str(color[1]), str(color[2]),
				str(face_normal[0]), str(face_normal[1]), str(face_normal[2])]) + '\n'
			f_ply.write(row)

	with open(os.path.join(folder, ply_fn), 'w') as f_ply:
		f_ply.write(header)
		write_vertices()
		write_faces_with_colours_and_normals()


def re_align_faces_based_on_normals(vertices, faces, face_normals):
	edge_0 = vertices[faces[:, 1]] - vertices[faces[:, 0]]
	edge_1 = vertices[faces[:, 2]] - vertices[faces[:, 0]]
	normals = np.cross(edge_0, edge_1)
	normals /= np.linalg.norm(normals)
	normal_angles = np.rad2deg(np.arccos(np.einsum('ij,ij->i', normals, face_normals)))
	for angle_ind, angle in enumerate(normal_angles):
		if angle > 90:
			v1 = faces[angle_ind, 1]
			v2 = faces[angle_ind, 2]
			faces[angle_ind, 1] = v2
			faces[angle_ind, 2] = v1
	return faces


if __name__ == "__main__":

	# _filename = "COMMERCIALcastle_mesh2985.obj"
	# _folder = "/media/christina/Elements/ANNFASS_DATA/objs/buildnet_example/COMMERCIALcastle_mesh2985"
	# _filename = "RESIDENTIALhouse_mesh3059.obj"
	# _folder = "/media/christina/Elements/ANNFASS_DATA/objs/buildnet_example/RESIDENTIALhouse_mesh3059"
	# _filename = "28_Stavrou_Economou_Building_01.obj"
	# _folder = "/media/christina/Elements/ANNFASS_DATA/objs/withStyle/28_Stavrou_Economou_Building"
	_filename = "29_Lefkaritis_Building_01.obj"
	_folder = "/media/christina/Elements/ANNFASS_DATA/objs/withStyle/29_Lefkaritis_Building"

	# Read obj
	_vertices, _faces, _face_color, _face_normals, _lines = read_obj(_folder, _filename)
	_faces = faces_indices_with_index_0(_faces)
	# _faces = re_align_faces_based_on_normals(_vertices, _faces, _face_normals)

	# Write ply
	write_ply(_folder, _filename[:-4]+'MY.ply', _vertices, _faces, _face_color, _face_normals)
