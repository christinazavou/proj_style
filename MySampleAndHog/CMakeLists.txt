cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_C_COMPILER gcc-7)
set(CMAKE_CXX_COMPILER g++-7)

project(ProjStyleSampleAndHog)
set(EXECUTABLE ProjStyleSampleAndHog)
set(TEST_EXECUTABLE TestApp)

file(GLOB HEADERS
        "*.h")
file(GLOB SOURCES
        "*.cpp")

add_executable(${EXECUTABLE}
        ${HEADERS}
        ${SOURCES})

#add_executable(${TEST_EXECUTABLE}
#        test_src/TestReadBmp.cpp
#        readbmp.cpp
#        readbmp.h)

add_executable(${TEST_EXECUTABLE}
        test_src/TestReadPpm.cpp)

## on pc:
#set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
#set(OpenCVLinkers -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_objdetect) # setting all the opencv libraries as one variable.
#target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project
#target_link_libraries(${EXECUTABLE} ${OpenCVLinkers}) # linking opencv libraries to the project

# on laptop:
set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project
#set(OPENCV_LIB_DIR /usr/lib/x86_64-linux-gnu)
#link_directories(${OPENCV_LIB_DIR})
#target_link_libraries(${EXECUTABLE} libopencv_core.so.3.2 libopencv_imgcodecs.so.3.2 libopencv_highgui.so.3.2 libopencv_objdetect.so.3.2)
set(OPENCV_LIB_DIR /opt/opencv/latest/release/lib)
link_directories(${OPENCV_LIB_DIR})
# note that order matters. libopencv_objectdetect depends on libopencv_imgproc etc.
target_link_libraries(${EXECUTABLE} libopencv_objdetect.so.2.4 libopencv_imgproc.so.2.4 libopencv_highgui.so.2.4 libopencv_core.so.2.4)
set(MORE_LIB_DIR /usr/lib/x86_64-linux-gnu)
link_directories(${MORE_LIB_DIR})
target_link_libraries(${EXECUTABLE} libz.so)
