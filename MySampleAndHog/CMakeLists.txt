cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

project(ProjStyleSampleAndHog)

set(EXECUTABLE ProjStyleSampleAndHog)

add_executable(${EXECUTABLE}
        main.cpp
        readbmp.cpp
        model.cpp
        FileZ.cpp)

set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project

#set(OPENCV_LIB_DIR /usr/lib/x86_64-linux-gnu)
#link_directories(${OPENCV_LIB_DIR})
#target_link_libraries(${EXECUTABLE} libopencv_core.so.3.2 libopencv_imgcodecs.so.3.2 libopencv_highgui.so.3.2 libopencv_objdetect.so.3.2)
set(OPENCV_LIB_DIR /opt/opencv/latest/release/lib)
link_directories(${OPENCV_LIB_DIR})
target_link_libraries(${EXECUTABLE} libopencv_core.so.2.4 libopencv_highgui.so.2.4 libopencv_objdetect.so.2.4 libopencv_imgproc.so.2.4)
#set(OpenCVLinkers -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_objdetect) # setting all the opencv libraries as one variable.
#target_link_libraries(${EXECUTABLE} ${OpenCVLinkers}) # linking opencv libraries to the project

#mkdir release & cd release
#cmake -G "Unix Makefiles" -DCMAKE_CXX_COMPILER=/usr/bin/g++-5 CMAKE_C_COMPILER=/usr/bin/gcc-5 -DOPENCV_GENERATE_PKGCONFIG=YES -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DWITH_TBB=ON -DBUILD_NEW_PYTHON_SUPPORT=ON -DWITH_V4L=ON -DINSTALL_C_EXAMPLES=OFF -DINSTALL_PYTHON_EXAMPLES=OFF -DBUILD_EXAMPLES=ON -DWITH_QT=ON -DWITH_OPENGL=ON -DBUILD_FAT_JAVA_LIB=ON -DINSTALL_TO_MANGLED_PATHS=ON -DINSTALL_CREATE_DISTRIB=ON -DINSTALL_TESTS=ON -DENABLE_FAST_MATH=ON -DWITH_IMAGEIO=ON -DBUILD_SHARED_LIBS=OFF -DWITH_GSTREAMER=ON ..
#make all -j$(nproc) # Uses all machine cores
#sudo make install
#cd ../../
#rm -rf ./opencv-2.4.13.5
#sudo apt-get install python-opencv -y
#pkg-config --modversion opencv
#sudo find . -name "opencv2.4*"


#sudo mkdir /opt/opencv
#sudo unzip ~/Downloads/opencv-2.4.13.5.zip -d /opt/opencv
#cd /opt/opencv
#sudo ln -s opencv-2.4.13.5 latest
#cd /opt/opencv/latest
#sudo mkdir release && cd release
#sudo cmake -DCMAKE_CXX_COMPILER=/usr/bin/g++-5 CMAKE_C_COMPILER=/usr/bin/gcc-5 -DCMAKE_BUILD_TYPE=Release -DOPENCV_GENERATE_PKGCONFIG=YES -DCMAKE_INSTALL_PREFIX=/opt/opencv/opencv-2.4.13.5  ..
#sudo make -j$(nproc)
#sudo make install
#sudo ldconfig
#sudo touch /etc/profile.d/opencv.sh
#sudo nano /etc/profile.d/opencv.sh
#    #!/bin/sh
#    export PATH=/opt/opencv/latest/bin:/opt/opencv/latest/release/bin:${PATH}
#    export LD_LIBRARY_PATH=/opt/opencv/latest/release/lib:$LD_LIBRARY_PATH
#    export PKG_CONFIG_PATH=/opt/opencv/latest/lib/pkgconfig
#    export OPENCV_TEST_DATA_PATH=/opt/opencv/latest/opencv_extra-master/testdata
#sudo chmod +x /etc/profile.d/opencv.sh
#sudo find /opt -name opencv*.pc
#sudo updatedb
#locate opencv_version | grep bin/opecv_version
#opencv_version
