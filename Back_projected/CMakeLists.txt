cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_COMPILER_ID GNU)

project(BackProjected)
set(EXECUTABLE BackProjected)

#include_directories(${OPENGL_INCLUDE_DIR})
#link_directories(${OPENGL_LIB_DIR})

file(GLOB HEADERS "*.h")
file(GLOB SOURCES "*.cpp")

add_executable(${EXECUTABLE} ${HEADERS} ${SOURCES})

#add_executable(TestExe FileZ.h FileZ.cpp test/test_bmp_io.cpp)
#add_executable(TestExe0 test/BitmapIO_0.cpp test/BitmapIO_0.h)
#add_executable(TestExe1 test/BitmapIO_1.cpp)

#set(OPENGL_LIB_DIR /usr/lib/x86_64-linux-gnu)
#set(OPENGL_INCLUDE_DIR /usr/include)
#target_link_libraries(${EXECUTABLE} libGL.so libglut.so libGLU.so)

set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project
set(MORE_LIB_DIR /usr/lib/x86_64-linux-gnu)
link_directories(${MORE_LIB_DIR})
target_link_libraries(${EXECUTABLE} libz.so)