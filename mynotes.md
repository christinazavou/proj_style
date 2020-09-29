
If i want to run only style localization for "our_furniture":

matlab -nodesktop -nosplash -r "output_our_style('our_furniture');exit"
start "" "..\..\Back_projected\back_projection.exe" "..\..\Back_projected\params_our_furniture.cfg"

if i want to run everything for "demo":
- i need 3dlines and models folder of demo
- cd scripts\demo
- ./sample.sh (C++)
  ```start "" "..\..\sample_and_hog\sample.exe" "sampling" "..\..\sample_and_hog\params_demo.cfg"```
  (logika to sample.exe exei dimiourgithei apo ton linker tis c++ vasei tou main.cpp sto folder sample_and_hog)
  (aporia: sta params.cfg exei seed_num:30 .. kai sta labels.m exei 30 labels .. diladi mono 30 samples pairnei ? ti einai auta ta samples? NOMIZO EINAI TRIANGLE MESHES!)
(note: ta data examples periexoun rotated examples)
(now i have patch and sample_points folders)
- ./cluster.sh (matlab)
  ```matlab -nodesktop -nosplash -r "Complete_run('demo',1);exit"```
  i.e. run data preparation
  1. runCT() i.e. calculate HOG
  2. runCluster() i.e. get with kmeans the centers of preselected clustered patches
  3. run_cluster_idf() i.e. get kernel for convolution
  4. preCNN()
- .\convolute.sh
  ```start "" "..\..\convolutional\convolute.exe" "..\..\convolutional\params_demo.cfg"```
- .\show_style.sh
  ```start "" "..\..\Back_projected\back_projection.exe" "..\..\Back_projected\params_demo.cfg"```
  `


trimesh:
sudo apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
cd /usr/include/X11/extensions && sudo ln -s XI.h XInput.h
