input_folder=/media/christina/Elements/ANNFASS_DATA/objs/objects_with_textures
output_folder=/media/christina/Elements/ANNFASS_DATA/objs/objects_without_textures

remove_materials(){
  obj_file=$1
  echo "Cleaning obj_file ..."
  sed '/usemtl/,+1 d' < ${input_folder}/${obj_file} > ${output_folder}/${obj_file}
}

if [ -d "${output_folder}" ]
then
    echo "Directory ${output_folder} exists."
else
    mkdir ${output_folder}
    echo "Directory ${output_folder} created."
fi

remove_materials COMMERCIALcastle_mesh0365.obj
remove_materials COMMERCIALcastle_mesh0882.obj
remove_materials COMMERCIALcastle_mesh0904.obj
