//
// Created by christina on 11-10-20.
//

#include "test_reader.h"

int main(int argv, char* args[]){
//    CL("/media/christina/Data/ANNFASS_code/zavou-repos/proj_style/data/their_building/imagesname/picname1.txt");
//    CL("../../data/their_building/imagesname/picname1.txt");

    std::ifstream ifs ("/data/their_building/imagesname/picname1.txt", std::ifstream::in);

    char c = ifs.get();

    while (ifs.good()) {
        std::cout << "eeee";
        c = ifs.get();
    }

    ifs.close();

    cout<<"kati";
}