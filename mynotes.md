
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


opencv248:
sudo apt-get install libtiff5-dev
sudo apt-get install gtk2.0
## sudo apt-get install libv4l-dev


mpainoun sto /usr/include


dont run tests: -DBUILD_opencv_ts=0
dont enable cuda support: -D WITH_CUDA=OFF

==> ok with sudo cmake -DBUILD_opencv_ts=0 -D WITH_CUDA=OFF . && make


sudo cmake -DBUILD_opencv_ts=0 -D WITH_CUDA=OFF -DCMAKE_BUILD_TYPE=Release -DOPENCV_GENERATE_PKGCONFIG=YES -DCMAKE_INSTALL_PREFIX=/media/graphicslab/zavou/dev_libraries/opencv/opencv-2.4.8  /media/graphicslab/zavou/dev_libraries/opencv/opencv-2.4.8
cd /media/graphicslab/zavou/dev_libraries/opencv/latest/release
sudo make
sudo make install
sudo ldconfig
sudo touch /etc/profile.d/opencv.sh
with:
	#!/bin/sh
	export PATH=//media/graphicslab/zavou/dev_libraries/opencv/latest/bin:/media/graphicslab/zavou/dev_libraries/opencv/latest/release/bin:${PATH}
	export LD_LIBRARY_PATH=/media/graphicslab/zavou/dev_libraries/opencvlatest/release/lib:$LD_LIBRARY_PATH
	export PKG_CONFIG_PATH=/media/graphicslab/zavou/dev_libraries/opencv/latest/lib/pkgconfig
sudo chmod +x /etc/profile.d/opencv.sh
source /etc/profile.d/opencv.sh


opencv3:
sudo apt-get install gcc g++ cmake pkg-config build-essential libgtk2.0-dev libavcodec-dev libavformat-dev  libtiff5-dev  libswscale-dev 

sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"

sudo apt update

sudo apt install libjasper1 libjasper-dev


opencv3.3.1:
sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev
sudo apt-get install python3-pip
sudo pip3 install -U pip numpy
git clone https://github.com/opencv/opencv.git
cd opencv && git checkout 3.3.1 && cd ..
git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib && git checkout 3.3.1 && cd ..
cd opencv && mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D BUILD_opencv_world=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON \
      -D WITH_CUDA=OFF \
      -D BUILD_opencv_java=OFF \
      -D BUILD_opencv_python=OFF \
      -D BUILD_opencv_python3=OFF \
      -DOPENCV_GENERATE_PKGCONFIG=ON \
      -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3.8 ..
make -j4
sudo make install
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig

check:
pkg-config --modversion opencv
pkg-config --cflags opencv

