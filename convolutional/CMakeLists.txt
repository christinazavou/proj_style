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

#https://stackoverflow.com/questions/45614230/running-multiple-versions-of-opencv-on-the-same-computer
find_package(OpenCV 2.4.8 REQUIRED PATHS "/opt/opencv-2.4.8/release/installed")
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(${EXECUTABLE} ${OpenCV_LIBS})
