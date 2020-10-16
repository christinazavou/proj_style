import os
import numpy as np

def read_obj(obj_fn):
    """Read BuildNet obj with accompanied .mtl file
       Only diffuse parameter is specified -> rgb = kd

       Return:
               vertices: N x 3, numpy.ndarray(float)
               faces: M x 3, numpy.ndarray(int)
               face_normals: M x 3, numpy.ndarray(float)
    """

    assert os.path.isfile(obj_fn)

    # Return variables
    vertices, faces, vertex_normals = [], [], []

    with open(obj_fn, 'r') as f_obj:
        # Get .mtl file
        first_line = f_obj.readline()
        while first_line[0] == "#" or first_line.strip() == '':
            first_line = f_obj.readline()
        first_line = first_line.strip().split('mtllib ')

        assert first_line[0] == '', first_line
        mtl_fn = first_line[1]
        mtl_filename = mtl_fn.split(os.sep)[-1]
        dir_name = os.path.dirname(obj_fn)
        assert os.path.isfile(os.path.join(dir_name, mtl_filename)), os.path.join(dir_name, mtl_filename)

        # Read material params
        diffuse_materials = {}
        with open(os.path.join(os.path.dirname(obj_fn), mtl_fn), 'r') as f_mtl:
            for line in f_mtl:
                line = line.strip().split(' ')
                if line[0] == 'newmtl':
                    assert len(line) == 2, line
                    mlt = line[1]
                if line[0] == 'Kd':
                    assert len(line) == 4 or len(line) == 5, line
                    rgb = np.array([float(line[1]), float(line[2]), float(line[3])], dtype=np.float32)
                    diffuse_materials[mlt] = rgb

        # Read obj geometry
        for line in f_obj:
            line = line.strip().split(' ')
            if line[0] == 'v':
                # Vertex row
                assert len(line) == 4, line
                vertex = [float(line[1]), float(line[2]), float(line[3])]
                vertices.append(vertex)
            if line[0] == 'vn':
                # Vertex normal row
                assert len(line) == 4, line
                vn = [float(line[1]), float(line[2]), float(line[3])]
                vertex_normals.append(vn)
            if line[0] == 'usemtl':
                # Material row
                assert len(line) == 2, line
                color = diffuse_materials[line[1]]
            if line[0] == 'f':

                # from here i can generate one new vertex with this colour .. i.e. duplicate vertices

                # Face row
                assert len(line) == 4, line
                face_normal_ind1 = int(line[1].split('/')[-1])
                face_normal_ind2 = int(line[2].split('/')[-1])
                face_normal_ind3 = int(line[3].split('/')[-1])
                face_normal1 = vertex_normals[face_normal_ind1-1]
                face_normal2 = vertex_normals[face_normal_ind2-1]
                face_normal3 = vertex_normals[face_normal_ind3-1]
                face_normal = np.mean([face_normal1, face_normal2, face_normal3], axis=0)
                face = [float(line[1].split('/')[0]), float(line[2].split('/')[0]), float(line[3].split('/')[0]),
                        face_normal[0], face_normal[1], face_normal[2]]
                faces.append(face)

    vertices = np.vstack(vertices)
    faces = np.vstack(faces)
    face_normals = faces[:, 3:6]
    faces = faces[:, 0:3]

    return vertices, faces.astype(np.int32), face_normals


def write_ply(ply_fn, vertices, faces, face_normals):
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
                  'property float nx\n' \
                  'property float ny\n' \
                  'property float nz\n' \
             'end_header\n'

    if np.min(faces) == 1:
        faces -= 1

    with open(ply_fn, 'w') as f_ply:
        # Write header
        f_ply.write(header)

        # Write vertices
        for vertex in vertices:
            row = ' '.join([str(vertex[0]), str(vertex[1]), str(vertex[2])]) + '\n'
            f_ply.write(row)
        # Write faces
        for face_ind, face in enumerate(faces):
            face_normal = face_normals[face_ind]
            row = ' '.join([str(len(face)), str(face[0]), str(face[1]), str(face[2]),
                            str(face_normal[0]), str(face_normal[1]), str(face_normal[2])]) + '\n'
            f_ply.write(row)


if __name__ == "__main__":

    filename = "/media/christina/Elements/ANNFASS_DATA/buildings_with_style_objs/28_Stavrou Economou Building/28_Stavrou Economou Building_01.obj"
    filename = "/media/christina/Elements/ANNFASS_DATA/buildings_with_style_objs/29_Lefkaritis Building/29_Lefkaritis Building_01/29_Lefkaritis Building_01.obj"
    filename = "/media/christina/Elements/ANNFASS_DATA/buildings_with_style_objs/30_Nicolaou Building/30_Nicolaou Building_01.obj"
    filename = "/media/christina/Elements/ANNFASS_DATA/buildings_without_style_objs/09_Ayios Michael Tripiotis/09_Ayios Michael Tripiotis_01_tri.obj"
    filename = "/media/christina/Elements/ANNFASS_DATA/buildings_without_style_objs/13_Kyrenia Gate/13_Kyrenia Gate_01_tri_sub.obj"

    # Read obj
    vertices, faces, face_normals = read_obj(obj_fn=filename)

    # Re-align faces based on face normals
    if np.min(faces) == 1:
        faces -= 1
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

    # Write ply
    write_ply(filename[:-4]+'Marios.ply', vertices, faces, face_normals)