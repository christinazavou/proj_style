#ifndef _FILE_H
#define _FILE_H

#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>

using namespace std;

class Info
{
public:
	string path;
	string file;
	string directory;
	string name;
};

class FileZ
{
public:
	FileZ();
	FileZ(string name, string type = NULL, bool subdir = true);
	bool isExist();
	void getFiles();
	void getFiles(string name);
	void copyFile(string target);
	void copyFile(string source, string target);
	void writeResult(string path, string flag);
public:
	string name;
	string type;
	bool subdir;
	vector<Info> files;

};

#endif // !_FILE_H