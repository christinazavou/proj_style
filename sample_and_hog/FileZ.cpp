#include "FileZ.h"
#include <unistd.h>
#include <cstring>
#include <dirent.h>
#include <sys/io.h>
#include <sys/types.h>

static constexpr const char* PATH_SEP = "/";

FileZ::FileZ()
{
	this->name = "";
	this->subdir = true;
}

FileZ::FileZ(string name, string type, bool subdir)
{
	this->name = name;
	this->type = type;
	this->subdir = subdir;
}

bool FileZ::isExist()
{
	if ((access(this->name.c_str(), F_OK)) != -1)
	{
		return true;
		/* Check for write permission */
		/*if ((_access("ACCESS.C", 2)) != -1)
		printf("File ACCESS.C has write permission ");*/
	}
	else
		return false;

}

void FileZ::getFiles(string name)
{
	intptr_t   hFile = 0;
	string p;

    DIR* dirFile = opendir(name.c_str());
    if ( dirFile )
    {
        struct dirent* hFile;
        errno = 0;
        while (( hFile = readdir( dirFile )) != NULL )
        {
            if ( !strcmp( hFile->d_name, "."  )) continue;
            if ( !strcmp( hFile->d_name, ".." )) continue;

            // in linux hidden files all start with '.'
            if ( hFile->d_name[0] == '.' ) continue;

            // dirFile.name is the name of the file. Do whatever string comparison
            // you want here. Something like:
            if ( strstr( hFile->d_name, ".obj" )){
                cout << "found an .obj file " << hFile->d_name << endl;
                Info info;
                info.directory = name;
                info.file = hFile->d_name;
                info.path = name + PATH_SEP + hFile->d_name;
                info.name = info.file.substr(0, info.file.find_first_of("."));
                this->files.push_back(info);
            }
        }
        closedir( dirFile );
    }
}

void FileZ::getFiles()
{
	getFiles(this->name);
}

void FileZ::copyFile(string target)
{
	fstream f1(this->name, ios::in);
	fstream f2(target, ios::out);

	f2 << f1.rdbuf();

	f2.close();
	f1.close();
}

void FileZ::writeResult(string path, string flag)
{
	ofstream ofs;
	ofs.open(path);
	if (ofs.fail())
	{
		cout << "?" << endl;
	}
	if (flag == "f")
	{
		//for (auto it = this->subfile.begin(); it != this->subfile.end(); it++)
		//{
		//	ofs << *it << endl;
		//}
	}
	else if (flag == "p")
	{
		/*for (auto it = this->subpath.begin(); it != this->subpath.end(); it++)
		{
		ofs << *it << endl;
		}*/
	}


	ofs.close();
}

void FileZ::copyFile(string source, string target)
{
	fstream f1(source, ios::in);
	fstream f2(target, ios::out);

	f2 << f1.rdbuf();

	f2.close();
	f1.close();
}
