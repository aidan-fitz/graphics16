#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <math.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

int main() {

  screen s;
  color c;

  // init red, go to blue (thru purple or green???)
  c.red = MAX_COLOR;
  c.green = 0;
  c.blue = 0;

  double DEGREE = M_PI / 180;

  // init 0
  double theta = 0;

  // count to 90
  while (theta <= M_PI_2) {
    int x1 = 0;
    int y1 = (int) (YRES * cos(theta));

    int x2 = (int) (XRES * sin(theta));
    int y2 = 0;

    draw_line(x1, y1, x2, y2, s, c);

    theta += DEGREE;
    
  }

  save_extension(s, "envelope.png");
  display(s);

}
