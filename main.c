#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lib/ml6.h"
#include "lib/display.h"
#include "lib/draw.h"
#include "lib/matrix.h"

int main() {
  // Setup
  
  screen s;
  struct matrix *restrict edges;
  struct matrix *restrict transform;

  edges = new_matrix(4, 4);

  // Put crap here

  double restrict vector[4] = {0, 0, 0, 1};
  double *restrict x = vector;
  double *restrict y = vector + 1;

  // Draw a pentagram
  
  // First point of pentagram
  *x = 0;
  *y = -200;

  // First transformation is a 144-degree rotation (one for each point in the pentagram)
  transform = make_rotZ_degree(144);

  // point 1
  append_vector(edges, vector);

  
  
  // Next transformation is a translation from the origin to the center of the screen

  // Clean up
  free_matrix( transform );
  free_matrix( edges );
}  
