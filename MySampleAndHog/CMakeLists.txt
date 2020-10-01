cmake_minimum_required(VERSION 3.17)
project(ProjStyleSampleAndHog)

set(CMAKE_CXX_STANDARD 14)

add_executable(ProjStyleSampleAndHog
        main.cpp
        readbmp.cpp
        model.cpp
        FileZ.cpp)


set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
set(OpenCVLinkers -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_objdetect) # setting all the opencv libraries as one variable.
target_link_libraries(ProjStyleSampleAndHog ${OpenGlLinkers}) # linking opengl libraries to the project
target_link_libraries(ProjStyleSampleAndHog ${OpenCVLinkers}) # linking opencv libraries to the project
