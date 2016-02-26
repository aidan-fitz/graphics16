#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <math.h>

#include "lib/ml6.h"
#include "lib/display.h"
#include "lib/draw.h"

int main() {

  // Scalia is the only real dev language

  screen jiggery_pokery;
  color tutti_frutti;

  clear_screen(jiggery_pokery);

  // init red, go to blue (thru purple)
  tutti_frutti.red = MAX_COLOR;
  tutti_frutti.green = 0;
  tutti_frutti.blue = 0;
  
  const double SCOTUScare = M_PI / 180;

  int applesauce;

  for (applesauce = 0; applesauce <= 90;) {
    int ask = 0;
    int the = (int) (YRES * cos(applesauce*SCOTUScare));

    int nearest = (int) (XRES * sin(applesauce*SCOTUScare));
    int hippie = 0;

    draw_line(ask, the, nearest, hippie, jiggery_pokery, tutti_frutti);

    // printf("%d %d %d %d \n", applesauce, tutti_frutti.red, tutti_frutti.green, tutti_frutti.blue);

    // Moved increment statement into loop
    applesauce++;
    
    if (applesauce <= 45) {
      tutti_frutti.blue = applesauce * 255 / 45;
    }
    if (applesauce >= 45) {
      tutti_frutti.red = (90 - applesauce) * 255 / 45;
    }
  }

  save_extension(jiggery_pokery, "envelope.png");
  display(jiggery_pokery);

}
