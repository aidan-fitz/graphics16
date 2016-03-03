#include <stdio.h>
#include <stdlib.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

// Bresenham's line algorithm
void draw_line(int x0, int y0, int x1, int y1, screen s, color c) {
  // The other half of the octants (3-6)
  if (x0 > x1) {
    draw_line(x1, y1, x0, y0, s, c);
    return;
  }

  int x = x0, y = y0;
  int A = y1 - y0, B = x0 - x1;

  // Octant 2: m > 1
  if (B > -A) {
    int d = A + 2*B;
    A *= 2;
    B *= 2;
    while (y <= y1) {
      plot(s, c, x, y);
      if (d < 0) {
	x++;
	d += A;
      }
      y++;
      d += B;
    }
  }
  
  // Octant 1: 1 > m > 0
  else if (y1 > y0) {
    int d = 2*A + B;
    A *= 2;
    B *= 2;
    while (x <= x1) {
      plot(s, c, x, y);
      if (d > 0) {
	y++;
	d += B;
      }
      x++;
      d += A;
    }
  }

  // Octant 8: 0 > m > -1
  else if (A > B) {
    int d = -2*A + B;
    A *= 2;
    B *= 2;
    while (x <= x1) {
      plot(s, c, x, y);
      if (d > 0) {
	y--;
	d += B;
      }
      x++;
      d -= A;
    }
  }

  // Octant 7: -1 > m
  else {
    int d = A - 2*B;
    A *= 2;
    B *= 2;
    while (y >= y1) {
      plot(s, c, x, y);
      if (d > 0) {
	x++;
	d += A;
      }
      y--;
      d -= B;
    }

  }
}

void draw_edges(struct matrix *edges, screen s, color c) {
  int i;
  for (i = 0; i < edges->usedcols; i += 2) {
    draw_line(edges->m[0][i], edges->m[1][i], edges->m[0][i + 1], edges->m[1][i + 1], s, c);
  }
}
