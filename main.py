#!/usr/bin/python

from display import *
from draw import *
from parser import *
from matrix import *

import sys

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
transform = new_matrix()

fname = None
if len(sys.argv) >= 2:
    fname = sys.argv[1]
else:
    fname = 'script_nocurves'

parse_file( fname, edges, transform, screen, color )
