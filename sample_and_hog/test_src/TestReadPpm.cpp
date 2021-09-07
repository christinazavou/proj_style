//
// Created by christina on 15-10-20.
//

#include <vector>
#include <fstream>
#include <iostream>
#include <cmath>

using namespace std;


struct RGB
{
    unsigned char r, g, b;
};

struct ImageRGB
{
    int w, h;
    std::vector<RGB> data;
};

void eat_comment(ifstream &f)
{
    char linebuf[1024];
    char ppp;
    while (ppp = f.peek(), ppp == '\n' || ppp == '\r')
        f.get();
    if (ppp == '#')
        f.getline(linebuf, 1023);
}

void load_ppm(ImageRGB &img, const string &name)
{
    ifstream f(name.c_str(), ios::binary);
    if (f.fail())
    {
        std::cout << "Could not open file: " << name << endl;
        return;
    }

    // get type of file
    eat_comment(f);
    int mode = 0;
    string s;
    f >> s;
    if (s == "P3")
        mode = 3;
    else if (s == "P6")
        mode = 6;

    // get w
    eat_comment(f);
    f >> img.w;

    // get h
    eat_comment(f);
    f >> img.h;

    // get bits
    eat_comment(f);
    int bits = 0;
    f >> bits;

    // error checking
    if (mode != 3 && mode != 6)
    {
        cout << "Unsupported magic number" << endl;
        f.close();
        return;
    }
    if (img.w < 1)
    {
        cout << "Unsupported width: " << img.w << endl;
        f.close();
        return;
    }
    if (img.h < 1)
    {
        cout << "Unsupported height: " << img.h << endl;
        f.close();
        return;
    }
    if (bits < 1 || bits > 255)
    {
        cout << "Unsupported number of bits: " << bits << endl;
        f.close();
        return;
    }

    // load image data
    img.data.resize(img.w * img.h);

    if (mode == 6)
    {
        f.get();
        f.read((char*)&img.data[0], img.data.size() * 3);
    }
    else if (mode == 3)
    {
        for (int i = 0; i < img.data.size(); i++)
        {
            int v;
            f >> v;
            img.data[i].r = v;
            f >> v;
            img.data[i].g = v;
            f >> v;
            img.data[i].b = v;
        }
    }

    // close file
    f.close();
}

ImageRGB imcrop(ImageRGB* image, int x, int y, int size)
{
    if (x<1 || y<1 || x + size >image->w || y + size> image->h)
    {
        cout << "imcrop error" << endl;
        exit(0);
    }
    ImageRGB* patch = new ImageRGB;
    patch->data.resize((size+1) * (size+1));
    for (int i = y; i <= y + size; i++)
        for (int j = x; j <= x + size; j++)
            patch->data[(i - y)*(size + 1) + j - x] = image->data[(i - 1)*image->w + j - 1];
    patch->h = size + 1;
    patch->w = size + 1;
    return *patch;
}


int main(int argc, char * argv[]){
    ImageRGB myimg;
    load_ppm(myimg, "/media/christina/Data/ANNFASS_code/zavou-repos/proj_style/data/our_car/style_patch/1_3_2.ppm");
    std::cout<<"myimg:";
    const ImageRGB newpatch = imcrop(&myimg, 75, 85, 15 - 1);
    std::cout<<"myimg:";

}