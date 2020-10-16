from PIL import Image
import os
from shutil import copyfile


folder_of_rtsc_out = "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_out/rtsc_out/buildnet"
folder_for_3dlines = "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_out/rtsc_out/bmp/buildnet/3dlines"
folder_of_models = "/media/christina/Elements/ANNFASS_DATA/buildnet_objs/objects_with_textures"
folder_for_models = "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_out/rtsc_out/bmp/buildnet/models"
if not os.path.exists(folder_for_3dlines):
    os.makedirs(folder_for_3dlines)
if not os.path.exists(folder_for_models):
    os.makedirs(folder_for_models)

lines = 0
mod = 0
for model_name in os.listdir(folder_of_rtsc_out):
    if "Marios" in model_name:
        continue
    mod+=1
    print("model ", model_name)
    for path in os.listdir(os.path.join(folder_of_rtsc_out, model_name)):
        lines+=1
        ppmimg=os.path.join(folder_of_rtsc_out, model_name, path)
        bmpimg=os.path.join(folder_for_3dlines, str(lines) + ".bmp")
        Image.open(ppmimg).save(bmpimg)
        obj_path = os.path.join(folder_of_models, model_name.replace("PlainMesh", ".obj"))
        copyfile(obj_path, os.path.join(folder_for_models, model_name+str(mod)+".obj"))

