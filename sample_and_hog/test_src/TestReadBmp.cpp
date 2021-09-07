//
// Created by root on 7/10/20.
//
#include <iostream>
#include "../readbmp.h"

using namespace std;

int main(int argc, char * argv[]){
    int a = 1;
    std::cout << std::to_string(a);
    string filename = "/media/graphicslab/BigData/zavou/ANNFASS_CODE/proj_style/data/building_yu/3dlines/1.bmp";
    BmpImage*image = readbmp(filename);
    std::cout << "entaksi";
    std::cout << image->height;
    std::cout << image->width;
}
