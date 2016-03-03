#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h> // for memcpy, oddly enough (why not stdlib?)

#include "matrix.h"

/*-------------- struct matrix *new_matrix() --------------
Inputs:  int rows
         int cols 
Returns: 

Once allocated, access the matrix as follows:
m->m[r][c]=something;
if (m->lastcol)... 
*/
struct matrix *new_matrix(int rows, int cols) {
  double **tmp;
  int i;
  struct matrix *m;

  tmp = (double **)malloc(rows * sizeof(double *));
  for (i = 0; i < rows; i++) {
    tmp[i]=(double *)malloc(cols * sizeof(double));
  }

  m=(struct matrix *)malloc(sizeof(struct matrix));
  m->m=tmp;
  m->rows = rows;
  m->cols = cols;
  m->usedcols = 0;

  return m;
}


/*-------------- void free_matrix() --------------
Inputs:  struct matrix *m 
Returns: 

1. free individual rows
2. free array holding row pointers
3. free actual matrix
*/
void free_matrix(struct matrix *m) {

  int i;
  for (i = 0; i < m->rows; i++) {
    free(m->m[i]);
  }
  free(m->m);
  free(m);
}


/*======== void grow_matrix() ==========
Inputs:  struct matrix *m
         int newcols 
Returns: 

Reallocates the memory for m->m such that it now has
newcols number of collumns
====================*/
void grow_matrix(struct matrix *m, int newcols) {  
  int i;
  for (i = 0; i < m->rows; i++) {
    m->m[i] = realloc(m->m[i], newcols * sizeof(double));
  }
  m->cols = newcols;
}


/*-------------- void print_matrix() --------------
Inputs:  struct matrix *m 
Returns: 

print the matrix
*/
void print_matrix(struct matrix *m) {
  int row, col;
  for (row = 0; row < m->rows; row++) {
    for (col = 0; col < m->usedcols; col++) {
      printf("%f ", m->m[row][col]);
    }
    putchar('\n');
  }
}

/*-------------- void ident() --------------
Inputs:  struct matrix *m <-- assumes m is a square matrix
Returns: 

turns m into an identity matrix
*/
void ident(struct matrix *m) {
  grow_matrix(m, m->rows);
  m->usedcols = m->rows;

  int i;
  for (i = 0; i < m->rows; i++) {
    // Set all the cells to 0.0
    memset(m->m[i], 0, m->usedcols * sizeof(double));

    // Set the diagonal to 1.0
    m->m[i][i] = 1.0;    
  }
}


/*-------------- void scalar_mult() --------------
Inputs:  double x
         struct matrix *m 
Returns: 

multiply each element of m by x
*/
void scalar_mult(double x, struct matrix *m) {
  int row, col;
  for (row = 0; row < m->rows; row++) {
    for (col = 0; col < m->usedcols; col++) {
      m->m[row][col] *= x;
    }
  }

}


/*-------------- void matrix_mult() --------------
Inputs:  struct matrix *a
         struct matrix *b 
Returns: 

a*b -> b
*/
void matrix_mult(struct matrix *a, struct matrix *b) {
  // In-place matrix multiplication
  // For the first round (before optimising), we'll simply allocate a new matrix,
  // do our business, copy it in, and free.

  if (a->cols == b->rows) {  
    struct matrix *product = new_matrix(a->rows, b->cols);

    int m, n, p;
    for (m = 0; m < a->rows; m++) {
      for (n = 0; n < b->usedcols; n++) {
	product->m[m][n] = 0.0;
	for (p = 0; p < a->usedcols; p++) {
	  product->m[m][n] += a->m[m][p] * b->m[p][n];
	}
      }
    }

    copy_matrix(product, b);

    free_matrix(product);
  }

  else {
    // it's an error
  }
}

void vector_mult(struct matrix *a, double *vector) {
  // Can't check size of vector, but that's fine

  double *result = calloc(a->rows, sizeof(double));

  int i, j;
  for (i = 0; i < a->rows; i++) {
    for (j = 0; j < a->usedcols; j++) {
      result[i] +=  a->m[i][j] * vector[j];
    }
  }

  memcpy(vector, result, a->rows * sizeof(double));

  free(result);
}




/*-------------- void copy_matrix() --------------
Inputs:  struct matrix *a
         struct matrix *b 
Returns: 

copy matrix a to matrix b
*/
void copy_matrix(struct matrix *a, struct matrix *b) {

  grow_matrix(b, a->usedcols);
  b->usedcols = a->usedcols;
  
  int r, c;

  for (r=0; r < a->rows; r++) {
    for (c=0; c < a->usedcols; c++) { 
      b->m[r][c] = a->m[r][c];
    }
  }
  
}

/*======== struct matrix * make_translate() ==========
Inputs:  int x
         int y
         int z 
Returns: The translation matrix created using x, y and z 
as the translation offsets.
====================*/
struct matrix *make_translate(double x, double y, double z) {
  struct matrix *yolo = new_matrix(4, 4);
  ident(yolo);
  yolo->m[0][3] = x;
  yolo->m[1][3] = y;
  yolo->m[2][3] = z;
  return yolo;
}

/*======== struct matrix * make_scale() ==========
Inputs:  int x
         int y
         int z 
Returns: The translation matrix creates using x, y and z
as the scale factors
====================*/
struct matrix * make_scale(double x, double y, double z) {
  struct matrix *yolo = new_matrix(4, 4);
  ident(yolo);
  yolo->m[0][0] = x;
  yolo->m[1][0] = y;
  yolo->m[2][0] = z;
  return yolo;  
}

/*======== struct matrix * make_rotX() ==========
Inputs:  double theta

Returns: The rotation matrix created using theta as the 
angle of rotation and X as the axis of rotation.
====================*/
struct matrix *make_rotX(double theta) {
  struct matrix *m = new_matrix(4, 4);
  int i;
  for (i = 0; i < m->rows; i++) {
    memset(m->m[i], 0, m->usedcols * sizeof(double));
  }

  double s = sin(theta), c = cos(theta);

  m->m[1][1] = c;  m->m[1][2] = -s;
  m->m[2][1] = s;  m->m[2][2] = c;

  return m;
}

/*======== struct matrix * make_rotY() ==========
Inputs:  double theta

Returns: The rotation matrix created using theta as the 
angle of rotation and Y as the axis of rotation.
====================*/
struct matrix *make_rotY(double theta) {
  struct matrix *m = new_matrix(4, 4);
  int i;
  for (i = 0; i < m->rows; i++) {
    memset(m->m[i], 0, m->usedcols * sizeof(double));
  }

  double s = sin(theta), c = cos(theta);

  m->m[0][0] = c;  m->m[0][2] = -s;
  m->m[2][0] = s;  m->m[2][2] = c;

  return m;
}

/*======== struct matrix * make_rotZ() ==========
Inputs:  double theta

Returns: The rotation matrix created using theta as the 
angle of rotation and Z as the axis of rotation.
====================*/
struct matrix *make_rotZ(double theta) {
  struct matrix *m = new_matrix(4, 4);
  int i;
  for (i = 0; i < m->rows; i++) {
    memset(m->m[i], 0, m->usedcols * sizeof(double));
  }

  double s = sin(theta), c = cos(theta);

  m->m[0][0] = c;  m->m[0][1] = -s;
  m->m[1][0] = s;  m->m[1][1] = c;

  return m;
}

void append_matrix(struct matrix *master, struct matrix *newcols) {
  if (master->rows == newcols->rows) {
    // If space runs out, double the # of available columns
    if (master->usedcols + newcols->usedcols > master->cols) {
      grow_matrix(master, master->cols * 2);
    }

    // Copy rows of new matrix
    // This routine uses master->usedcols so don't update it yet~!
    int row, col;
    for (row = 0; row < newcols->rows; row++) {
      for (col = 0; col < newcols->cols; col++) {
	master->m[row][master->usedcols + col] = newcols->m[row][col];
      }
    }

    // then update usedcols
    master->usedcols += newcols->usedcols;
  }
}

void append_vector(struct matrix *master, double *vector) {
  // can't check size of double array

  // If space runs out, double the # of available columns
  if (master->usedcols + 1 > master->cols) {
    grow_matrix(master, master->cols * 2);
  }

  // Copy rows of new matrix
  // This routine uses master->usedcols so don't update it yet~!
  int row;
  for (row = 0; row < master->rows; row++) {
      master->m[row][master->usedcols] = vector[row];
  }

  // then update usedcols
  master->usedcols++;

}
