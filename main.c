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
  struct matrix *edges;
  struct matrix *transform;

  clear_screen(s);

  edges = new_matrix(4, 4);

  // Put crap here

  double vertex[5][4];

  int i;
  for (i = 0; i < 5; i++) {
    memset(vertex[i], 0, 4 * sizeof(double));
  }

  // Draw a pentagram
  
  // First vertex of pentagram
  vertex[0][0] = 0;
  vertex[0][1] = -200;
  vertex[0][2] = 0;
  vertex[0][3] = 1;

  // Make each of the four remaining vertices by rotating each previous one by 144 degrees

  transform = make_rotZ_degree(144);

  for (i = 1; i < 5; i++) {
    vector_mult(transform, vertex[i-1], vertex[i]);
  }

  free_matrix(transform);

  // Translate each point such that the pentagram is centered
  // This transformation maps origin to center
  
  transform = make_translate(XRES / 2, YRES / 2, 0);

  for (i = 0; i < 5; i++) {
    double result[4];
    vector_mult(transform, vertex[i], result);
    copy_vector(vertex[i], result);
  }

  free_matrix(transform);

  // Append each vertex to the edge matrix twice
  for (i = 0; i < 5; i++) {
    append_vector(edges, vertex[i % 5]);
    append_vector(edges, vertex[(i + 1) % 5]);
  }

  print_matrix(edges);

  // Draw!
  color pen;
  pen.red = 0;
  pen.green = 0;
  pen.blue = 0;

  draw_edges(edges, s, pen);

  save_extension(s, "pentagram.png");

  // Clean up
  free_matrix(edges);
}  
