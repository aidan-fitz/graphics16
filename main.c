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

  clear_screen(s);

  // init red, go to blue (thru purple)
  c.red = MAX_COLOR;
  c.green = 0;
  c.blue = 0;
  
  const double DEGREE = M_PI / 180;

  int theta;

  for (theta = 0; theta <= 360;) {
    int x1 = 0;
    int y1 = (int) (YRES * cos(theta*DEGREE) / 2);

    int x2 = (int) (XRES * sin(theta*DEGREE) / 2);
    int y2 = 0;

    draw_line(x1, y1, x2, y2, s, c);

    // printf("%d %d %d %d \n", theta, c.red, c.green, c.blue);

    // Moved increment statement into loop
    theta++;

    // red to purple
    if (theta <= 45) {
      c.blue = theta * 255 / 45;
    }
    // to blue
    if (45 <= theta && theta < 90) {
      c.red = (90 - theta) * 255 / 45;
    }
    // to white
    if (90 <= theta && theta < 180) {
      c.green = (theta - 90) * 255 / 90;
      c.red = c.green;
    }
    // to yellow
    if (180 <= theta && theta < 270) {
      c.blue = (270 - theta) * 255 / 90;
    }
    // back to red
    if (270 <= theta) {
      c.green = (360 - theta) * 255 / 90;
    }
  }

  save_extension(s, "envelope.png");
  display(s);

  // for testing purposes
  //save_ppm(s, "envelope.ppm");
  
}
