import bpy
import math
import os
import sys
import argparse
# NOTE: type in console: help(bpy.data.objects.get) !!!


DATA_DIR = None
RENDER_DIR = None
AXIS = None


def load_obj(name):
    file_loc = os.path.join(DATA_DIR, name)
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)


def load_ply(name):
    file_loc = os.path.join(DATA_DIR, name)
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc)


def clean_scene():
    for objkey, objvalue in bpy.data.objects.items():
        bpy.data.objects.remove(objvalue, do_unlink=True)


def initialize(camera_location, add_light=True):
    empty = bpy.data.objects.new("Empty", None)
    camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    bpy.context.scene.collection.objects.link(empty)
    bpy.context.scene.collection.objects.link(camera)
    # NOTE that z is height and y is depth !!
    camera.location = camera_location
    #camera.rotation_euler = (0, math.radians(30), math.radians(30))
    camera_constraint = camera.constraints.new('TRACK_TO')
    camera_constraint.target = empty
    if add_light:
        add_lightning()


def add_lightning():
    scene = bpy.context.scene
    lamp_data = bpy.data.lights.new(name="New Lamp", type='POINT')
    lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
    bpy.context.scene.collection.objects.link(lamp_object)
    lamp_object.location = (5.0, 5.0, 5.0)
    # bpy.context.view_layer.objects.active = lamp_object


def remove_obj():
    for objkey, objvalue in bpy.data.objects.items():
        if not 'Empty' in objkey and not 'Camera' in objkey:
            bpy.data.objects.remove(objvalue, do_unlink=True)
    assert len(bpy.context.scene.objects) == 1, 'ops?'
    assert len(bpy.data.objects) == 1, 'ops?'


def set_camera_around_point(center_x=0, center_y=0, camera_x=2, camera_y=2, camera_z=0, degrees=30):
    angle = math.radians(degrees)
    x = center_x+math.cos(angle)*(camera_x-center_x)-math.sin(angle)*(camera_y-center_y)
    y = center_y+math.sin(angle)*(camera_x-center_x)+math.cos(angle)*(camera_y-center_y)
    if AXIS == 'z':
        return (x, y, camera_z)
    else:
        return (x, camera_z, y)


def render(name, camera, d=30):
    (cx, cy, cz) = camera.location
    x_y_z = set_camera_around_point(camera_x=cx, camera_y=cy, camera_z=cz, degrees=d)
    camera.location = x_y_z
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    renderer = bpy.context.scene.render # or D.scenes[0].render
    #scale = renderer.resolution_percentage / 100
    #WIDTH = int(renderer.resolution_x * scale)
    #HEIGHT = int(renderer.resolution_y*scale)
    renderer.filepath = os.path.join(RENDER_DIR, "{}angle{}".format(name, d))
    bpy.ops.render.render(write_still=True)


def multi_view_render(name):
    clean_scene()
    if AXIS == 'z':
        initialize((2, 2, 0))
    else:
        initialize((2, 0, 2))
    if '.obj' in name:
        load_obj(name)
    elif '.ply' in name:
        load_ply(name)
    else:
        raise Exception('{} not supported'.format(name.split('.')[-1]))
    cam = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = cam
    bpy.context.scene.camera = cam
    for a in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]:
        render(name, cam, a)


def hide_objects(include_names=None):
    hide_all = True if include_names is None else False
    include_names = [] if include_names is None else include_names
    for objkey, objvalue in bpy.data.objects.items():
        hide = False
        for containing_str in include_names:
            if containing_str in objkey:
                hide = True
        # objvalue.hide_viewport = hide
        objvalue.hide_set(hide or hide_all)
        objvalue.hide_render = hide or hide_all


def show_objects(include_names=None):
    show_all = True if include_names is None else False
    include_names = [] if include_names is None else include_names
    for objkey, objvalue in bpy.data.objects.items():
        show = False
        for containing_str in include_names:
            if containing_str in objkey:
                show = True
        # objvalue.hide_viewport = hide
        objvalue.hide_set(not (show or show_all))
        objvalue.hide_render = show or show_all


def render_element(name):
    clean_scene()
    initialize((25, 25, 10))
    if '.obj' in name:
        load_obj(name)
    elif '.ply' in name:
        load_ply(name)
    else:
        raise Exception('{} not supported'.format(name.split('.')[-1]))
    # hide_objects()
    # show_objects(['Door'])
    cam = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = cam
    bpy.context.scene.camera = cam
    render(name, cam, 0)


def render_freestyle_on_white_background(name):
    clean_scene()
    initialize((5, 5, 1), False)
    if '.obj' in name:
        load_obj(name)
    elif '.ply' in name:
        load_ply(name)
    else:
        raise Exception('{} not supported'.format(name.split('.')[-1]))
    cam = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = cam
    bpy.context.scene.camera = cam
    bpy.context.scene.render.use_freestyle = True
    # a linestyle can be assigned to any line set
    freestyle_settings = bpy.context.scene.view_layers["View Layer"].freestyle_settings
    freestyle_settings.as_render_pass = True
    # lineset = freestyle_settings.linesets["LineSet"]
    # lineset.select_border = True
    # lineset.select_silhouette = True
    bpy.context.scene.use_nodes = True
    tree = bpy.data.scenes['Scene'].node_tree
    l = tree.links[0]
    tree.links.remove(l)
    Src = tree.nodes["Render Layers"]
    alphaover = tree.nodes.new("CompositorNodeAlphaOver")
    alphaover.inputs[1].default_value = (1, 1, 1, 1)
    Dst = tree.nodes["Composite"]
    tree.links.new(Src.outputs["Freestyle"], alphaover.inputs[2])
    tree.links.new(alphaover.outputs["Image"], Dst.inputs["Image"])
    bpy.context.scene.render.image_settings.file_format = 'BMP'
    render(name, cam, 0)


if __name__ == '__main__':

    if len(sys.argv)>=2:
        print("using command line arguments")
        parser = argparse.ArgumentParser()

        _, all_arguments = parser.parse_known_args()
        double_dash_index = all_arguments.index('--')
        script_args = all_arguments[double_dash_index + 1:]

        parser.add_argument('-dd', '--datadir')
        parser.add_argument('-rd', '--renderdir')
        parser.add_argument('-fn', '--filename')
        parser.add_argument('-a', '--axis', default='z')
        parser.add_argument('-i', '--include', default='')
        args, _ = parser.parse_known_args(script_args)

        DATA_DIR = args.datadir  # "/media/christina/Elements/ANNFASS_DATA/objs"
        RENDER_DIR = args.renderdir  # "/media/christina/Elements/ANNFASS_data/proj_style_out"
        AXIS = args.axis
        FILENAME = args.filename
    else:
        print("using default arguments")
        DATA_DIR = "/media/christina/Data/ANFASS_data/ANNFASS_Buildings/Byzantine architecture/02_Panagia Chrysaliniotissa/"
        DATA_DIR = "/media/christina/Elements/ANNFASS_DATA/buildnet_objs/objects_with_textures/"
        RENDER_DIR = "/media/christina/Data/ANNFASS_data/blender_render"
        AXIS = 'z'
        FILENAME = 'RESIDENTIALvilla_mesh3265Marios.ply'

    # multi_view_render(FILENAME)
    # bpy.context.space_data.shading.type = 'MATERIAL'
    # render_element(FILENAME)
    render_freestyle_on_white_background(FILENAME)

# export DATADIR /media/christina/Elements/ANNFASS_DATA/objs
# export RENDERDIR /media/christina/Elements/ANNFASS_data/proj_style_out
# export FILENAME  COMMERCIALcastle_mesh0365.ply
# blender --background --python preprocess_buildings/MultiCamerasRender.py -- --datadir ${DATADIR} \
#                                                                             --renderdir ${RENDERDIR} \
#                                                                             --filename ${FILENAME}
