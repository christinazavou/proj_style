
#include "../FileZ.h"

int main(int argc, char * argv[])
{
    FileZ fz;
    fz.name = "../../data/our_car/models";
    fz.type = "obj";
    fz.getFiles();
    std::cout << fz.files.size() << std::endl;
    return 0;
}