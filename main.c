#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lib/ml6.h"
#include "lib/display.h"
#include "lib/draw.h"
#include "lib/matrix.h"

int main() {

  screen s;
  struct matrix *edges;
  struct matrix *transform;

  edges = new_matrix(4, 4);
  transform = new_matrix(4, 4);

  
  free_matrix( transform );
  free_matrix( edges );
}  
