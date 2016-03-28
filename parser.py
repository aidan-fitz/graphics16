from display import *
from matrix import *
from draw import *
from draw3d import *
from math import *

def parse_file( fname, edges, T, screen, pen ):
    # flag for whether image was modified
    modified = False
    
    # Iterating over the file so we can keep it open
    # Allows us to use stdin
    with open(fname) as fd:
        itr = iter(fd)
        
        # Do not loop through the list because we need to get multiple elements
        while True:
            cmd = next(itr, "quit").strip().lower()
            
            # Skip comments and blank lines
            if cmd == '' or cmd[0] == '#':
                continue

            print cmd

            # 2-D drawing routines
            if cmd == "line":
                args = next(itr).split()
                x0 = float(args[0])
                y0 = float(args[1])
                z0 = float(args[2])
                x1 = float(args[3])
                y1 = float(args[4])
                z1 = float(args[5])
                add_edge(edges, x0, y0, z0, x1, y1, z1)
                modified = True
            elif cmd == "circle" or cmd == "c":
                args = next(itr).split()
                cx = float(args[0])
                cy = float(args[1])
                cz = 0
                r = float(args[2])
                step = 1/round(4 * sqrt(r))
                add_circle(edges, cx, cy, cz, r, step)
                modified = True
            elif cmd == "hermite" or cmd == "h":
                args = next(itr).split()
                x = [float(s) for s in args[:4]]
                y = [float(s) for s in args[4:]]
                add_curve(edges, x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3], 0.05, HERMITE)
                modified = True
            elif cmd == "bezier" or cmd == "b":
                args = next(itr).split()
                x = [float(s) for s in args[:4]]
                y = [float(s) for s in args[4:]]
                add_curve(edges, x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3], 0.05, BEZIER)
                modified = True
            
            # 3-D drawing routines
            elif cmd == "box":
                args = next(itr).split()
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                width = float(args[3])
                height = float(args[4])
                depth = float(args[5])
                add_box(edges, x, y, z, width, height, depth)
                modified = True
            elif cmd == 'sphere':
                args = next(itr).split()
                x = float(args[0])
                y = float(args[1])
                z = 0
                r = float(args[2])
                step = 1/round(4 * sqrt(r))
                add_sphere(edges, x, y, z, r, step)
                modified = True
            elif cmd == 'torus':
                args = next(itr).split()
                x = float(args[0])
                y = float(args[1])
                z = 0
                r = float(args[2])
                R = float(args[3])
                step = 1/round(4 * sqrt(r))
                add_torus(edges, x, y, z, r, R, step)
                modified = True

            # clear edge matrix
            elif cmd == "clear":
                edges = []
                modified = True

            # matrix control operations
            elif cmd == "ident":
                ident(T)
            elif cmd == "translate":
                args = next(itr).split()
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                u = make_translate(x, y, z)
                matrix_mult(u, T)
            elif cmd == "scale":
                args = next(itr).split()
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                u = make_scale(x, y, z)
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
                    print "Redraw"
                    clear_screen(screen)
                    draw_lines(edges, screen, pen)
                    modified = False
                display(screen)
            elif cmd == "save":
                if modified:
                    print "Redraw"
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
            
            # handle invalid commands
            else:
                print 'Invalid command:', cmd
