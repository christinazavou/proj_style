from PIL import Image
import os


folder_of_rtsc_out = "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_out/rtsc_out/buildnet"
folder_of_rtsc_out_bmp = "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_out/rtsc_out/bmp/buildnet"

if not os.path.exists(folder_of_rtsc_out_bmp):
    os.makedirs(folder_of_rtsc_out_bmp)

for model_name in os.listdir(folder_of_rtsc_out):
    if "Marios" in model_name:
        continue
    for path in os.listdir(os.path.join(folder_of_rtsc_out, model_name)):
        ppmimg=os.path.join(folder_of_rtsc_out, model_name, path)
        bmpimg=os.path.join(folder_of_rtsc_out_bmp, model_name, path.replace(".ppm", ".bmp"))
        if not os.path.exists(os.path.join(folder_of_rtsc_out_bmp, model_name)):
            os.makedirs(os.path.join(folder_of_rtsc_out_bmp, model_name))
        Image.open(ppmimg).save(bmpimg)
