
#include "test_reader.h"

int main(int argv, char* args[]){
    std::ifstream ifs ("/media/graphicslab/BigData/zavou/ANNFASS_CODE/proj_style/data/building_yu/imagesname/picname1.txt", std::ifstream::in);

    char c;

    while (ifs.good()) {
        c = ifs.get();
        std::cout << c;
    }

    ifs.close();

    cout<<"telos";
}