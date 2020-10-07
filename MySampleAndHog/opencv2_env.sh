#!/bin/sh
export PATH=/opt/opencv/latest/bin:/opt/opencv/latest/release/bin:${PATH}
export LD_LIBRARY_PATH=/opt/opencv/latest/release/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=/opt/opencv/latest/lib/pkgconfig
export OPENCV_TEST_DATA_PATH=/opt/opencv/latest/opencv_extra-master/testdata