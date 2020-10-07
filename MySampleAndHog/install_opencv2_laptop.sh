#!/bin/bash

cd Downloads && wget https://github.com/opencv/opencv/archive/2.4.13.5.zip -O opencv-2.4.13.5.zip
sudo mkdir /opt/opencv
sudo unzip ~/Downloads/opencv-2.4.13.5.zip -d /opt/opencv
cd /opt/opencv
sudo ln -s opencv-2.4.13.5 latest
cd latest && sudo mkdir release && cd release
sudo cmake -DCMAKE_CXX_COMPILER=/usr/bin/g++-5 \
           -DCMAKE_C_COMPILER=/usr/bin/gcc-5 \
           -DCMAKE_BUILD_TYPE=Release \
           -DOPENCV_GENERATE_PKGCONFIG=YES \
           -DCMAKE_INSTALL_PREFIX=/opt/opencv/opencv-2.4.13.5  ..
sudo make -j$(nproc)
sudo make install
sudo ldconfig
sudo touch /etc/profile.d/opencv.sh
sudo cp opencv2_env.sh /etc/profile.d/opencv.sh
sudo chmod +x /etc/profile.d/opencv.sh
sudo find /opt -name opencv*.pc
sudo updatedb
locate opencv_version | grep bin/opecv_version
opencv_version
