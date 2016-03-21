from display import *
from matrix import *
from draw import *
from math import *

def parse_file( fname, points, transform, screen, color ):
    # Setup screen
    screen = new_screen()
    # flag for whether image was modified
    modified = False
    # pen color
    pen = [0, 255, 0]
    
    # Setup edges as empty list
    edges = []
    T = new_matrix()
    
    # Open file, read script, and close it
    script = None
    with open(fname) as f:
        script = f.read()
    
    # Parse script - separate at whitespace
    args = script.split()
    itr = iter(args)
    
    # Do not loop through the list because we need to get multiple elements
    while True:
        cmd = next(itr, "quit").lower()
        print cmd

        # Drawing routines
        if cmd == "line":
            add_edge(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), \
                     float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)))
            modified = True
        elif cmd == "circle" or cmd == "c":
            add_circle(edges, float(next(itr, 0)), float(next(itr, 0)), 0, float(next(itr, 0)), 0.01)
            modified = True
        elif cmd == "hermite" or cmd == "h":
            add_curve(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), 0.05, HERMITE)
            modified = True
        elif cmd == "bezier" or cmd == "b":
            add_curve(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), 0.05, BEZIER)
            modified = True
        
        # matrix control operations
        elif cmd == "ident":
            ident(T)
        elif cmd == "translate":
            u = make_translate(float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)))
            matrix_mult(u, T)
        elif cmd == "scale":
            u = make_scale(float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)))
            matrix_mult(u, T)
        elif cmd == "xrotate":
            u = make_rotX(radians(float(next(itr, 0))))
            matrix_mult(u, T)
        elif cmd == "yrotate":
            u = make_rotY(radians(float(next(itr, 0))))
            matrix_mult(u, T)
        elif cmd == "zrotate":
            u = make_rotZ(radians(float(next(itr, 0))))
            matrix_mult(u, T)
        elif cmd == "apply":
            matrix_mult(T, edges)
            modified = True
        
        # engine control operations
        elif cmd == "display":
            if modified:
                print "Redraw screen"
                clear_screen(screen)
                draw_lines(edges, screen, pen)
                modified = False
            display(screen)
        elif cmd == "save":
            if modified:
                print "Redraw screen"
                clear_screen(screen)
                draw_lines(edges, screen, pen)
                modified = False
            # if the filename isn't specified, do nothing
            fname = next(itr, None)
            if fname is not None:
                if fname[-4:].lower() == ".ppm":
                    save_ppm(screen, fname)
                else:
                    save_extension(screen, fname)
        elif cmd == "quit":
            return
