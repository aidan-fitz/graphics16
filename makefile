OBJECTS= main.o draw.o display.o
CFLAGS= -Wall
CC= gcc

all: $(OBJECTS)
	$(CC) -o main $(OBJECTS) -lm

main.o: main.c lib/display.h lib/draw.h lib/ml6.h
	$(CC) -c main.c

draw.o: lib/draw.c lib/draw.h lib/display.h lib/ml6.h
	$(CC) $(CFLAGS) -c lib/draw.c -o draw.o

display.o: lib/display.c lib/display.h lib/ml6.h
	$(CC) $(CFLAGS) -c lib/display.c -o display.o

clean:
	rm *.o *~
