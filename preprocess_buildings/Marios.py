import os
import numpy as np

def read_obj(obj_fn):
    """Read BuildNet obj with accompanied .mtl file
       Only diffuse parameter is specified -> rgb = kd

       Return:
               vertices: N x 3, numpy.ndarray(float)
               faces: M x 3, numpy.ndarray(int)
               face_color: M x 3, numpy.ndarray(float)
               face_normals: M x 3, numpy.ndarray(float)
               lines: K x 2, numpy.ndarray(int)
    """

    assert os.path.isfile(obj_fn)

    # Return variables
    vertices, faces, face_color, lines, vertex_normals = [], [], [], [], []

    with open(obj_fn, 'r') as f_obj:
        # Get .mtl file
        first_line = f_obj.readline().strip().split(' ')
        assert first_line[0] == 'mtllib', first_line[0]
        mtl_fn = first_line[1]
        assert mtl_fn[:-4] == obj_fn.split(os.sep)[-1][:-4], mtl_fn[:-4] + " == " + obj_fn.split(os.sep)[-1][:-4]
        assert os.path.isfile(os.path.join(os.path.dirname(obj_fn), mtl_fn)), os.path.join(os.path.dirname(obj_fn), mtl_fn)

        # Read material params
        diffuse_materials = {}
        with open(os.path.join(os.path.dirname(obj_fn), mtl_fn), 'r') as f_mtl:
            for line in f_mtl:
                line = line.strip().split(' ')
                if line[0] == 'newmtl':
                    assert len(line) == 2, line
                    mlt = line[1]
                if line[0] == 'Kd':
                    assert len(line) == 4, line
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
                # Face row
                assert len(line) == 4, line
                face_normal_ind = int(line[1].split('/')[-1])
                assert face_normal_ind == int(line[2].split('/')[-1])
                assert face_normal_ind == int(line[3].split('/')[-1])
                face_normal = vertex_normals[face_normal_ind-1]
                face = [float(line[1].split('/')[0]), float(line[2].split('/')[0]), float(line[3].split('/')[0]),
                        color[0], color[1], color[2],
                        face_normal[0], face_normal[1], face_normal[2]]
                faces.append(face)
            if line[0] == 'l':
                # Line row
                assert len(line) == 3
                l = [float(line[1]), float(line[2])]
                lines.append(l)

    vertices = np.vstack(vertices)
    faces = np.vstack(faces)
    face_color = faces[:, 3:6]
    face_normals = faces[:, 6:9]
    faces = faces[:, 0:3]
    lines = np.vstack(lines)

    return vertices, faces.astype(np.int32), face_color, face_normals, lines


def write_ply(ply_fn, vertices, faces, face_color, face_normals):
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

    if np.min(faces) == 1:
        faces -= 1

    with open(ply_fn, 'w') as f_ply:
        # Write header
        f_ply.write(header)

        # Write vertices
        for vertex in vertices:
            row = ' '.join([str(vertex[0]), str(vertex[1]), str(vertex[2])]) + '\n'
            f_ply.write(row)
        # Write faces + face_color
        for face_ind, face in enumerate(faces):
            color = face_color[face_ind]
            face_normal = face_normals[face_ind]
            row = ' '.join([str(len(face)), str(face[0]), str(face[1]), str(face[2]),
                            str(color[0]), str(color[1]), str(color[2]),
                            str(face_normal[0]), str(face_normal[1]), str(face_normal[2])]) + '\n'
            f_ply.write(row)


if __name__ == "__main__":

    filename = "/home/christina/Downloads/COMMERCIALcastle_mesh2985/COMMERCIALcastle_mesh2985.obj"

    # Read obj
    vertices, faces, face_color, face_normals, lines = read_obj(obj_fn=filename)

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
    write_ply(filename[:-4]+'Marios.ply', vertices, faces, face_color, face_normals)