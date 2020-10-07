cmake_minimum_required(VERSION 3.17)
project(ProjStyleSampleAndHog)

set(CMAKE_CXX_STANDARD 14)
set(EXECUTABLE ProjStyleSampleAndHog)
set(TEST_EXECUTABLE TestApp)

file(GLOB HEADERS
        "*.h")
file(GLOB SOURCES
        "*.cpp")

add_executable(${EXECUTABLE}
        ${HEADERS}
        ${SOURCES})

set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
set(OpenCVLinkers -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_objdetect) # setting all the opencv libraries as one variable.
target_link_libraries(${EXECUTABLE} ${OpenGlLinkers}) # linking opengl libraries to the project
target_link_libraries(${EXECUTABLE} ${OpenCVLinkers}) # linking opencv libraries to the project


add_executable(${TEST_EXECUTABLE}
        test_src/TestMe.cpp)