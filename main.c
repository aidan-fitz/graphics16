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

  for (theta = 0; theta <= 90;) {
    int x1 = 0;
    int y1 = (int) (YRES * cos(theta*DEGREE));

    int x2 = (int) (XRES * sin(theta*DEGREE));
    int y2 = 0;

    draw_line(x1, y1, x2, y2, s, c);

    // printf("%d %d %d %d \n", theta, c.red, c.green, c.blue);

    // Moved increment statement into loop
    theta++;
    
    if (theta <= 45) {
      c.blue = theta * 255 / 45;
    }
    if (theta >= 45) {
      c.red = (90 - theta) * 255 / 45;
    }
  }

  save_extension(s, "envelope.png");
  display(s);

  // for testing purposes
  //save_ppm(s, "envelope.ppm");
  
}
