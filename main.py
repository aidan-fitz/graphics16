#!/usr/bin/python

from display import *
from draw import *
from draw3d import *
from parser import *
from matrix import *

import sys

screen = new_screen()
pen2d = [0, 255, 0]
pen3d = [255, 0, 255]
edges = []
polygons = []
transform = new_matrix()

fname = None
if len(sys.argv) >= 2:
    fname = sys.argv[1]
else:
    fname = '/dev/stdin'

parse_file( fname, edges, polygons, transform, screen, pen2d, pen3d )
