
import os


def get_obj_list(folder, out_file):
    with open(out_file, "w") as f_out:
        for filename in os.listdir(folder):
            if ".obj" in filename:
                f_out.write(os.path.join(folder, filename) + "\n")


if __name__ == '__main__':
    get_obj_list(
        "/media/christina/Elements/ANNFASS_DATA/buildnet_objs/objects_with_textures",
        "/media/christina/Elements/ANNFASS_SOLUTION/proj_style_data/rtsc_in/buildnet/obj_list.txt"
    )
