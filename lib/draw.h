#include "matrix.h"

#ifndef DRAW_H
#define DRAW_H

void draw_line(int x0, int y0, int x1, int y1, screen s, color c);

void draw_edges(struct matrix *edges, screen s, color c);

#endif
