//
// Created by christina on 13-10-20.
//

#include "testReadFiles.h"
#include "../FileZ.h"

int main(int argc, char * argv[])
{

    FileZ fz;

    //initial model
    fz.name = "../../data/our_car/models";
    fz.type = "obj";
    fz.getFiles();
    std::cout << fz.files.size() << std::endl;


    return 0;

}