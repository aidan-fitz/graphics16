from display import *
from matrix import *
from draw import *
from math import *

def parse_file( fname, points, transform, screen, color ):
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
        # Drawing routines
        if cmd == "line":
            add_edge(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), \
                     float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)))
        elif cmd == "circle":
            add_circle(edges, float(next(itr, 0)), float(next(itr, 0)), 0, float(next(itr, 0)), 0.05)
        elif cmd == "hermite":
            add_curve(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), 0.05, HERMITE)
        elif cmd == "bezier":
            add_curve(edges, float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), float(next(itr, 0)), 0.05, BEZIER)
        # control operations
        elif cmd == "quit":
            return
