cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 14)
set(OPENGL_LIB_DIR /usr/lib/x86_64-linux-gnu)
set(OPENGL_INCLUDE_DIR /usr/include)
set(EXECUTABLE MyBackProjectedExe)

project(MyBackProjectedApp)

include_directories(${OPENGL_INCLUDE_DIR})
link_directories(${OPENGL_LIB_DIR})

file(GLOB HEADERS "*.h")
file(GLOB SOURCES "*.cpp")

add_executable(${EXECUTABLE} ${HEADERS} ${SOURCES})

add_executable(TestExt test/testReadFiles.cpp test/testReadFiles.h FileZ.cpp FileZ.h)

target_link_libraries(${EXECUTABLE} libGL.so libglut.so libGLU.so)
