
#include "FileZ.h"
#include "CommonZ.h"
#include "model.h"
#include <ctime>
#include <cstdio>
#include <iostream>
#include <cmath>
#include <cstring>

using namespace std;
GLint window_size = 200;

GLMmodel *model;
double threshold = 0.0;
GLfloat radius = 0.0;
double angle_threshold = 60.0;
double view_distance = 1.5;

int model_current = 0;

int snum = 0;
int view_num = 0;

string models_path;
string seed_path;
string style_path;

string back_projection_path;
FileZ fz;

clock_t start;
clock_t finish;

const string PATH_SEP = "/";

//Sampling seeds
void setseed_and_style(string filename)
{
	cout << "read seed" << endl;
	FILE *file;
	file = fopen(filename.data(), "r");
	if (!file)
	{
		fprintf(stderr, "setseed failed: can't open file \"%s\".\n", filename.c_str());
		system("PAUSE");
		exit(1);
	}
	char st1[30];
	fgets(st1, 30, file);
	fgets(st1, 30, file);
	model->numseeds = snum;
	model->seeds = (GLfloat *)malloc(sizeof(GLfloat)* 3 * (model->numseeds));

	for (int i = 0; i < model->numseeds; i++)
	{

		fscanf(file, "%f %f %f\n", &model->seeds[3 * i + 0], &model->seeds[3 * i + 1], &model->seeds[3 * i + 2]);
	}

	fclose(file);

	cout << "read style" << endl;
	
	model->isstyle = new bool[model->numseeds];
	for (int i = 0; i < model->numseeds; i++)
		model->isstyle[i] = false;
	

	fstream stylefile;
	stylefile.open(style_path, ios::in);
	string imagename;

	while (getline(stylefile, imagename))
	{
		int pos = imagename.find('_', 0);
		string s_m_index = imagename.substr(0, pos);
		int m_index = atoi(s_m_index.data()) - 1;
		if (m_index == model_current)
		{
			int pos2 = imagename.find('.', 0);
			string s_s_index = imagename.substr(pos + 1, pos2 - pos - 1);
			int s_index = atoi(s_s_index.data()) - 1;
			model->isstyle[s_index] = true;
		}
		if (m_index > model_current)
		{
			break;
		}
	}
	stylefile.close();
}

//color the style areas
void isincube()
{
	cout << "color style patches" << endl;
	model->iscolored = new bool[model->numseeds * model->numtriangles];
	for (int i = 0; i < (model->numseeds * model->numtriangles); i++)
		model->iscolored[i] = false;

	for (int i = 0; i < model->numseeds; i++)
	{
		for (int j = 0; j < model->numtriangles; j++)
		{
			double distance0 = pow(model->vertices[model->triangles[j].vindices[0] * 3 + 0] - model->seeds[3 * i + 0], 2)
				+ pow(model->vertices[model->triangles[j].vindices[0] * 3 + 1] - model->seeds[3 * i + 1], 2)
				+ pow(model->vertices[model->triangles[j].vindices[0] * 3 + 2] - model->seeds[3 * i + 2], 2);

			double distance1 = pow(model->vertices[model->triangles[j].vindices[1] * 3 + 0] - model->seeds[3 * i + 0], 2)
				+ pow(model->vertices[model->triangles[j].vindices[1] * 3 + 1] - model->seeds[3 * i + 1], 2)
				+ pow(model->vertices[model->triangles[j].vindices[1] * 3 + 2] - model->seeds[3 * i + 2], 2);

			double distance2 = pow(model->vertices[model->triangles[j].vindices[2] * 3 + 0] - model->seeds[3 * i + 0], 2)
				+ pow(model->vertices[model->triangles[j].vindices[2] * 3 + 1] - model->seeds[3 * i + 1], 2)
				+ pow(model->vertices[model->triangles[j].vindices[2] * 3 + 2] - model->seeds[3 * i + 2], 2);

			if (distance0 < threshold && distance1 < threshold && distance2 < threshold)
			{
				model->iscolored[i * model->numtriangles + j] = true;
			}
		}
	}
}

/**
 * Save the current image to a PPM file.
 * (from TriMesh2 library)
 */
void dump_image(const char* output_file)
{
    // Find first non-used filename
    FILE *f;
    while (1) {
        f = fopen(output_file, "rb");
        if (!f) {
            f = fopen(output_file, "wb");
            printf("\n\nSaving image %s... ", output_file);
            fflush(stdout);
            break;
        }
        fclose(f);
    }

    // Read pixels
    GLint V[4];
    glGetIntegerv(GL_VIEWPORT, V);
    GLint width = V[2], height = V[3];
    char *buf = new char[width*height*3];
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    glReadPixels(V[0], V[1], width, height, GL_RGB, GL_UNSIGNED_BYTE, buf);

    // Flip top-to-bottom
    for (int i = 0; i < height/2; i++) {
        char *row1 = buf + 3 * width * i;
        char *row2 = buf + 3 * width * (height - 1 - i);
        for (int j = 0; j < 3 * width; j++)
            std::swap(row1[j], row2[j]);
    }

    // Write out file
    fprintf(f, "P6\n#\n%d %d\n255\n", width, height);
    fwrite(buf, width*height*3, 1, f);
    fclose(f);
    delete [] buf;

    printf("Done.\n\n");
}

void saveScreenShotAsPpm(GLfloat angle)
{
	int view_current = angle / 30 + 1;
	string
		filename2 = back_projection_path + PATH_SEP +
		std::to_string(model_current + 1) + "_" +
		std::to_string(model->seed_current + 1) + "_" +
		std::to_string(view_current) + ".ppm";
    dump_image(filename2.data());
}

void initialize(string params)
{
	//initialize parameters
	if (params.empty())
	{
		cout << "please input the parameters file" << endl;
		cin.get();
		exit(0);
	}

	ifstream ifs;
	ifs.open(params);
	if (ifs.fail())
	{
		cout << "can't open parameters file" << endl;
	}
	string tmp;
	ifs >> tmp >> models_path
		>> tmp >> back_projection_path
		>> tmp >> seed_path
		>> tmp >> style_path
		>> tmp >> snum
		>> tmp >> view_num
		>> tmp >> radius
		>> tmp >> angle_threshold;

	ifs.close();

	threshold = pow(radius, 2) * 3;
	
	//initial model
	fz.name = models_path;
	fz.type = "obj";
	fz.getFiles();

}

void initRendering()
{
	glClearColor(1.0, 1.0, 1.0, 0.0);
	glEnable(GL_DEPTH_TEST);
	glDepthMask(GL_TRUE);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glShadeModel(GL_SMOOTH);
	glPixelStorei(GL_PACK_ROW_LENGTH, 0);
	glPixelStorei(GL_PACK_ALIGNMENT, 1);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_NORMALIZE);

	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glDisable(GL_LIGHT1);

	GLfloat mat_ambient[] = { 32.0 / 255.0f, 32.0 / 255.0f, 32.0 / 255.0f, 1.0f };
	GLfloat mat_diffuse[] = { 182.0 / 255.0f, 182.0 / 255.0f, 182.0 / 255.0f, 1.0f };
	GLfloat mat_specular[] = { 0.6f, 0.6f, 0.6f, 1.0f };


	//GLfloat mat_ambient[] = { 32.0/255.0f, 32.0/255.0f, 32.0/255.0f, 1.0f };
	//GLfloat mat_diffuse[] = { 1.0f,0.0f, 0.0f, 1.0f };
	//GLfloat mat_specular[] = { 0.6f, 0.2f, 0.0f, 1.0f };

	glLightfv(GL_LIGHT0, GL_AMBIENT, mat_ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, mat_diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, mat_specular);

	/*glLightfv(GL_LIGHT1, GL_AMBIENT, mat_ambient);
	glLightfv(GL_LIGHT1, GL_DIFFUSE, mat_diffuse);
	glLightfv(GL_LIGHT1, GL_SPECULAR, mat_specular);*/

	glEnable(GL_COLOR_MATERIAL);
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
	glDisable(GL_CULL_FACE);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	/*gluLookAt(0, 1 * 2, -1.732 * 2,
		0, 0, 0,
		0, 1 * 2, 1.732 * 2);*/
	
	gluLookAt(0, -1.732 * view_distance, 1 * view_distance,
		0, 0, 0,
		0, 1 * view_distance, 1.732 * view_distance);
}

void reshape(int w, int h)
{
	glViewport(0, 0, (GLsizei)w, (GLsizei)h);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	//gluPerspective(60.0,(GLfloat)w/(GLfloat)h,1.0,20.0);
	glOrtho(-1, 1, -1, 1, 1.0, 20.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	gluLookAt(0, -1.732 * view_distance, 1 * view_distance,
		0, 0, 0,
		0, 1 * view_distance, 1.732 * view_distance);
}


void render()
{
	
	cout << "render" << endl;
	for (int k = 0; k < fz.files.size(); k++)
	{
		start = clock();
		model = glmReadOBJ(const_cast<char *>(fz.files[model_current].path.c_str()));
		int pos = fz.files[model_current].path.find_last_of(PATH_SEP);
		int length = fz.files[model_current].path.length();
		string seed_filename = seed_path + PATH_SEP + fz.files[model_current].path.substr(pos + 1, length - 5 - pos) + ".off";
		setseed_and_style(seed_filename);
		isincube();
		for (int i = 0; i < 30; i++)
		{
			for (GLfloat angle = 30; angle < angle_threshold; angle = angle + 30)
			{

				glPushMatrix();
				glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

				glRotatef((GLfloat)angle, 0, 0, 1);
				
				for (int i = 0; i < model->numtriangles; i++)
				{
					glBegin(GL_TRIANGLES);
					//glPolygonMode(GL_FRONT_AND_BACK, GL_FILL); 
					//cout << "color size is" << _msize(model->iscolored)/sizeof(bool);

					if (model->iscolored[model->seed_current * model->numtriangles + i] == false)
					{
						glColor3f(0.71f, 0.71f, 0.71f);
					}
					else
					{
						glColor3f(0.0f, 0.0f, 8.0f);
						//glColor3f(0.71f, 0.71f, 0.71f);
					}

					int ifindex = model->triangles[i].findex;
					glNormal3f(model->facetnorms[3 * ifindex], model->facetnorms[3 * ifindex + 1], model->facetnorms[3 * ifindex + 2]);

					glVertex3f(model->vertices[model->triangles[i].vindices[0] * 3 + 0],
						model->vertices[model->triangles[i].vindices[0] * 3 + 1],
						model->vertices[model->triangles[i].vindices[0] * 3 + 2]);

					glVertex3f(model->vertices[model->triangles[i].vindices[1] * 3 + 0],
						model->vertices[model->triangles[i].vindices[1] * 3 + 1],
						model->vertices[model->triangles[i].vindices[1] * 3 + 2]);

					glVertex3f(model->vertices[model->triangles[i].vindices[2] * 3 + 0],
						model->vertices[model->triangles[i].vindices[2] * 3 + 1],
						model->vertices[model->triangles[i].vindices[2] * 3 + 2]);

					glEnd();

				}

				glPopMatrix();

				if (model->isstyle[model->seed_current])
                    saveScreenShotAsPpm(angle);
				//glutSwapBuffers();
			}
			model->seed_current++;
		}

		cout << fz.files[model_current].file << " done!" << endl;
		glmDelete(model);
		model_current++;
		finish = clock();
		cout << "it takes " << (finish - start) / 1000 << "seconds" << endl;
	}

}


int main(int argc, char * argv[])
{

	start = clock();

	if (argc <2)
		return 0;

	string params = argv[1];

	initialize(params);

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(window_size, window_size);
	glutInitWindowPosition(window_size, 100);
	glutCreateWindow("Sampling parts");
	glutHideWindow();
	initRendering();
	reshape(window_size, window_size);
	render();

	return 0;

}