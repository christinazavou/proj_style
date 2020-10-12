cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

project(MyConvApp)

set(OPENCV_INCLUDE_DIR /usr/local/include/)
set(OPENCV_LIB_DIR /usr/local/lib/)
set(EXECUTABLE MyConvExe)
set(OPENCV_LIBRARIES libopencv_objdetect.so libopencv_imgproc.so libopencv_highgui.so libopencv_core.so)

include_directories(${OPENCV_INCLUDE_DIR})
link_directories(${OPENCV_LIB_DIR})

file(GLOB HEADERS "*.h")
file(GLOB SOURCES "*.cpp")
#add_executable(${EXECUTABLE} ${HEADERS} ${SOURCES})
add_executable(${EXECUTABLE} main.cpp)
target_link_libraries(${EXECUTABLE} ${OPENCV_LIBRARIES})
add_executable(TestExe test_reader.cpp test_reader.h)
