cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_C_COMPILER gcc-7)
set(CMAKE_CXX_COMPILER g++-7)

project(SampleAndHog)
set(EXECUTABLE SampleAndHog)
set(TEST_BMP_EXE TestReadBmp)
set(TEST_FILE_EXE TestReadFile)
set(TEST_PPM_EXE TestReadPpm)

file(GLOB HEADERS
        "*.h")
file(GLOB SOURCES
        "*.cpp")

add_executable(${EXECUTABLE}
        ${HEADERS}
        ${SOURCES})


add_executable(${TEST_BMP_EXE}
        test_src/TestReadBmp.cpp
        readbmp.cpp)

add_executable(${TEST_FILE_EXE}
        test_src/TestReadFile.cpp)

add_executable(${TEST_PPM_EXE}
        test_src/TestReadPpm.cpp)

set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project
find_package(OpenCV REQUIRED)  # equivalent of g++ ... `pkg-config --cflags --libs opencv`
target_link_libraries(${EXECUTABLE} ${OpenCV_LIBS})
set(MORE_LIB_DIR /usr/lib/x86_64-linux-gnu)
link_directories(${MORE_LIB_DIR})
target_link_libraries(${EXECUTABLE} libz.so)
