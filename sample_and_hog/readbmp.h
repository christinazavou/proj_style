#ifndef _READBMP_H
#define _READBMP_H


//#include <gl\glut.h>
#include <GL/glut.h>
#include <string>
using namespace std;
//static GLint    ImageWidth;
//static GLint    ImageHeight;
//static GLint    PixelLength;
//static GLubyte* PixelData;
#define   WIDTHBYTES(bits) (((bits)+31)/32*4)  // row size = (bits per pixel * image width + 31)/32*4

typedef unsigned char BYTE;
typedef unsigned short WORD;
typedef unsigned long DWORD;
typedef long LONG;

typedef struct mytagBITMAPFILEHEADER
{
uint32_t bfSize;
ushort  bfReserved1;
ushort  bfReserved2;
uint32_t bfOffBits;
} BITMAPFILEHEADER;

typedef struct mytagBITMAPINFOHEADER{

uint32_t  biSize;
int32_t   biWidth;
int32_t    biHeight;
ushort   biPlanes;
ushort    biBitCount;
uint32_t   biCompression;
uint32_t   biSizeImage;
int32_t    biXPelsPerMeter;
int32_t    biYPelsPerMeter;
uint32_t   biClrUsed;
uint32_t   biClrImportant;
} BITMAPINFOHEADER;


typedef struct mytagRGBQUAD {

BYTE     rgbBlue;
BYTE     rgbGreen;
BYTE     rgbRed;
//BYTE     rgbReserved;
} myRGBQUAD;
typedef struct tagRGBQUAD2 {

BYTE     rgbBlue;
BYTE     rgbGreen;
BYTE     rgbRed;
BYTE     rgbReserved;
} RGBQUAD2;

typedef struct BmpImageInfo {

myRGBQUAD* dataOfBmp;
GLint width;
GLint height;
GLint depth;
} BmpImage;
typedef struct BlackPatchindex {

GLfloat x1;
GLfloat y1;
GLfloat x2;
GLfloat y2;
} Patch;

BmpImage* readbmp(string Filename);
Patch* getpatch(unsigned char *bitmapData,int width, int height);
BmpImage* imcrop(BmpImage* image,int x, int y,int size);

#endif