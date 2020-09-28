import bpy
import math
import os

# NOTE: type in console: help(bpy.data.objects.get) !!!


DATA_DIR = "E:\ANNFASS_DATA\objs"
RENDER_DIR = "C:\\Users\\GraphicsLab\\Documents\\zavou_repositories\\dev\\blenderRelated"


def load_obj(name):
    name = 'example_commercial_hotel_mesh0215\COMMERCIALhotel_building_mesh0215.obj'
    file_loc = os.path.join(DATA_DIR, name)
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)


def clean_scene():
    for objkey, objvalue in bpy.data.objects.items():
        bpy.data.objects.remove(objvalue, do_unlink=True)


def initialize():
    empty = bpy.data.objects.new("Empty", None)
    camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    bpy.context.scene.collection.objects.link(empty)
    bpy.context.scene.collection.objects.link(camera)
    # NOTE that z is height and y is depth !!
    camera.location = (2, 2, 0)
    #camera.rotation_euler = (0, math.radians(30), math.radians(30))
    camera_constraint = camera.constraints.new('TRACK_TO')
    camera_constraint.target = empty


def remove_obj():
    for objkey, objvalue in bpy.data.objects.items():
        if not 'Empty' in objkey and not 'Camera' in objkey:
            bpy.data.objects.remove(objvalue, do_unlink=True)
    assert len(bpy.context.scene.objects) == 1, 'ops?'
    assert len(bpy.data.objects) == 1, 'ops?'


def set_camera_around_point(center_x=0, center_y=0, camera_x=2, camera_y=2, degrees=30):
    angle = math.radians(degrees)
    x = center_x+math.cos(angle)*(camera_x-center_x)-math.sin(angle)*(camera_y-center_y)
    y = center_y+math.sin(angle)*(camera_x-center_x)+math.cos(angle)*(camera_y-center_y)
    return (x, y, 0)


def render(camera, d=30):
    x_y_z = set_camera_around_point(degrees=d)
    camera.location = x_y_z
    renderer = bpy.context.scene.render # or D.scenes[0].render
    #scale = renderer.resolution_percentage / 100
    #WIDTH = int(renderer.resolution_x * scale)
    #HEIGHT = int(renderer.resolution_y*scale)
    renderer.filepath = os.path.join(RENDER_DIR, "angle{}.jpg".format(d))
    bpy.ops.render.render(write_still=True)


#camera.select_set(True)
#empty.select_set(True)


if __name__ == '__main__':
    
    clean_scene()
    initialize()
    load_obj('example_commercial_hotel_mesh0215\COMMERCIALhotel_building_mesh0215.obj')
    cam = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = cam
    bpy.context.scene.camera = cam
    for a in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]:
        render(cam, a)
