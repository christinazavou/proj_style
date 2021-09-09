cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_C_COMPILER gcc-5)
set(CMAKE_CXX_COMPILER g++-5)

project(Convolutional)
set(EXECUTABLE Convolutional)
set(TEST_READ_EXE TestReadFile)

file(GLOB HEADERS
        "*.h")
file(GLOB SOURCES
        "*.cpp")

add_executable(${EXECUTABLE}
        ${HEADERS}
        main.cpp)
add_executable(${TEST_READ_EXE}
        ${HEADERS}
        test_reader.cpp)

set(OPENCV_INCLUDE_DIR /opt/opencv-2.4.8/release/installed/include/)
set(OPENCV_LIB_DIR /opt/opencv-2.4.8/release/installed/lib/)
set(OPENCV_LIBRARIES libopencv_objdetect.so libopencv_imgproc.so libopencv_highgui.so libopencv_core.so)
include_directories(${OPENCV_INCLUDE_DIR})
link_directories(${OPENCV_LIB_DIR})
target_link_libraries(${EXECUTABLE} ${OPENCV_LIBRARIES})
set(MORE_LIB_DIR /usr/lib/x86_64-linux-gnu)
link_directories(${MORE_LIB_DIR})
target_link_libraries(${EXECUTABLE} libz.so)
#find_package(OpenCV REQUIRED)  # equivalent of g++ ... `pkg-config --cflags --libs opencv`
#target_link_libraries(${EXECUTABLE} ${OpenCV_LIBS})
