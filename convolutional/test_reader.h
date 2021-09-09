//
// Created by christina on 11-10-20.
//

#ifndef MYCONVAPP_TEST_READER_H
#define MYCONVAPP_TEST_READER_H
#include <fstream>
#include<iostream>
using namespace std;


int CL(const char *filename){
    cout <<"CL"<<endl;
    ifstream ReadFile;
    int n=0;
    string temp;
    ReadFile.open(filename);
    if(ReadFile.fail())
    {
        ReadFile.close();
        return 0;
    }else
    {

        while(getline(ReadFile,temp)){

            n++;
        }
        ReadFile.close();
        return n;
    }
}

#endif //MYCONVAPP_TEST_READER_H
