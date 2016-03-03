#include <math.h> // for M_PI

#ifndef MATRIX_H
#define MATRIX_H

struct matrix {
  double **restrict m;
  int rows, cols;
  int usedcols;
} matrix;

//Basic matrix manipulation routines
struct matrix *new_matrix(int rows, int cols);
void free_matrix(struct matrix *m);
void grow_matrix(struct matrix *m, int newcols);
void copy_matrix(struct matrix *a, struct matrix *b);
void print_matrix(struct matrix *m);
void ident(struct matrix *m);

void scalar_mult(double x, struct matrix *m);
void matrix_mult(struct matrix *a, struct matrix *b);

void vector_mult(struct matrix *a, double *vector);

struct matrix *make_translate(double x, double y, double z);
struct matrix *make_scale(double x, double y, double z);

struct matrix *make_rotX(double theta);
struct matrix *make_rotY(double theta);
struct matrix *make_rotZ(double theta);

#define DEGREE M_PI / 180
#define make_rotX_degree(theta) make_rotX(theta * DEGREE)
#define make_rotY_degree(theta) make_rotY(theta * DEGREE)
#define make_rotY_degree(theta) make_rotZ(theta * DEGREE)

// Resizable matrix routines
void append_matrix(struct matrix *master, struct matrix *newcols);
void append_vector(struct matrix *master, double *vector);

#endif
