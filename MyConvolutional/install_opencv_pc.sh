#!/bin/bash

# download opencv2.4.8.zip, extract it and put it under /opt

cd /opt/opencv-2.4.8/

# first add in CMakeLists.txt first line: set(CMAKE_CXX_STANDARD 11)

mkdir release && cd release

mkdir release/installed && sudo cmake -D WITH_CUDA=OFF \
      -D CMAKE_CXX_COMPILER=/usr/bin/g++-5 \
      -D CMAKE_C_COMPILER=/usr/bin/gcc-5 \
      -D ENABLE_AVX=OFF \
      -D WITH_OPENGL=OFF \
      -D WITH_OPENCL=OFF \
      -D WITH_IPP=OFF \
      -D WITH_EIGEN=OFF \
      -D WITH_V4L=OFF \
      -D WITH_FFMPEG=OFF \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/opt/opencv-2.4.8/release/installed ..
sudo make -j6
sudo make install
