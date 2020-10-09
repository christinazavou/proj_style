//
// Created by root on 7/10/20.
//
#include <iostream>
#include "../readbmp.h"

using namespace std;

int main(int argc, char * argv[]){
    int a = 1;
    std::cout << std::to_string(a);
    BmpImage*image = readbmp("../demo/3dlines/1.bmp");
    std::cout << "entaksi";
}
