//
// Created by graphicslab on 7/9/21.
//

#include <iostream>
#include <fstream>
#include <string>

using namespace std;
int main(){
    ifstream myFile_Handler;
    string myLine;

    myFile_Handler.open("../CMakeLists.txt");

    if(myFile_Handler.is_open()){
        while(getline(myFile_Handler, myLine)){
            cout << myLine << endl;
        }
        myFile_Handler.close();
    }
    else{
        cout << "Unable to open the file!";
    }
    return 0;
}